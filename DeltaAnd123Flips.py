import numpy as np
from scipy.cluster import hierarchy
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os

# 1. Upload the CSV
input_csv = "./dendros/renamed_evolutionary_matrix.csv"  # Remember to add here the new species!
df = pd.read_csv(input_csv, header=None)

# 2. Convert the CSV entries into a distance matrix (distance_matrix_np)
distance_matrix = df.iloc[1:, 1:].fillna(0).astype(float).values

# Find the maximum numerical value in the matrix
max_value = np.max(distance_matrix)

# Normalize the matrix by dividing all numerical values by the maximum value
distance_matrix_np = distance_matrix / max_value

# Extract the upper triangular matrix (excluding the diagonal)
upper_triangle = distance_matrix_np[np.triu_indices(len(distance_matrix), k=1)]
upper_cleaned_1 = upper_triangle  # Use consistently for linkage calculation

# Load labels for dendrogram
labels_1 = []
with open("./dendros/renaming_list.txt") as fp: #Remember to add here the new species!
    labels_1 = [line.strip() for line in fp]

# Generate the first dendrogram
link_1 = 'average'
Z1 = hierarchy.linkage(np.array(upper_cleaned_1), link_1)

plt.figure()
plt.title("Phylogenetic", fontweight="bold")
dn_1 = hierarchy.dendrogram(
    Z1,
    p=30,
    truncate_mode=None,
    color_threshold=1.2,
    get_leaves=True,
    orientation='left',
    labels=labels_1,
    count_sort=False,
    distance_sort=False,
    show_leaf_counts=True,
    no_plot=False,
    no_labels=False,
    leaf_font_size=None,
    leaf_rotation=None,
    leaf_label_func=None,
    show_contracted=False,
    link_color_func=None,
    ax=None,
    above_threshold_color='C0'
)
#plt.show()

# Extract graph and shortest paths for the first dendrogram
root_1, nodelist_1 = hierarchy.to_tree(Z1, rd=True)
G1 = nx.Graph()

# Add nodes and edges from the first dendrogram
for node in nodelist_1:
    left = node.get_left()
    right = node.get_right()
    if left:
        G1.add_edge(node.get_id(), left.get_id())
    if right:
        G1.add_edge(node.get_id(), right.get_id())

# Add labels (leaves only) to the graph
leaf_labels_1 = {n.get_id(): labels_1[i] for i, n in enumerate(nodelist_1) if n.is_leaf()}
spl_1 = dict(nx.all_pairs_shortest_path_length(G1))

# Generate the shortest path distance matrix for the first dendrogram
size_1 = len(labels_1)
distance_matrix_1_shortest = np.full((size_1, size_1), np.inf)

for i in range(size_1):
    for j in range(size_1):
        try:
            distance_matrix_1_shortest[i][j] = spl_1[i][j]
        except KeyError:
            print(f"Warning: No path between {i} and {j}")

# List of species - remember to add here the name of the new species!
species_list = ["Arabidopsis", "Asplenium", "Brachypodium", "Barley", "Isoetes", "Lemna", 
                "Lilium", "Marislea", "Selaginella", "Sweetpea", "Switchgrass", "Tomato", "Triticum", "Brassica"]

# Define the directory containing the saved talfabeta matrices
matrix_dir = "./outputs/TauAlfaBetaMatrices" 

# Load talfabeta matrices from files
talfabeta_matrices = []
for species in species_list:
    file_path = os.path.join(matrix_dir, f"{species}_talfabeta_normalised.txt") #Remember to calculate this for the new species as well!
    try:
        # Load the matrix and append to the list
        matrix = np.loadtxt(file_path, delimiter=" ")
        talfabeta_matrices.append(matrix)
        #print(f"Loaded matrix for {species} from {file_path}")
    except Exception as e:
        print(f"Error loading matrix for {species}: {e}")
        raise

# Initialize matrices for norms
num_species = len(talfabeta_matrices)
norm_one_matrix = np.zeros((num_species, num_species))

