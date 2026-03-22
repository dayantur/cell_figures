import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster import hierarchy
from matplotlib import pyplot as plt

# 1. Upload the CSV
input_csv = "./dendros/renamed_evolutionary_matrix.csv"  # Replace with your CSV path
df = pd.read_csv(input_csv, header=None)

# 2. Convert the CSV entries into a distance matrix (distance_matrix_np)
# Replace NaN values with 0 for the calculations
distance_matrix = df.iloc[1:, 1:].replace(np.nan, 0).astype(float).values

# Find the maximum numerical value in the matrix
max_value = np.nanmax(distance_matrix)

# Normalize the matrix by dividing all numerical values by the maximum value
distance_matrix_np = distance_matrix / max_value

# Extract the upper triangular matrix (excluding the diagonal)
upper_triangle = distance_matrix_np[np.triu_indices(len(distance_matrix), k=1)]

# Load labels for dendrogram
labels = []
with open("./dendros/renaming_list.txt") as fp:
    labels = [line.strip() for line in fp]

# Generate the dendrogram
linkage_method = 'average'
Z = hierarchy.linkage(upper_triangle, method=linkage_method)

plt.figure(figsize=(7, 5))
plt.title("Phylogenetic Tree", fontweight="bold")
hierarchy.dendrogram(
    Z,
    orientation='left',
    labels=labels,
    color_threshold=0.53,
    above_threshold_color='C0',
    leaf_font_size=12,
    show_leaf_counts=True
)

# Save the figure
output_path = "./generatedfigures/Fig3C.pdf"
plt.savefig(output_path, bbox_inches='tight', dpi=1000)
plt.show()

print(f"Phylogenetic dendrogram saved to {output_path}")
