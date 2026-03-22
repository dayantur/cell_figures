import os
import matplotlib.pyplot as plt
import numpy as np

# Define constants
data_dir = "./outputs/Resilience/"
types_attacks = ["rnd", "egm"]  # Attack types
scales = ["normal", "log"]     # Scale types

all_plants = ["Arabidopsis", "Asplenium", "Brachypodium", "Barley", "Isoetes", "Lemna", "Lilium", 
              "Marislea", "Selaginella", "Sweetpea", "Switchgrass", "Tomato", "Triticum", "Brassica"]

x_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]  # Percentages as fractions

colors = ["red", "orange", "yellow", "lightgreen", "green", "darkgreen", "turquoise", "blue", 
          "purple", "violet", "magenta", "pink", "grey", "darkred"]

dot_size = 150  # Match dot size from old code

# Create the figure and axes
fig, axs = plt.subplots(2, 2, figsize=(14, 12))
fig.tight_layout(pad=6)

# Function to process data for a plant and attack type
def load_resilience_data(plant, attack):
    file_path = os.path.join(data_dir, f"{plant}_{attack}_resilience.txt")
    if not os.path.exists(file_path):
        print(f"Warning: File not found for {plant} with {attack}. Skipping.")
        return None
    resilience_values = []
    with open(file_path, "r") as f:
        for line in f:
            _, value = line.split(":")
            resilience_values.append(float(value.strip()))
    return resilience_values

# Plot data
for i, attack in enumerate(types_attacks):
    for j, scale in enumerate(scales):
        ax = axs[i, j]
        for q, plant in enumerate(all_plants):
            y_values = load_resilience_data(plant, attack)
            if y_values is not None:
                ax.scatter(x_values, y_values, s=dot_size, color=colors[q], alpha=0.7, label=plant)
                ax.plot(x_values, y_values, '-', color=colors[q], alpha=0.5, linewidth=10)
        ax.set_xlabel("p", fontsize=14)
        if scale == "log":
            ax.set_yscale("log")
            ax.set_ylabel(r"log($\rho$)", fontsize=14)
        else:
            ax.set_ylabel(r"$\rho$", fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)

        # Add annotation for RND and EGM
        if i == 0:  # First row
            ax.text(0.95, 0.95, "RND", transform=ax.transAxes, fontsize=16, fontweight='bold', ha='right', va='top')
        elif i == 1:  # Second row
            ax.text(0.95, 0.95, "EGM", transform=ax.transAxes, fontsize=16, fontweight='bold', ha='right', va='top')

# Save and display the plot
plt.savefig("./generatedfigures/FigS6.pdf", bbox_inches="tight", dpi=300)
plt.show()
