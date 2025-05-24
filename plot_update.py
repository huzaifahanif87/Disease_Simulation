# # plot_update.py
# #O(n + m + f)


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from constants import *
from movement import update_positions
from infection import update_infection
quarantine_mode = False
show_edges = True

def toggle_edges(event):
    global show_edges, quarantine_mode
    if event.key == 'e':
        show_edges = not show_edges
    elif event.key == 'g':
        quarantine_mode = True

# Tracking stats
infection_counts = []
recovery_counts = []
susceptible_counts = []
detected_counts = []
frames_history = []
# New tracking for infection rates
growth_rate_values = []  # Renamed from r1_values
reproduction_values = []  # Renamed from r2_values
standard_r_values = []   # Standard R tracking
# Number of frames for rate calculation (modifiable)
rate_frame_window = 1

# For standard R calculation
total_new_infections = 0
total_infectious_frames = 0

def update(num, G, positions, velocities, infected, detected_infected, recovered,
           infection_timers, detection_timers, quarantine, quarantine_area, node_colors,
           ax_sim, ax_graph, ax_text):
    
    global infection_counts, recovery_counts, susceptible_counts, frames_history
    global growth_rate_values, reproduction_values, standard_r_values
    global total_new_infections, total_infectious_frames

    # Clear axes for fresh draw
    ax_sim.clear()
    ax_graph.clear()
    ax_text.clear()

    infected, detected_infected, recovered, infection_timers, detection_timers = update_infection(
    G, positions, infected, detected_infected, recovered,infection_timers, detection_timers, velocities
)

        # Update movement
    update_positions(G, positions, velocities,recovered)

    # Quarantine logic: detected ones move to quarantine zone
    quarantine_center = np.array([150, 80])
    quarantine_size = 30

    if quarantine_mode:
        for node in detected_infected:
            jitter = np.random.uniform(-quarantine_size/2, quarantine_size/2, 2)
            positions[node] = quarantine_center + jitter
            velocities[node] *= 0.1  # Slow down quarantined nodes

    # Camera follow
    all_positions = np.array(list(positions.values()))
    center_of_mass = np.mean(all_positions, axis=0)
    ax_sim.set_xlim(-120,180)  # big enough to include people and quarantine area
    ax_sim.set_ylim(-120, 120)
    ax_sim.set_title(f"Simulation (Frame {num}) | Press 'e' to toggle edges and 'g' to quarantine detected infected")

    # Draw quarantine area
    rect = plt.Rectangle((120,60), 50, 40,
                         linewidth=2, edgecolor='purple', facecolor='none', linestyle='--')
    ax_sim.add_patch(rect)
    ax_sim.text(quarantine_center[0], quarantine_center[1] + quarantine_size + 5,
                '🩺 Quarantine Zone', ha='center', fontsize=10, color='purple')

    # Draw nodes
    colors = []
    for node in G.nodes():
        if node in detected_infected:
            colors.append('purple')
        elif node in infected:
            colors.append('red')
        elif node in recovered:
            colors.append('blue')
        else:
            colors.append('green')

    nx.draw_networkx_nodes(G, positions, node_color=colors, node_size=30, ax=ax_sim)
    if show_edges:
        nx.draw_networkx_edges(G, positions, alpha=0.1, ax=ax_sim)

    # Update stats
    detected_count = len(detected_infected)
    infected_count = len(infected)-len(detected_infected)
    recovered_count = len(recovered)
    susceptible_count = len(G.nodes) - infected_count - recovered_count

    # Store current total infected count (detected + undetected)
    current_total_infected = infected_count + detected_count
    
    # Calculate new infections in this frame
    if len(infection_counts) > 0:
        previous_total = infection_counts[-1] + detected_counts[-1]
        new_infections = current_total_infected - previous_total
        if new_infections > 0:
            total_new_infections += new_infections
    else:
        new_infections = current_total_infected  # Initial infected count
        total_new_infections = new_infections
    
    # Count infectious person-frames (for standard R)
    total_infectious_frames += infected_count  # Only undetected can spread

    infection_counts.append(infected_count)
    recovery_counts.append(recovered_count)
    susceptible_counts.append(susceptible_count)
    detected_counts.append(detected_count)
    frames_history.append(num)
    
    # Calculate infection rates
    growth_rate = 0  # Renamed from r1
    reproduction_number = 0  # Renamed from r2
    standard_r = 0
    
    if len(infection_counts) > rate_frame_window:
        # For growth rate calculation, consider change in total infected
        previous_total_infected = infection_counts[-rate_frame_window-1] + detected_counts[-rate_frame_window-1]
        infected_diff = current_total_infected - previous_total_infected
        
        # Growth Rate = change in infected / time window
        growth_rate = infected_diff / rate_frame_window
        
        previous_undetected = infection_counts[-rate_frame_window-1]
        if previous_undetected > 0:
            reproduction_number = infected_diff / (previous_undetected * rate_frame_window)
    
    # Calculate standard R (average reproduction number over the entire simulation)
    if total_infectious_frames > 0:
        standard_r = total_new_infections / total_infectious_frames
    
    growth_rate_values.append(growth_rate)
    reproduction_values.append(reproduction_number)
    standard_r_values.append(standard_r)

    ax_graph.plot(frames_history, detected_counts, color='purple', label='Detected & Quarantined')
    ax_graph.plot(frames_history, infection_counts, color='red', label='Infected')
    ax_graph.plot(frames_history, recovery_counts, color='blue', label='Recovered')
    ax_graph.plot(frames_history, susceptible_counts, color='green', label='Susceptible')
    ax_graph.set_title("Infection & Recovery Over Time")
    ax_graph.set_xlabel("Frames")
    ax_graph.set_ylabel("Count")
    # ax_graph.legend()

    ax_text.set_title("Current Stats")
    ax_text.text(0.1, 0.8, f" Infected: {infected_count}", fontsize=12, color='red')
    ax_text.text(0.1, 0.6, f" Detected: {len(detected_infected)}", fontsize=12, color='purple')
    ax_text.text(0.1, 0.4, f" Recovered: {recovered_count}", fontsize=12, color='blue')
    ax_text.text(0.1, 0.2, f" Susceptible: {susceptible_count}", fontsize=12, color='green')
    
    # Display infection rates with more descriptive names
    ax_text.text(0.5, 0.8, f"Growth Rate: {growth_rate:.3f}", fontsize=10, color='orange')
    ax_text.text(0.5, 0.6, f"R (Reproduction №): {reproduction_number:.3f}", fontsize=10, color='orange')
   # ax_text.text(0.5, 0.4, f"Standard R: {standard_r:.3f}", fontsize=10, color='orange')

    return infected, detected_infected, recovered, infection_timers, detection_timers