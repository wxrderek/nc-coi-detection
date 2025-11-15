import pandas as pd
import numpy as np

class Node:
    def __init__(self, GOID):
        self.GOID = GOID
        self.neighbors = {}

GOIDs = set([])
nodes = []

adj_data = np.load("../Adjacency/nc-bg-adjacency.npz")

print(adj_data.data)