# Compute norms between all pairs of matrices
for i in range(num_species):
    current_matrix = talfabeta_matrices[i]

    for j in range(num_species):
        comparison_matrix = talfabeta_matrices[j]
        
        if i != j:  # Skip comparison with itself
            # Compute the difference matrix
            difference_matrix = np.abs(current_matrix - comparison_matrix)

            # Compute Norm-1 (sum of absolute differences)
            norm_one_matrix[i, j] = np.sum(difference_matrix)

# Normalize the Norm-1 matrix
max_value = np.max(norm_one_matrix)
if max_value == 0:
    raise ValueError("Maximum value in Norm-1 matrix is zero, cannot normalize.")
norm_one_matrix_normalized = norm_one_matrix / max_value

# Prepare the upper triangular matrix for dendrogram
upper_triangle = norm_one_matrix_normalized[np.triu_indices(num_species, k=1)]

# Validate and filter the upper_triangle values
if not np.all(np.isfinite(upper_triangle)):
    print("Found non-finite values in the condensed distance matrix. Replacing them with 1e9.")
    upper_triangle = np.nan_to_num(upper_triangle, nan=1e9, posinf=1e9, neginf=1e9)

# Prepare labels for the dendrogram
labels_2 = [species for species in species_list if species != "Equisetum"]  # Exclude "Equisetum"

# Generate the dendrogram
linkage_method = 'average'
linkage_matrix = hierarchy.linkage(upper_triangle, method=linkage_method)

#plt.figure(figsize=(7, 5))
plt.title("MFPT", fontweight="bold")
hierarchy.dendrogram(
    linkage_matrix,
    orientation='left',
    labels=labels_2,
    color_threshold=0.53,
    above_threshold_color='C0',
    leaf_font_size=12,
    show_leaf_counts=True
)

#plt.show()

# Extract the graph structure and compute the shortest path matrix from the dendrogram
root_2, nodelist_2 = hierarchy.to_tree(linkage_matrix, rd=True)
G2 = nx.Graph()

# Add nodes and edges from the dendrogram
for node in nodelist_2:
    left = node.get_left()
    right = node.get_right()
    if left:
        G2.add_edge(node.get_id(), left.get_id())
    if right:
        G2.add_edge(node.get_id(), right.get_id())

# Add labels (leaves only) to the graph
leaf_labels_2 = {n.get_id(): labels_2[i] for i, n in enumerate(nodelist_2) if n.is_leaf()}
spl_2 = dict(nx.all_pairs_shortest_path_length(G2))

# Generate the shortest path distance matrix
####size_2 = len(labels)
size_2 = len(labels_2)
distance_matrix_2_shortest = np.full((size_2, size_2), np.inf)

for i in range(size_2):
    for j in range(size_2):
        try:
            distance_matrix_2_shortest[i][j] = spl_2[i][j]
        except KeyError:
            print(f"Warning: No path between {i} and {j}")
            
# Define the consistent order of species (from species_list)
consistent_order = species_list

# Create a mapping from label to its position in the consistent order
label_to_index = {label: i for i, label in enumerate(consistent_order)}

# Function to reorder a distance matrix to match the consistent order
def reorder_distance_matrix(distance_matrix, current_order, consistent_order):
    size = len(consistent_order)
    reordered_matrix = np.full((size, size), np.inf)

    # Map the current order indices to the consistent order indices
    index_mapping = [label_to_index[label] for label in current_order]

    # Rearrange rows and columns according to the consistent order
    for i, original_i in enumerate(index_mapping):
        for j, original_j in enumerate(index_mapping):
            reordered_matrix[original_i][original_j] = distance_matrix[i][j]

    return reordered_matrix

# Reorder matrices to match the consistent order
distance_matrix_1_aligned = reorder_distance_matrix(distance_matrix_1_shortest, labels_1, consistent_order)
distance_matrix_2_aligned = reorder_distance_matrix(distance_matrix_2_shortest, labels_2, consistent_order)

