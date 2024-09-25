import matplotlib.pyplot as plt
import numpy as np

def plot_loxodromes():
    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Number of points where rhumb lines converge
    num_points = 8  # Typically 8 or 16 points in traditional maps
    angles_per_rose = np.linspace(0, 2 * np.pi, 32, endpoint=False)  # 32 cardinal directions

    # Plot loxodromes from each point
    for i in range(num_points):
        # Center of each "compass rose"
        angle = i * (2 * np.pi / num_points)
        x_center = np.cos(angle)
        y_center = np.sin(angle)

        # Plot lines radiating from this center in all 32 directions
        for angle in angles_per_rose:
            # Draw a line for each direction
            x_end = x_center + np.cos(angle) * 4  # Line extended length
            y_end = y_center + np.sin(angle) * 4

            ax.plot([x_center, x_end], [y_center, y_end], color='black', linewidth=0.7)

    # Set the plot limits to frame everything tightly
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)

    # Hide axes and grid
    ax.set_axis_off()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    plot_loxodromes()
