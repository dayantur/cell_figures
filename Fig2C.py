#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
import pandas as pd

# 1. Parameters and File Paths
colour = "green"
ks_size_file = "./outputs/KSStatistics/KS_Size.csv"
ks_treel_file = "./outputs/KSStatistics/KS_Treel.csv"

# 2. Load Data
# Load KS Size data
ks_size_data = pd.read_csv(ks_size_file)
ks_treel_data = pd.read_csv(ks_treel_file)

# Merge KS size and treel data on species
data = pd.merge(ks_size_data, ks_treel_data, on="Species", suffixes=("_size", "_treel"))

# Extract data for plotting
x = data["KS_Statistic_size"]  # KS size on x-axis
y = data["KS_Statistic_treel"]  # KS treel on y-axis
annotations = data["Species"]  # Species names for annotation

# 3. Plotting
plt.figure(figsize=(8, 6))

# Scatter plot
plt.scatter(x, y, s=80, c="black", alpha=0.8)

# Adjust annotations to avoid overlap with points
texts = [plt.text(x[i] + 0.005, y[i] + 0.005, annotations[i], fontsize=12, ha='center', va='bottom') for i in range(len(x))]
adjust_text(texts, arrowprops=None)

# Labels and limits
plt.xlabel(r"Size KS ($\omega_{S}$)", fontsize=14)
plt.ylabel(r"Stringiness KS ($\omega_{\sigma}$)", fontsize=14)
plt.xlim(0, 0.8)
plt.ylim(0, 0.8)

# Remove the grid and customize axis visibility
plt.grid(False)  # Ensure no grid is displayed
plt.gca().spines['top'].set_visible(False)  # Hide the top spine
plt.gca().spines['right'].set_visible(False)  # Hide the right spine
plt.gca().spines['bottom'].set_color('black')  # Set bottom spine to black
plt.gca().spines['left'].set_color('black')  # Set left spine to black

# Set ticks and tick labels for clarity
plt.tick_params(axis="x", colors="black")  # Set x-axis ticks to black
plt.tick_params(axis="y", colors="black")  # Set y-axis ticks to black

# Adjust layout
plt.tight_layout()

# Save the figure to a PDF file
output_pdf = "./generatedfigures/Fig2C.pdf"
plt.savefig(output_pdf, format="pdf", bbox_inches="tight")

print(f"Plot saved as PDF: {output_pdf}")

# Show plot
plt.show()