# Directory to save the matrices
output_dir = "./outputs/DeltaAndFlips/QuadrupleFlip/"

# File paths for the output files
phylogenetic_file = os.path.join(output_dir, "Phylogenetic_originaldistancematrix.txt")
mfpt_file = os.path.join(output_dir, "MFPT_originaldistancematrix.txt")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Save the aligned matrices with integer entries
np.savetxt(phylogenetic_file, distance_matrix_1_aligned.astype(int), fmt="%d", delimiter=" ")
np.savetxt(mfpt_file, distance_matrix_2_aligned.astype(int), fmt="%d", delimiter=" ")

print(f"Aligned distance matrices saved to:\n{phylogenetic_file}\n{mfpt_file}")

import math

# Initialize the sum variable
total_sum = 0.0

# Calculate the sum of the absolute differences between the two aligned matrices - i.e. DELTA
for i in range(len(distance_matrix_1_aligned)):
    for j in range(len(distance_matrix_2_aligned)):
        # Compute the absolute difference for the current cell
        cell_difference = abs(distance_matrix_1_aligned[i][j] - distance_matrix_2_aligned[i][j])
        # Add the difference to the total sum
        total_sum += cell_difference

# Print the results
print("Delta:", total_sum)

# Generate all possible permutations of row-column swaps for the distance matrix (oneflip)
permutations_oneflip = []
matrix_size_oneflip = len(distance_matrix_1_aligned)

for i in range(matrix_size_oneflip):
    for j in range(i + 1, matrix_size_oneflip):
        permutations_oneflip.append([i, j])

# Calculate the distances for each permutation (oneflip)
distance_permutations_oneflip = []

for perm in permutations_oneflip:
    # Create a copy of the matrix for swapping
    permuted_matrix_oneflip = np.copy(distance_matrix_1_aligned)

    # Swap rows and columns
    permuted_matrix_oneflip[[perm[0], perm[1]], :] = permuted_matrix_oneflip[[perm[1], perm[0]], :]
    permuted_matrix_oneflip[:, [perm[0], perm[1]]] = permuted_matrix_oneflip[:, [perm[1], perm[0]]]

    # Calculate the norm difference between the original and permuted matrices
    total_difference_oneflip = 0.0
    for row in range(matrix_size_oneflip):
        for col in range(matrix_size_oneflip):
            cell_difference_oneflip = abs(distance_matrix_1_aligned[row][col] - permuted_matrix_oneflip[row][col])
            total_difference_oneflip += cell_difference_oneflip

    # Store total difference
    distance_permutations_oneflip.append(total_difference_oneflip)

# Generate all possible two-row-column flip permutations for the distance matrix
two_permutations = []
total_permutations = len(permutations_oneflip)

# Generate initial two-permutation pairs
for i in range(total_permutations):
    for j in range(i, total_permutations):
        if i != j:
            two_permutations.append([permutations_oneflip[i], permutations_oneflip[j]])

# Extend the list of two-permutations by adding additional combinations
for perm_pair in two_permutations[:]:  # Iterate over a copy of the list
    if perm_pair[0][0] == perm_pair[1][0]:
        new_pair = [perm_pair[1], perm_pair[0]]
        two_permutations.append(new_pair)
    if perm_pair[0][0] == perm_pair[1][1]:
        new_pair = [perm_pair[1], perm_pair[0]]
        two_permutations.append(new_pair)
    if perm_pair[0][1] == perm_pair[1][0]:
        new_pair = [perm_pair[1], perm_pair[0]]
        two_permutations.append(new_pair)
    if perm_pair[0][1] == perm_pair[1][1]:
        new_pair = [perm_pair[1], perm_pair[0]]
        two_permutations.append(new_pair)

# Calculate the distances for each two-flip permutation
distance_twoflips = []


