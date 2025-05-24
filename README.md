# 🦠 Infectious Disease Spread Simulation

This project simulates the spread of an infectious disease (like COVID-19) through a synthetic social network using **Python**, **NetworkX**, **matplotlib**, and **KDTree** for efficient spatial queries. The simulation models real-world dynamics like infection based on proximity, social structure tiers, recovery, and reinfection.

## 🚀 Features

- 👪 **Three-Tier Social Structure**: Nodes (individuals) belong to:
  - **Family Tier**: High infection probability (15%)
  - **Cross-Family Tier**: Medium infection probability (5%)
  - **Social Tier**: General interactions with moderate probability (3%)

- 📍 **Location-Based Infection**:
  - Infection spreads only within a specified proximity using KDTree (`< 10 units`)
  - chance of infection only if susceptible within range

- 🔄 **Dynamic Movement**:
  - Nodes move based on a physics-inspired force-directed layout
  - Initial velocities also added to make more realistic movement

- ⏱ **Time-Based Simulation**:
  - Recovery occurs 23 hrs after infection (9-10 frames)
  - Reinfection chance is very low (0.1%)

- 📊 **Live Visualization**:
  - Animated simulation using `matplotlib.animation`
  - Real-time line graph of infection, recovery, and detection statistics

---

## 📂 Project Structure
```plaintext
.
├── constants.py       # Simulation constants (timing, probabilities)
├── graph_utils.py     # Social graph generation logic
├── movement.py        # Movement logic for individuals
├── infection.py       # Infection update logic
├── plot_update.py     # Animation frame updates & graph rendering
├── simulation.py      # Main runner: puts everything together
└── README.md          # Documentation (this file)
```

---

## 🧪 Installation & Running

### ✅ Requirements

- Python 3.7+
- Install required packages:

```bash
pip install matplotlib networkx numpy scipy
```
### ▶️ Run the Simulation
```bash
pyton3 main.py
```
