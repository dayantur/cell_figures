import os
import numpy as np
import sys
import math

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <current_id>")
    exit(1)

# Get the current ID from command-line arguments
current_id = int(sys.argv[1])

# Load the distance matrix from an external file
distance_matrix_file = "./Phylogenetic_originaldistancematrix.txt"
try:
    distance_matrix = np.loadtxt(distance_matrix_file, delimiter=" ")
except Exception as e:
    print(f"Error loading distance matrix from {distance_matrix_file}: {e}")
    exit(1)

# Generate all possible pairs for row-column swaps
single_flips = []
matrix_size = len(distance_matrix)

for i in range(matrix_size):
    for j in range(i + 1, matrix_size):
        single_flips.append([i, j])

# Generate all possible triplets for triple flips
triple_flips = []

for i in single_flips:
    for j in single_flips:
        for k in single_flips:
            triplet = [i, j, k]
            triple_flips.append(triplet)

# Filter the triplets to ensure no duplicate flips within the triplet
filtered_triple_flips = []

for triplet in triple_flips:
    if triplet[0] != triplet[1] and triplet[1] != triplet[2]:
        filtered_triple_flips.append(triplet)

# Define intervals based on current ID
n_of_jobs = 98  # Adjust this value as needed
interval = int(len(filtered_triple_flips) / n_of_jobs)
lower_bound = interval * current_id
upper_bound = interval * (current_id + 1)

# Generate quadruple flips
quadruple_flips = []

for i in range(lower_bound, upper_bound):
    for j in range(len(single_flips)):
        quadruplet = [
            filtered_triple_flips[i][0],
            filtered_triple_flips[i][1],
            filtered_triple_flips[i][2],
            single_flips[j]
        ]
        quadruple_flips.append(quadruplet)

# Calculate distances for quadruple flips
quadruple_distances = []

print("Original Matrix:")
print(distance_matrix)
print("\n")

for flips in quadruple_flips:
    permuted_matrix = np.copy(distance_matrix)

    # Apply the first flip
    permuted_matrix[[flips[0][0], flips[0][1]], :] = permuted_matrix[[flips[0][1], flips[0][0]], :]
    permuted_matrix[:, [flips[0][0], flips[0][1]]] = permuted_matrix[:, [flips[0][1], flips[0][0]]]

    # Apply the second flip
    permuted_matrix[[flips[1][0], flips[1][1]], :] = permuted_matrix[[flips[1][1], flips[1][0]], :]
    permuted_matrix[:, [flips[1][0], flips[1][1]]] = permuted_matrix[:, [flips[1][1], flips[1][0]]]

    # Apply the third flip
    permuted_matrix[[flips[2][0], flips[2][1]], :] = permuted_matrix[[flips[2][1], flips[2][0]], :]
    permuted_matrix[:, [flips[2][0], flips[2][1]]] = permuted_matrix[:, [flips[2][1], flips[2][0]]]

    # Apply the fourth flip
    permuted_matrix[[flips[3][0], flips[3][1]], :] = permuted_matrix[[flips[3][1], flips[3][0]], :]
    permuted_matrix[:, [flips[3][0], flips[3][1]]] = permuted_matrix[:, [flips[3][1], flips[3][0]]]

    # Calculate the total difference
    total_difference = 0.0
    for row in range(matrix_size):
        for col in range(matrix_size):
            total_difference += abs(distance_matrix[row][col] - permuted_matrix[row][col])

    # Calculate normalized difference
    quadruple_distances.append(total_difference)

# Save the distances to a file
output_dir = "./data/"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f"PHY_quadrupleflip_data_{current_id}.txt")

with open(output_file, "w") as f:
    for distance in quadruple_distances:
        f.write(f"{distance}\n")

print(f"Distances saved to {output_file}")