for perm_pair in two_permutations:
    # Create a copy of the matrix for swapping
    permuted_matrix_twoflip = np.copy(distance_matrix_1_aligned)

    # Apply the first flip
    permuted_matrix_twoflip[[perm_pair[0][0], perm_pair[0][1]], :] = permuted_matrix_twoflip[[perm_pair[0][1], perm_pair[0][0]], :]
    permuted_matrix_twoflip[:, [perm_pair[0][0], perm_pair[0][1]]] = permuted_matrix_twoflip[:, [perm_pair[0][1], perm_pair[0][0]]]

    # Apply the second flip
    permuted_matrix_twoflip[[perm_pair[1][0], perm_pair[1][1]], :] = permuted_matrix_twoflip[[perm_pair[1][1], perm_pair[1][0]], :]
    permuted_matrix_twoflip[:, [perm_pair[1][0], perm_pair[1][1]]] = permuted_matrix_twoflip[:, [perm_pair[1][1], perm_pair[1][0]]]

    # Calculate the norm difference between the original and permuted matrices
    total_difference_twoflip = 0.0
    for row in range(len(distance_matrix_1_aligned)):
        for col in range(len(distance_matrix_1_aligned)):
            cell_difference_twoflip = abs(distance_matrix_1_aligned[row][col] - permuted_matrix_twoflip[row][col])
            total_difference_twoflip += cell_difference_twoflip

    # Store total difference
    distance_twoflips.append(total_difference_twoflip)

# Generate all possible three-row-column flip permutations for the distance matrix
three_permutations = []
total_permutations = len(permutations_oneflip)

# Generate all possible triplets of permutations
for i in range(total_permutations):
    for j in range(total_permutations):
        for k in range(total_permutations):
            triplet = [permutations_oneflip[i], permutations_oneflip[j], permutations_oneflip[k]]
            three_permutations.append(triplet)

# Filter the triplets to ensure no duplicate flips within the triplet
valid_three_permutations = []
for triplet in three_permutations:
    if triplet[0] != triplet[1] and triplet[1] != triplet[2]:
        valid_three_permutations.append(triplet)

# Calculate the distances for each three-flip permutation
distance_threeflips = []

for triplet in valid_three_permutations:
    # Create a copy of the matrix for swapping
    permuted_matrix_threeflip = np.copy(distance_matrix_1_aligned)

    # Apply the first flip
    permuted_matrix_threeflip[[triplet[0][0], triplet[0][1]], :] = permuted_matrix_threeflip[[triplet[0][1], triplet[0][0]], :]
    permuted_matrix_threeflip[:, [triplet[0][0], triplet[0][1]]] = permuted_matrix_threeflip[:, [triplet[0][1], triplet[0][0]]]

    # Apply the second flip
    permuted_matrix_threeflip[[triplet[1][0], triplet[1][1]], :] = permuted_matrix_threeflip[[triplet[1][1], triplet[1][0]], :]
    permuted_matrix_threeflip[:, [triplet[1][0], triplet[1][1]]] = permuted_matrix_threeflip[:, [triplet[1][1], triplet[1][0]]]

    # Apply the third flip
    permuted_matrix_threeflip[[triplet[2][0], triplet[2][1]], :] = permuted_matrix_threeflip[[triplet[2][1], triplet[2][0]], :]
    permuted_matrix_threeflip[:, [triplet[2][0], triplet[2][1]]] = permuted_matrix_threeflip[:, [triplet[2][1], triplet[2][0]]]

    # Calculate the norm difference between the original and permuted matrices
    total_difference_threeflip = 0.0
    for row in range(len(distance_matrix_1_aligned)):
        for col in range(len(distance_matrix_1_aligned)):
            cell_difference_threeflip = abs(distance_matrix_1_aligned[row][col] - permuted_matrix_threeflip[row][col])
            total_difference_threeflip += cell_difference_threeflip

    # Store total difference
    distance_threeflips.append(total_difference_threeflip)

