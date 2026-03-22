#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 1. Load the KS size and treel data
ks_size_file = "./outputs/KSStatistics/KS_Size.csv"
ks_treel_file = "./outputs/KSStatistics/KS_Treel.csv"

ks_size_data = pd.read_csv(ks_size_file)
ks_treel_data = pd.read_csv(ks_treel_file)

# Merge the two datasets on species
data = pd.merge(ks_size_data, ks_treel_data, on="Species", suffixes=("_size", "_treel"))

# Shorten species names to the first three letters
data["Short_Name"] = data["Species"].str[:4]

# Sort species by KS statistics for size and treelikeness
ranked_by_size = data.sort_values(by="KS_Statistic_size", ascending=False)["Short_Name"].tolist()
ranked_by_treel = data.sort_values(by="KS_Statistic_treel", ascending=False)["Short_Name"].tolist()

print("Ranked by Size KS:", ranked_by_size)
print("Ranked by Treelikeness KS:", ranked_by_treel)

# 2. Plot Ranked Lists with Ordered Colour Mapping
plt.figure(figsize=(12, 3))

# Assign colours based on the size ranking
colors = plt.cm.plasma(np.linspace(0, 1, len(ranked_by_size)))  # Gradient colouring
species_to_color = {species: color for species, color in zip(ranked_by_size, colors)}  # Map size ranking to colours

# Adjust vertical positioning
size_ks_y = 0.7  # Adjusted Y-coordinate for Size KS
treel_ks_y = 0.4  # Adjusted Y-coordinate for Treelikeness KS
text_fontsize = 16  # Enlarged font size for species names

# Plot rankings for size KS
for i, name in enumerate(ranked_by_size):
    plt.text(i + 0.5, size_ks_y, name, ha='center', va='center', fontsize=text_fontsize, color=species_to_color[name], weight='bold', style='italic')

# Draw a black rectangle around the list for size KS
plt.plot([0, len(ranked_by_size)], [size_ks_y + 0.1, size_ks_y + 0.1], color="black", lw=2)  # Top border
plt.plot([0, len(ranked_by_size)], [size_ks_y - 0.1, size_ks_y - 0.1], color="black", lw=2)  # Bottom border
plt.plot([0, 0], [size_ks_y - 0.1, size_ks_y + 0.1], color="black", lw=2)  # Left border
plt.plot([len(ranked_by_size), len(ranked_by_size)], [size_ks_y - 0.1, size_ks_y + 0.1], color="black", lw=2)  # Right border

# Plot rankings for treelikeness KS
for i, name in enumerate(ranked_by_treel):
    plt.text(i + 0.5, treel_ks_y, name, ha='center', va='center', fontsize=text_fontsize, color=species_to_color[name], weight='bold', style='italic')

# Draw a black rectangle around the list for treelikeness KS
plt.plot([0, len(ranked_by_treel)], [treel_ks_y + 0.1, treel_ks_y + 0.1], color="black", lw=2)  # Top border
plt.plot([0, len(ranked_by_treel)], [treel_ks_y - 0.1, treel_ks_y - 0.1], color="black", lw=2)  # Bottom border
plt.plot([0, 0], [treel_ks_y - 0.1, treel_ks_y + 0.1], color="black", lw=2)  # Left border
plt.plot([len(ranked_by_treel), len(ranked_by_treel)], [treel_ks_y - 0.1, treel_ks_y + 0.1], color="black", lw=2)  # Right border

# Remove axes and tidy up
plt.axis('off')
plt.tight_layout()

# Save the figure as a PDF
output_dir = "./generatedfigures/"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
output_file = os.path.join(output_dir, "Fig2D.pdf")
plt.savefig(output_file, format="pdf", bbox_inches="tight")

print(f"Figure saved as PDF: {output_file}")

# Show the plot
plt.show()

from scipy.stats import kendalltau

# Convert rankings into sequences of numbers
# Map species to their ranks in size and treel rankings
size_ranks = {species: rank for rank, species in enumerate(ranked_by_size, start=1)}
treel_ranks = {species: rank for rank, species in enumerate(ranked_by_treel, start=1)}

# Create numeric sequences for the rankings
size_numeric = [size_ranks[species] for species in ranked_by_size]
treel_numeric = [size_ranks[species] for species in ranked_by_treel]  # Note: order from treel ranking

# Calculate Kendall's Tau on the numeric sequences
kt_numeric, p_numeric = kendalltau(size_numeric, treel_numeric)

print(f"Kendall's Tau: {kt_numeric:.2f}, p-value: {p_numeric}")


