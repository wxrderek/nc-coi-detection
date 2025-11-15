#!/usr/bin/env python3
"""
nc_bg_adjacency.py

Downloads NC block group TIGER/Line shapefile, counts BGs, builds adjacency (queen or rook),
and writes outputs:
  - nc_bg_edges.csv  (columns: source,target)
  - nc_bg_adj.json   (adjacency dict: GEOID -> [GEOID,...])

Requires: geopandas, requests, rtree (for sindex), shapely, optionally libpysal (fast).
Install: pip install geopandas requests rtree shapely pyproj
Optional (faster adjacency builder): pip install libpysal
"""

import os
import sys
import zipfile
import tempfile
import shutil
import json
import time
from pathlib import Path

import requests
import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union

# PARAMETERS
YEAR = "2020"
STATE_FIPS = "37"                      # NC
TIGER_BASE = "https://www2.census.gov/geo/tiger/TIGER{year}/BG/"  # TIGER{year}/BG/
# For 2020 TIGER/Line the file pattern is like tl_2020_37_bg.zip
TIGER_ZIPNAME = f"tl_{YEAR}_{STATE_FIPS}_bg.zip"
TIGER_URL = TIGER_BASE.format(year=YEAR) + TIGER_ZIPNAME

OUTPUT_DIR = Path(".")
EDGE_CSV = OUTPUT_DIR / "nc_bg_edges.csv"
ADJ_JSON = OUTPUT_DIR / "nc_bg_adj.json"
SHAPE_CACHE = OUTPUT_DIR / f"tl_{YEAR}_{STATE_FIPS}_bg"  # folder to extract to (if you want to reuse)
GEOID_COLS = ["GEOID", "GEOID20", "GEOID_BG", "GEOID10", "GEOID20"]  # possible names

# Choose adjacency type: "queen" (touch by point or edge) or "rook" (share boundary length)
ADJTYPE = os.getenv("ADJTYPE", "queen").lower()  # override by env var ADJTYPE=rook

# Target projected CRS for geometry ops (equal area)
CRS_TARGET = "EPSG:5070"  # Albers Conus Equal Area

# Small tolerance for numeric checks (rook)
LENGTH_TOL = 1e-9

# Helper functions
def download_and_extract(url, dest_folder: Path):
    dest_folder = dest_folder.resolve()
    dest_folder.mkdir(parents=True, exist_ok=True)
    tmpzip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    try:
        print(f"Downloading {url} ...")
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(tmpzip.name, "wb") as fh:
            for chunk in r.iter_content(chunk_size=8192):
                fh.write(chunk)
        print("Download complete, extracting...")
        with zipfile.ZipFile(tmpzip.name, "r") as zf:
            zf.extractall(path=dest_folder)
        print("Extracted to", dest_folder)
        return dest_folder
    finally:
        try:
            os.unlink(tmpzip.name)
        except Exception:
            pass

def find_shapefile(folder: Path):
    # returns path to first .shp in folder
    for p in folder.iterdir():
        if p.suffix.lower() == ".shp":
            return p
    # try nested
    for p in folder.rglob("*.shp"):
        return p
    raise FileNotFoundError("No .shp file found in extracted TIGER zip.")

def choose_geoid_column(gdf: gpd.GeoDataFrame):
    for c in GEOID_COLS:
        if c in gdf.columns:
            return c
    # fallback: try any column named lower-case geoid
    for c in gdf.columns:
        if c.lower() == "geoid":
            return c
    raise KeyError("No GEOID column found in shapefile. Available columns: " + ", ".join(gdf.columns))