# Directory to store the output files
output_dir = "./outputs/DeltaAndFlips/"
os.makedirs(output_dir, exist_ok=True)

# Define the distances for each flip
flips_distances = {
    "1flip": distance_permutations_oneflip,
    "2flip": distance_twoflips,
    "3flip": distance_threeflips
}

# Save distances into separate files
for flip, distances in flips_distances.items():
    output_file = os.path.join(output_dir, f"{flip}_Phylogenetic_deltadistances.txt")
    try:
        with open(output_file, "w") as file:
            for distance in distances:
                file.write(f"{distance}\n")
        #print(f"Saved {flip} distances to {output_file}")
    except Exception as e:
        print(f"Error saving {flip} distances: {e}")

# Generate all possible permutations of row-column swaps for the distance matrix (oneflip)
permutations_oneflip = []
matrix_size_oneflip = len(distance_matrix_2_aligned)

for i in range(matrix_size_oneflip):
    for j in range(i + 1, matrix_size_oneflip):
        permutations_oneflip.append([i, j])

# Calculate the distances for each permutation (oneflip)
distance_permutations_oneflip = []

for perm in permutations_oneflip:
    # Create a copy of the matrix for swapping
    permuted_matrix_oneflip = np.copy(distance_matrix_2_aligned)

    # Swap rows and columns
    permuted_matrix_oneflip[[perm[0], perm[1]], :] = permuted_matrix_oneflip[[perm[1], perm[0]], :]
    permuted_matrix_oneflip[:, [perm[0], perm[1]]] = permuted_matrix_oneflip[:, [perm[1], perm[0]]]

    # Calculate the norm difference between the original and permuted matrices
    total_difference_oneflip = 0.0
    for row in range(matrix_size_oneflip):
        for col in range(matrix_size_oneflip):
            cell_difference_oneflip = abs(distance_matrix_2_aligned[row][col] - permuted_matrix_oneflip[row][col])
            total_difference_oneflip += cell_difference_oneflip

    # Store total difference
    distance_permutations_oneflip.append(total_difference_oneflip)

# Generate all possible two-row-column flip permutations for the distance matrix
two_permutations = []
total_permutations = len(permutations_oneflip)

# Generate initial two-permutation pairs
for i in range(total_permutations):
    for j in range(i, total_permutations):
        if i != j:
            two_permutations.append([permutations_oneflip[i], permutations_oneflip[j]])

# Extend the list of two-permutations by adding additional combinations
for perm_pair in two_permutations[:]:  # Iterate over a copy of the list
    if perm_pair[0][0] == perm_pair[1][0]:
        new_pair = [perm_pair[1], perm_pair[0]]
        two_permutations.append(new_pair)
    if perm_pair[0][0] == perm_pair[1][1]:
        new_pair = [perm_pair[1], perm_pair[0]]
        two_permutations.append(new_pair)
    if perm_pair[0][1] == perm_pair[1][0]:
        new_pair = [perm_pair[1], perm_pair[0]]
        two_permutations.append(new_pair)
    if perm_pair[0][1] == perm_pair[1][1]:
        new_pair = [perm_pair[1], perm_pair[0]]
        two_permutations.append(new_pair)

# Calculate the distances for each two-flip permutation
distance_twoflips = []

