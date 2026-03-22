import os
import numpy as np
import zipfile

# List of species
species_list = ["Arabidopsis", "Asplenium", "Brachypodium", "Barley", "Isoetes", "Lemna", 
                "Lilium", "Marislea", "Selaginella", "Sweetpea", "Switchgrass", "Tomato", "Triticum", "Brassica"]

# Base path to the real files
base_path = "./MFPT/Real_MFPT" 

# Path to the zipped null files
null_zip_path = "./MFPT/Nulls_MFPT/Null_Fixed.zip"

# Dictionary to store talfabeta_real matrices for each species
talfabeta_real_dict = {}

# Process each species
for species in species_list:
    input_file = f"{base_path}/10^4_mfpt_{species}.txt"  # Construct the file path

    # Initialize a 3x3 matrix to store the MFPT values
    talfabeta_real = np.zeros((3, 3))

    # Initialize counters for each matrix entry
    counters = np.zeros((3, 3))  # Same shape as talfabeta_real

    try:
        # Process the file
        with open(input_file, "r") as file:
            for line in file:
                # Split the line into components
                parts = line.strip().split(" ")
                
                # Identify the row (key) from the first entry
                row = int(parts[0].split(":")[0])
                
                # Iterate through the remaining entries in the line
                for entry in parts[1:]:
                    # Split the entry into column and value
                    col, value = entry.split(":")
                    col = int(col)
                    value = float(value)
                    
                    # Update the sum and count for the corresponding matrix entry
                    talfabeta_real[row, col] += value
                    counters[row, col] += 1

        # Calculate the average for each matrix entry
        talfabeta_real = np.divide(
            talfabeta_real, counters, out=np.zeros_like(talfabeta_real), where=counters != 0
        )

        # Store the resulting matrix in the dictionary
        talfabeta_real_dict[species] = talfabeta_real

        print(f"Processed {species}:")
        print(talfabeta_real)

    except FileNotFoundError:
        print(f"File not found for {species}: {input_file}")

# Dictionary to store talfabeta_nulls matrices for each species
talfabeta_nulls_dict = {}

# Open the zip file
with zipfile.ZipFile(null_zip_path, 'r') as zip_file:
    # Process each species
    for species in species_list:
        # Initialize a 3x3 matrix to store the sum of MFPT values
        talfabeta_nulls = np.zeros((3, 3))
        counters = np.zeros((3, 3))  # Same shape as talfabeta_nulls

        # Get a sorted list of all null files for the species in the zip
        null_files = sorted(
            [f for f in zip_file.namelist() if f.endswith(f"{species}_.txt")]
        )

        # Loop through each null file
        for null_file in null_files:
            # Open the file directly from the zip
            with zip_file.open(null_file) as file:
                for line in file:
                    try:
                        # Decode the line from bytes to string, ignore problematic characters
                        line = line.decode('utf-8', errors='ignore').strip()
                        
                        # Split the line into components
                        parts = line.split(" ")
                        
                        # Identify the row (key) from the first entry
                        row = int(parts[0].split(":")[0])
                        
                        # Iterate through the remaining entries in the line
                        for entry in parts[1:]:
                            # Split the entry into column and value
                            col, value = entry.split(":")
                            col = int(col)
                            value = float(value)
                            
                            # Update the sum and count for the corresponding matrix entry
                            talfabeta_nulls[row, col] += value
                            counters[row, col] += 1
                    except Exception as e:
                        print(f"Error processing line in file {null_file}: {e}")

        # Compute the averages by dividing each cell's sum by its counter
        with np.errstate(divide='ignore', invalid='ignore'):  # Handle divide by zero safely
            talfabeta_nulls = np.divide(talfabeta_nulls, counters, where=counters > 0)

        # Store the resulting matrix in the dictionary
        talfabeta_nulls_dict[species] = talfabeta_nulls

        # Print progress (optional)
        print(f"Processed nulls for {species}:")
        print(talfabeta_nulls)

# Define the output directory
output_dir = "./outputs/TauAlfaBetaMatrices"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

# Dictionary to store the normalized matrices for each species
talfabeta_normalised_dict = {}

# Process each species
for species in species_list:
    # Retrieve the real and null matrices for the current species
    talfabeta_real = talfabeta_real_dict[species]  
    talfabeta_nulls = talfabeta_nulls_dict[species]
    
    # Ensure talfabeta_nulls is non-zero to avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):  # Handle division by zero safely
        talfabeta_normalised = np.divide(talfabeta_real, talfabeta_nulls, where=talfabeta_nulls > 0)
    
    # Handle division by zero explicitly (set these values to 0 or np.nan)
    talfabeta_normalised[np.isnan(talfabeta_normalised)] = 0  # Replace NaN with 0 if division by zero occurred
    
    # Extract the 2x2 sub-matrix (rows and columns 1 and 2 only)
    talfabeta_normalised_cropped = talfabeta_normalised[1:3, 1:3]
    
    # Store the cropped matrix in the dictionary
    talfabeta_normalised_dict[species] = talfabeta_normalised_cropped
    
    # Save the 2x2 matrix to a file
    output_file = os.path.join(output_dir, f"{species}_talfabeta_normalised.txt")
    np.savetxt(output_file, talfabeta_normalised_cropped, fmt="%.6f", delimiter=" ")
    
    print(f"Saved {species} talfabeta_normalised (2x2) matrix to {output_file}")

print("\nAll species' talfabeta_normalised matrices have been saved.")


# Directly populate talfabeta_matrices from talfabeta_normalised_dict
talfabeta_matrices = []

for species in species_list:
    if species in talfabeta_normalised_dict:
        talfabeta_matrices.append(talfabeta_normalised_dict[species])
    else:
        print(f"Warning: {species} not found in talfabeta_normalised_dict")

# Verify the length of the list matches the number of species
print(f"\nNumber of matrices: {len(talfabeta_matrices)} (Expected: {len(species_list)})")

import numpy as np
from scipy.cluster import hierarchy
from matplotlib import pyplot as plt

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
labels = [species for species in species_list if species != "Equisetum"]  # Exclude "Equisetum"

# Generate the dendrogram
linkage_method = 'average'
linkage_matrix = hierarchy.linkage(upper_triangle, method=linkage_method)

plt.figure(figsize=(7, 5))
plt.title("MFPT", fontweight="bold")
hierarchy.dendrogram(
    linkage_matrix,
    orientation='left',
    labels=labels,
    color_threshold=0.53,
    above_threshold_color='C0',
    leaf_font_size=12,
    show_leaf_counts=True
)

# Save the figure
output_path = "./generatedfigures/Fig3D.pdf"
plt.savefig(output_path, bbox_inches='tight', dpi=300)

print(f"Dendrogram saved to {output_path}")
plt.show()