def build_adjacency_with_libpysal(gdf, geoid_col, adjtype="queen"):
    from libpysal.weights import Queen, Rook
    print("Building adjacency using libpysal (fast C-backed routines)...")
    # libpysal expects geometries in planar CRS and non-empty
    if adjtype == "queen":
        w = Queen.from_dataframe(gdf, idVariable=geoid_col)
    else:
        w = Rook.from_dataframe(gdf, idVariable=geoid_col)
    # w.neighbors maps geoid -> list of neighbor geoids (or indices if not idVariable)
    neighbors = {}
    for gid, neigh in w.neighbors.items():
        # w.neighbors keys are the geoid values when idVariable provided
        neighbors[str(gid)] = [str(n) for n in neigh]
    # But libpysal may return indices if idVariable not recognized; normalize below if needed
    # If values look like ints that are indices, fallback to mapping via gdf.index
    # Check one key: if it's numeric string equal to an index? We'll assume proper idVariable works.
    return neighbors

def build_adjacency_with_geopandas(gdf, geoid_col, adjtype="queen"):
    import time
    try:
        from tqdm import tqdm
        has_tqdm = True
    except Exception:
        has_tqdm = False

    print("Building adjacency using GeoPandas + spatial index (with fallback).")
    sindex = gdf.sindex
    geoms = gdf.geometry.values
    ids = gdf[geoid_col].astype(str).values
    n = len(geoms)

    # First try: use query_bulk if available (fast)
    try:
        pairs = sindex.query_bulk(geoms, predicate="intersects")
        left_idx, right_idx = pairs
        mask = left_idx < right_idx
        left_idx = left_idx[mask]
        right_idx = right_idx[mask]
        print(f"query_bulk candidate pairs: {len(left_idx)}")
        candidate_iter = zip(left_idx, right_idx)
    except AttributeError:
        # Fallback: iterate each geometry and use intersection on its bounds
        print("SpatialIndex has no query_bulk — falling back to per-geometry intersection (may be slower).")
        # We'll build a list of candidate pairs (i,j) with i < j
        candidate_pairs = []
        rng = range(n)
        if has_tqdm:
            iter_range = tqdm(rng, desc="Index queries")
        else:
            iter_range = rng

        for i in iter_range:
            geom = geoms[i]
            if geom is None or geom.is_empty:
                continue
            # query index by bounding box -> returns indices of possible intersects (including itself)
            try:
                possible = list(sindex.intersection(geom.bounds))
            except Exception:
                # If intersection(...) fails for a specific geom, skip it
                continue
            for j in possible:
                if j <= i:
                    continue  # keep only i < j to avoid duplicates & self-pairs
                candidate_pairs.append((i, j))

        print("Candidate pairs from intersection-loop:", len(candidate_pairs))
        candidate_iter = iter(candidate_pairs)

    # Now refine candidate pairs with accurate geometry predicates
    edges = []
    adjacency = {}

    # We will iterate through candidate_iter which yields (i,j) pairs
    if has_tqdm:
        # Try to get length for progress if possible
        try:
            length = len(left_idx)
        except Exception:
            try:
                length = len(candidate_pairs)
            except Exception:
                length = None
        candidate_iter = tqdm(candidate_iter, total=length, desc="Refining pairs")

    for i, j in candidate_iter:
        g1 = geoms[i]; g2 = geoms[j]
        if g1 is None or g2 is None or g1.is_empty or g2.is_empty:
            continue
        try:
            if adjtype == "queen":
                # consider touches (touching at point or line)
                if g1.touches(g2):
                    a = ids[i]; b = ids[j]
                else:
                    continue
            else:  # rook
                if g1.touches(g2):
                    inter = g1.boundary.intersection(g2.boundary)
                    if inter.is_empty:
                        continue
                    # length check to ensure not just a point
                    try:
                        if inter.length > 1e-9:
                            a = ids[i]; b = ids[j]
                        else:
                            continue
                    except Exception:
                        if inter.geom_type not in ("Point", "MultiPoint"):
                            a = ids[i]; b = ids[j]
                        else:
                            continue
                else:
                    continue
        except Exception:
            # geometry op problem; skip
            continue

        edges.append((a, b))
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)

    # convert sets to lists
    adjacency = {k: sorted(v) for k, v in adjacency.items()}
    return edges, adjacency

