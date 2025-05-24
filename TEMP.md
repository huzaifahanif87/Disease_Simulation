# Infectious Disease Spread Simulation
## KD-Tree Optimized Graph-Based Modeling

## Outline
1. Introduction
2. System Architecture
3. Algorithmic Optimizations
4. Model Implementation
5. Results & Conclusions

---

## 1. Introduction

- Real-time simulation of disease spread through social interactions
- Graph-based approach modeling human connections and proximity
- Optimized using KD-trees for efficient spatial queries
- Goal: Create realistic model while maintaining computational efficiency

[SCREENSHOT: Simulation showing healthy (green), infected (red), quarantined (purple), and recovered (blue) individuals]

---

## 2. System Architecture

### Components:
1. **Graph Model**: Social network with family, social, and random connections
2. **Spatial Engine**: KD-tree optimized position tracking 
3. **Disease Model**: State-based infection logic
4. **Visualization**: Real-time animation and statistics

### Disease States:
- Healthy → Infected → Detected → Recovered
- Each state transition follows probabilistic rules

[SCREENSHOT: Component interaction diagram]

---

## 3. Algorithmic Optimizations

### Challenge: Performance Bottleneck
- Initial proximity checking: O(n²) complexity
- Quadratic scaling made large simulations impractical

### Solution: KD-Tree Spatial Partitioning
- Reduced proximity queries from O(n²) to O(n log n)
- Enables efficient radius-based neighbor finding

```python
# Key optimization in movement.py
def update_positions(G, positions, velocities, recovered):
    # Create KD-Tree for efficient spatial queries
    node_list = list(G.nodes())
    pos_array = np.array([positions[n] for n in node_list])
    tree = KDTree(pos_array)
    
    # Find nearby nodes in O(log n) time instead of O(n)
    nearby_idxs = tree.query_ball_point(pos, repulsion_radius)
```

```python
# Key optimization in infection.py
def update_infection(G, positions, infected, ...):
    # Build KDTree for fast radius queries
    pos_array = np.array([positions[n] for n in all_nodes])
    tree = KDTree(pos_array)

    # Query all neighbors within infection radius - O(log n)
    neighbors = tree.query_ball_point(pos, INFECTION_RADIUS)
```

---

## 4. Model Implementation

### Social Structure:
- Family connections (high infection probability: 15%)
- Social connections (medium probability: 5%)
- Proximity-based transmission within 10 units

### Infection & Recovery Logic:
- Time-based recovery (23 simulated hours)
- Delayed detection (4-6 days)
- Quarantine option for detected cases

[SCREENSHOT: Visualization showing infection spread network patterns]

---

## 5. Results & Conclusions

### Experimental Observations:
- Baseline (No intervention): Rapid spread through ~80% of population
- With quarantine: Moderate reduction in infections
- With social distancing (increased repulsion): Significant reduction

### Key Findings:
- KD-tree optimization reduced complexity from O(n²) to O(n log n)
- Enabled simulation of larger populations (300+ individuals)
- Social distancing more effective than reactive quarantine

[SCREENSHOT: Comparison graph showing infection curves under different scenarios]

---

### Thank You!

[SCREENSHOT: Final simulation state showing disease progression]
