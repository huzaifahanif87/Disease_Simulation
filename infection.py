# infection.py
#nlogn

import numpy as np
import random
from constants import INFECTION_PROBABILITY, CROSS_FAMILY_PROBABILITY, SOCIAL_INTERACTION_PROBABILITY, INFECTION_RADIUS, RECOVERY_FRAMES, DETECTION_DELAY_DAYS, FRAMES_PER_DAY, VIEW_LIMIT
from scipy.spatial import KDTree  # 🚀 Accelerates spatial queries

def infect_initial_nodes(G):
    infected = set()
    detected_infected = set()
    recovered = set()
    infection_timers = {}
    detection_timers = {}

    initial_infected = random.sample(list(G.nodes), 3)
    for node in initial_infected:
        infected.add(node)
        infection_timers[node] = 0
        detection_timers[node] = random.choice(DETECTION_DELAY_DAYS) * FRAMES_PER_DAY

    return infected, detected_infected, recovered, infection_timers, detection_timers


def update_infection(G, positions, infected, detected_infected, recovered,
                     infection_timers, detection_timers, velocities=None):

    new_infected = set()
    all_nodes = list(G.nodes)
    pos_array = np.array([positions[n] for n in all_nodes])
    index_map = {n: i for i, n in enumerate(all_nodes)}

    # Build KDTree for fast radius queries
    tree = KDTree(pos_array)

    for node in infected:
        if node in recovered:
            continue
        idx = index_map[node]
        pos = pos_array[idx]
        
        # Query all neighbors within infection radius
        neighbors = tree.query_ball_point(pos, INFECTION_RADIUS)

        for nbr_idx in neighbors:
            nbr = all_nodes[nbr_idx]
            if nbr == node or nbr in infected or nbr in recovered:
                continue

            if G.has_edge(node, nbr):
                edge_type = G[node][nbr].get('type', 'social')
            else:
                edge_type = 'social'

            prob = INFECTION_PROBABILITY if edge_type == 'family' else CROSS_FAMILY_PROBABILITY
            if random.random() < prob:
                new_infected.add(nbr)

    for node in new_infected:
        infected.add(node)
        infection_timers[node] = 0
        detection_timers[node] = random.choice(DETECTION_DELAY_DAYS) * FRAMES_PER_DAY

    to_recover = []
    for node in list(infected):
        detection_timers[node] -= 1
        infection_timers[node] += 1

        if detection_timers[node] <= 0 and node not in detected_infected:
            detected_infected.add(node)

        if infection_timers[node] >= RECOVERY_FRAMES:
            to_recover.append(node)

    for node in to_recover:
        infected.remove(node)
        detected_infected.discard(node)
        recovered.add(node)
        infection_timers.pop(node)
        detection_timers.pop(node)

        positions[node] = np.random.uniform(-VIEW_LIMIT * 0.8, VIEW_LIMIT * 0.8, 2)

        if velocities is not None and node in velocities:
            velocities[node] = np.random.uniform(-2.0, 2.0, 2)

    return infected, detected_infected, recovered, infection_timers, detection_timers
