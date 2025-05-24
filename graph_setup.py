#graph_setup.py
#nlogn
import networkx as nx
import numpy as np
import random
from constants import *
import itertools

def setup_graph():
    G = nx.Graph()
    families = []
    positions = {}
    velocities = {}

    node_idx = 0
    for _ in range(NUM_FAMILIES):
        family = []
        for _ in range(FAMILY_SIZE):
            G.add_node(node_idx)
            family.append(node_idx)
            positions[node_idx] = np.random.uniform(-VIEW_LIMIT, VIEW_LIMIT, 2)
            velocities[node_idx] = np.random.uniform(-1, 1, 2)
            node_idx += 1
        families.append(family)

    # Add intra-family edges (still O(n), where n is number of nodes)
    for family in families:
        for i in family:
            for j in family:
                if i != j:
                    G.add_edge(i, j, type='family')

    # Efficient cross-family edges
    all_nodes = list(G.nodes)
    num_cross_links = int(len(all_nodes) * np.log(len(all_nodes)))  # ≈ n log n

    for _ in range(num_cross_links):
        i, j = random.sample(all_nodes, 2)
        if not G.has_edge(i, j):
            G.add_edge(i, j, type='social')

    return G, families, positions, velocities