def main():
    print("NC Block Group adjacency builder (TIGER year", YEAR, ")")
    use_cached = False
    extract_folder = SHAPE_CACHE
    if extract_folder.exists() and any(extract_folder.glob("*.shp")):
        print("Found existing extracted shapefile folder:", extract_folder)
        use_cached = True

    try:
        if not use_cached:
            download_and_extract(TIGER_URL, extract_folder)
        shp = find_shapefile(extract_folder)
    except Exception as e:
        print("Error obtaining shapefile:", e)
        sys.exit(1)

    print("Reading shapefile:", shp)
    gdf = gpd.read_file(shp)
    print("Rows read:", len(gdf))
    if len(gdf) == 0:
        print("No features found in shapefile.")
        sys.exit(1)

    # choose geoid col
    try:
        geoid_col = choose_geoid_column(gdf)
        print("Using GEOID column:", geoid_col)
    except KeyError as e:
        print("ERROR:", e)
        print("Available columns:", list(gdf.columns))
        sys.exit(1)

    # Keep only geoid and geometry (memory friendly)
    gdf = gdf[[geoid_col, "geometry"]].dropna(subset=["geometry"]).reset_index(drop=True)
    # Project to planar CRS for reliable geometry ops
    print("Projecting to CRS", CRS_TARGET, "for geometry operations...")
    gdf = gdf.to_crs(CRS_TARGET)

    # Fix invalid geometries if any
    invalid_count = (~gdf.is_valid).sum()
    if invalid_count:
        print(f"Found {invalid_count} invalid geometries; attempting to fix with buffer(0)...")
        gdf["geometry"] = gdf["geometry"].apply(lambda gg: gg.buffer(0) if gg is not None and not gg.is_valid else gg)
        still_invalid = (~gdf.is_valid).sum()
        print("Still invalid after fix:", still_invalid)
        if still_invalid:
            print("You may want to inspect invalid geometries; continuing but some adjacency may be missed.")

    total_bgs = len(gdf)
    print(f"Total block groups in NC (rows): {total_bgs}")

    # Attempt libpysal if available and user hasn't explicitly selected geopandas-only
    neighbors = None
    edges = None
    try_libpysal = True
    if try_libpysal:
        try:
            import importlib
            if importlib.util.find_spec("libpysal") is not None:
                neighbors = build_adjacency_with_libpysal(gdf, geoid_col, adjtype=ADJTYPE)
                # libpysal returns dict geoid->list; build edges from that
                edges = []
                for a, neighs in neighbors.items():
                    for b in neighs:
                        # to avoid duplicates, only append when a < b lexicographically
                        if str(a) < str(b):
                            edges.append((str(a), str(b)))
                # adjacency dict already present; ensure all keys exist
                neighbors = {str(k): [str(x) for x in v] for k, v in neighbors.items()}
                print("libpysal adjacency built. Nodes with neighbors:", len(neighbors))
        except Exception as e:
            print("libpysal path failed or not installed:", e)
            neighbors = None
            edges = None

    # If libpysal not used or failed, fallback to geopandas approach
    if neighbors is None:
        edges, neighbors = build_adjacency_with_geopandas(gdf, geoid_col, adjtype=ADJTYPE)
        print("GeoPandas adjacency built. Nodes with neighbors:", len(neighbors))

    # Save edge list CSV
    edges_df = pd.DataFrame(edges, columns=["source", "target"])
    edges_df.to_csv(EDGE_CSV, index=False)
    print("Saved edge list to", EDGE_CSV, "rows:", len(edges_df))

    # Save adjacency JSON
    with open(ADJ_JSON, "w") as f:
        json.dump(neighbors, f)
    print("Saved adjacency JSON to", ADJ_JSON, "nodes:", len(neighbors))

    print("Done. Summary:")
    print("  - total block groups:", total_bgs)
    print("  - nodes with >=1 neighbor:", len(neighbors))
    print("  - total edges recorded:", len(edges))
    print("  (adjacency type:", ADJTYPE, ")")

if __name__ == "__main__":
    main()
