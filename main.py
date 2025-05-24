#O(2000·(n + m) + 2000²)
#main.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
from graph_setup import setup_graph
from infection import infect_initial_nodes
from plot_update import update, toggle_edges


# Setup graph and initial infection state
G, families, positions, velocities = setup_graph()
infected, detected_infected, recovered, infection_timers, detection_timers = infect_initial_nodes(G)

# Quarantine and node colors placeholders
quarantine = set()
quarantine_area = [10, 10]  # Center of quarantine zone
node_colors = {}  # Colors will be dynamically updated in each frame

# Setup figure and subplots
fig = plt.figure(figsize=(16, 9))
gs = gridspec.GridSpec(2, 2, width_ratios=[7, 3], height_ratios=[1, 1], wspace=0.1, hspace=0.3)

ax_simulation = fig.add_subplot(gs[:, 0])
ax_graph = fig.add_subplot(gs[0, 1])
ax_text = fig.add_subplot(gs[1, 1])
ax_text.axis('off')

# Capture keyboard events
fig.canvas.mpl_connect('key_press_event', toggle_edges)

# Frame update logic
def frame_update(frame):
    global infected, detected_infected, recovered, infection_timers, detection_timers

    infected, detected_infected, recovered, infection_timers, detection_timers = update(
        frame, G, positions, velocities, infected, detected_infected, recovered,
        infection_timers, detection_timers, quarantine, quarantine_area, node_colors,
        ax_simulation, ax_graph, ax_text
    )

ani = animation.FuncAnimation(fig, frame_update, frames=2000, interval=20, repeat=False)
plt.show()