for perm_pair in two_permutations:
    # Create a copy of the matrix for swapping
    permuted_matrix_twoflip = np.copy(distance_matrix_2_aligned)

    # Apply the first flip
    permuted_matrix_twoflip[[perm_pair[0][0], perm_pair[0][1]], :] = permuted_matrix_twoflip[[perm_pair[0][1], perm_pair[0][0]], :]
    permuted_matrix_twoflip[:, [perm_pair[0][0], perm_pair[0][1]]] = permuted_matrix_twoflip[:, [perm_pair[0][1], perm_pair[0][0]]]

    # Apply the second flip
    permuted_matrix_twoflip[[perm_pair[1][0], perm_pair[1][1]], :] = permuted_matrix_twoflip[[perm_pair[1][1], perm_pair[1][0]], :]
    permuted_matrix_twoflip[:, [perm_pair[1][0], perm_pair[1][1]]] = permuted_matrix_twoflip[:, [perm_pair[1][1], perm_pair[1][0]]]

    # Calculate the norm difference between the original and permuted matrices
    total_difference_twoflip = 0.0
    for row in range(len(distance_matrix_2_aligned)):
        for col in range(len(distance_matrix_2_aligned)):
            cell_difference_twoflip = abs(distance_matrix_2_aligned[row][col] - permuted_matrix_twoflip[row][col])
            total_difference_twoflip += cell_difference_twoflip

    # Store total difference
    distance_twoflips.append(total_difference_twoflip)

# Generate all possible three-row-column flip permutations for the distance matrix
three_permutations = []
total_permutations = len(permutations_oneflip)

# Generate all possible triplets of permutations
for i in range(total_permutations):
    for j in range(total_permutations):
        for k in range(total_permutations):
            triplet = [permutations_oneflip[i], permutations_oneflip[j], permutations_oneflip[k]]
            three_permutations.append(triplet)

# Filter the triplets to ensure no duplicate flips within the triplet
valid_three_permutations = []
for triplet in three_permutations:
    if triplet[0] != triplet[1] and triplet[1] != triplet[2]:
        valid_three_permutations.append(triplet)

# Calculate the distances for each three-flip permutation
distance_threeflips = []

for triplet in valid_three_permutations:
    # Create a copy of the matrix for swapping
    permuted_matrix_threeflip = np.copy(distance_matrix_2_aligned)

    # Apply the first flip
    permuted_matrix_threeflip[[triplet[0][0], triplet[0][1]], :] = permuted_matrix_threeflip[[triplet[0][1], triplet[0][0]], :]
    permuted_matrix_threeflip[:, [triplet[0][0], triplet[0][1]]] = permuted_matrix_threeflip[:, [triplet[0][1], triplet[0][0]]]

    # Apply the second flip
    permuted_matrix_threeflip[[triplet[1][0], triplet[1][1]], :] = permuted_matrix_threeflip[[triplet[1][1], triplet[1][0]], :]
    permuted_matrix_threeflip[:, [triplet[1][0], triplet[1][1]]] = permuted_matrix_threeflip[:, [triplet[1][1], triplet[1][0]]]

    # Apply the third flip
    permuted_matrix_threeflip[[triplet[2][0], triplet[2][1]], :] = permuted_matrix_threeflip[[triplet[2][1], triplet[2][0]], :]
    permuted_matrix_threeflip[:, [triplet[2][0], triplet[2][1]]] = permuted_matrix_threeflip[:, [triplet[2][1], triplet[2][0]]]

    # Calculate the norm difference between the original and permuted matrices
    total_difference_threeflip = 0.0
    for row in range(len(distance_matrix_2_aligned)):
        for col in range(len(distance_matrix_2_aligned)):
            cell_difference_threeflip = abs(distance_matrix_2_aligned[row][col] - permuted_matrix_threeflip[row][col])
            total_difference_threeflip += cell_difference_threeflip

    # Store total difference
    distance_threeflips.append(total_difference_threeflip)

# Directory to store the output files
output_dir = "./outputs/DeltaAndFlips/"
os.makedirs(output_dir, exist_ok=True)

# Define the distances for each flip
flips_distances = {
    "1flip": distance_permutations_oneflip,
    "2flip": distance_twoflips,
    "3flip": distance_threeflips
}

# Save distances into separate files
for flip, distances in flips_distances.items():
    output_file = os.path.join(output_dir, f"{flip}_MFPT_deltadistances.txt")
    try:
        with open(output_file, "w") as file:
            for distance in distances:
                file.write(f"{distance}\n")
        #print(f"Saved {flip} distances to {output_file}")
    except Exception as e:
        print(f"Error saving {flip} distances: {e}")
