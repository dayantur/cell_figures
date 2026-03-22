import numpy as np
import matplotlib.pyplot as plt
import math
import os

# Define the dendrogram types and flips
type_den = ["Phylogenetic", "MFPT"]
flip = ["2flip", "3flip", "4flip"]  # Include "4flip"
###delta_reference = 328  # Use 328 for normalization
delta_reference = 378  # Use 328 for normalization

# Set figure size
plt.rcParams['figure.figsize'] = [13, 5]

# Directory containing the delta distances
data_dir_123 = "./outputs/DeltaAndFlips/"
data_dir_4 = "./outputs/DeltaAndFlips/QuadrupleFlip/"

# Loop through each dendrogram type and flip type
for dendro_type in type_den:
    for flip_type in flip:
        dataset = []

        # File path for the current flip and dendrogram type
        if flip_type == "2flip" or flip_type == "3flip":
            file_path = os.path.join(data_dir_123, f"{flip_type}_{dendro_type}_deltadistances.txt")
        else:
            file_path = os.path.join(data_dir_4, f"{flip_type}_{dendro_type}_deltadistances.txt")
        
        try:
            # Load the dataset from the file and normalize by delta_reference
            with open(file_path, "r") as data_file:
                dataset = [float(line.strip()) / delta_reference for line in data_file]
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue

        # Determine the number of bins for the histogram
        if flip_type == "2flip":
            bins_evaluated = 12
        elif flip_type == "3flip":
            bins_evaluated = 13
        elif flip_type == "4flip":
            bins_evaluated = 15

        # Calculate the histogram
        counts, bin_edges = np.histogram(dataset, bins=bins_evaluated, density=True)
        pdf = counts / sum(counts)

        # Plot the PDF with different styles based on flip and dendrogram type
        if flip_type == "2flip":
            if dendro_type == "Phylogenetic":
                plt.plot(bin_edges[1:], pdf, label="n=2, PHY", color="black", alpha=0.2)
            else:
                plt.plot(bin_edges[1:], pdf, label="n=2, MFPT", color="black", linestyle='dashed', alpha=0.2)
        elif flip_type == "3flip":
            if dendro_type == "Phylogenetic":
                plt.plot(bin_edges[1:], pdf, label="n=3, PHY", color="black", alpha=0.6)
            else:
                plt.plot(bin_edges[1:], pdf, label="n=3, MFPT", color="black", linestyle='dashed', alpha=0.6)
        elif flip_type == "4flip":
            if dendro_type == "Phylogenetic":
                plt.plot(bin_edges[1:], pdf, label="n=4, PHY", color="black", alpha=1)
            else:
                plt.plot(bin_edges[1:], pdf, label="n=4, MFPT", color="black", linestyle='dashed', alpha=1)

# Add the vertical line for Δ(PHY, MFPT) normalized
plt.axvline(x=1, linewidth=3, color="red", label=r"$\Delta=\Delta(PHY, MFPT)$")
plt.legend(fontsize=18)

# Add text annotation in the top-right corner
plt.text(
    1.05, 0.28,  # Coordinates for the text
    f"$\\Delta$(PHY, MFPT) = {delta_reference}", 
    fontsize=15,
    color="black"
)

# Configure plot aesthetics
plt.title("")
plt.ylim(0, 0.3)
plt.xlabel(r"$\Delta / \Delta(PHY,MFPT)$", fontsize=25)
plt.ylabel(r"$P(\Delta / \Delta(PHY,MFPT))$", fontsize=25)
plt.tight_layout()
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

# Save the plot
output_path = "./generatedfigures/FigS3.pdf"
plt.savefig(output_path)
print(f"Plot saved to {output_path}")

# Display the plot
plt.show()
