
# movement.py
# O(n log n)
import numpy as np
from constants import VIEW_LIMIT, TIME_STEP
from scipy.spatial import KDTree

def update_positions(G, positions, velocities, recovered):
    max_speed = 2.0
    friction = 0.9
    noise_strength = 0.5
    repulsion_radius = 8
    repulsion_strength = 1
    spring_strength = 0.005

    node_list = list(G.nodes())
    pos_array = np.array([positions[n] for n in node_list])
    index_map = {n: i for i, n in enumerate(node_list)}
    tree = KDTree(pos_array)

    for node in G.nodes():
        idx = index_map[node]
        force = np.zeros(2)
        pos = positions[node]

        # Spring attraction to neighbors (like force-directed graph)
        if node not in recovered:
            for neighbor in G.neighbors(node):
                direction = positions[neighbor] - pos
                distance = np.linalg.norm(direction)
                if distance > 0:
                    force += spring_strength * direction / distance

        # Efficient Repulsion using KDTree
        nearby_idxs = tree.query_ball_point(pos, repulsion_radius)
        for nbr_idx in nearby_idxs:
            other = node_list[nbr_idx]
            if other == node:
                continue
            direction = pos - positions[other]
            distance = np.linalg.norm(direction)
            if distance > 0:
                push = direction / distance
                correction = (repulsion_radius - distance) * repulsion_strength
                force += push * correction

        # Random noise
        noise = np.random.uniform(-1, 1, 2) * (noise_strength * (2.0 if node in recovered else 1.0))
        force += noise

        # Update velocity and clamp
        velocities[node] += force
        velocities[node] *= friction
        speed = np.linalg.norm(velocities[node])
        if speed > max_speed:
            velocities[node] = velocities[node] / speed * max_speed

        # Update position
        positions[node] += velocities[node] * TIME_STEP

        # Boundary bounce
        for dim in [0, 1]:
            if positions[node][dim] < -VIEW_LIMIT or positions[node][dim] > VIEW_LIMIT:
                velocities[node][dim] *= -1
                positions[node][dim] = np.clip(positions[node][dim], -VIEW_LIMIT, VIEW_LIMIT)

