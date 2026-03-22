import os
import numpy as np
import pandas as pd

# Define constants
species_list = [
    "Arabidopsis", "Asplenium", "Brachypodium", "Barley", "Isoetes", "Lemna", 
    "Lilium", "Marislea", "Selaginella", "Sweetpea", "Switchgrass", "Tomato", "Triticum", "Brassica"
]
percentages = [10, 20, 30, 40, 50, 60]
realizations = 100
attacks = ["RND", "EGM"]

# Input and output paths
input_dir = "./MFPT/Real_MFPT/"
output_dir = "./outputs/TauAlfaBetaAttacked/Real/"
os.makedirs(output_dir, exist_ok=True)

# Process files for all species
for species in species_list:
    print(f"Processing species: {species}")
    
    # Input file path
    input_file = os.path.join(input_dir, f"10^4_mfpt_{species}.txt")
    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found. Skipping.")
        continue

    # Initialize matrices
    time_matrix = [[0.0 for _ in range(3)] for _ in range(3)]
    counter_matrix = [[0.0 for _ in range(3)] for _ in range(3)]
    talfabeta_matrix = [[0.0 for _ in range(3)] for _ in range(3)]

    # Read input file and populate time and counter matrices
    with open(input_file) as fp:
        for line in fp:
            line = line.replace("0:", "").replace("1:", "").replace("2:", "").replace("3:", "")
            data = line.split()
            from_state = int(data[0])
            if from_state < 3:  # Ensure state index is within range
                time_matrix[from_state][0] += float(data[1])
                counter_matrix[from_state][0] += 1.0
                time_matrix[from_state][1] += float(data[2])
                counter_matrix[from_state][1] += 1.0
                time_matrix[from_state][2] += float(data[3])
                counter_matrix[from_state][2] += 1.0

    # Calculate talfabeta matrix
    for i in range(3):
        for j in range(3):
            if time_matrix[i][j] == 0 and counter_matrix[i][j] == 0:
                talfabeta_matrix[i][j] = 0.0
            else:
                talfabeta_matrix[i][j] = time_matrix[i][j] / counter_matrix[i][j]

    # Output file path
    output_file = os.path.join(output_dir, f"{species}_talfabeta.txt")
    with open(output_file, "w") as f:
        for row in talfabeta_matrix:
            f.write(" ".join(f"{value:.6f}" for value in row))
            f.write("\n")

    print(f"Processed species: {species}")

print("Processing completed.")

# Input and output paths
input_base_dir = "./MFPT/Attacks_MFPT/"
output_dir = "./outputs/TauAlfaBetaAttacked/Attacked/"
os.makedirs(output_dir, exist_ok=True)

# Process each attack, species, and percentage
for attack in attacks:
    print(f"Processing attack: {attack}")
    for species in species_list:
        print(f"  Processing species: {species}")
        for perc in percentages:
            print(f"    Processing percentage: {perc}%")

            # Initialize matrices for totals
            matrice_talfabeta_rnd_tot = [[0.0 for _ in range(3)] for _ in range(3)]
            numero_realizzazioni = 0.0

            # Loop through realizations
            for r in range(realizations):
                # Input file path for the realization
                input_file = os.path.join(
                    input_base_dir, attack, attack,
                    f"10^4_mfpt_{species}_r{r}_{attack.lower()}worm_p{perc}.txt"
                )
                if not os.path.exists(input_file):
                    print(f"      Warning: {input_file} not found. Skipping.")
                    continue

                # Initialize time and counter matrices for this realization
                matrice_tempi_rnd = [[0.0 for _ in range(3)] for _ in range(3)]
                matrice_contatori_rnd = [[0.0 for _ in range(3)] for _ in range(3)]

                # Process the realization file
                with open(input_file, "r") as file:
                    for line in file:
                        line = line.replace("0:", "").replace("1:", "").replace("2:", "").replace("3:", "")
                        data = line.split()
                        if len(data) == 4:  # Ensure valid line
                            from_state = int(data[0])
                            if from_state < 3 and from_state >=0:  # Ensure state index is within range
                                matrice_tempi_rnd[from_state][0] += float(data[1])
                                matrice_contatori_rnd[from_state][0] += 1.0
                                matrice_tempi_rnd[from_state][1] += float(data[2])
                                matrice_contatori_rnd[from_state][1] += 1.0
                                matrice_tempi_rnd[from_state][2] += float(data[3])
                                matrice_contatori_rnd[from_state][2] += 1.0

                # Calculate talfabeta matrix for this realization
                matrice_talfabeta_rnd = [[0.0 for _ in range(3)] for _ in range(3)]
                for i in range(3):
                    for j in range(3):
                        if matrice_tempi_rnd[i][j] == 0 and matrice_contatori_rnd[i][j] == 0:
                            matrice_talfabeta_rnd[i][j] = 0.0
                        else:
                            matrice_talfabeta_rnd[i][j] = matrice_tempi_rnd[i][j] / matrice_contatori_rnd[i][j]

                # Accumulate the realization's talfabeta matrix into the total matrix
                for i in range(3):
                    for j in range(3):
                        matrice_talfabeta_rnd_tot[i][j] += matrice_talfabeta_rnd[i][j]

                numero_realizzazioni += 1.0

            # Average the talfabeta matrix across realizations
            for i in range(3):
                for j in range(3):
                    matrice_talfabeta_rnd_tot[i][j] /= numero_realizzazioni

            # Output the averaged matrix
            output_file = os.path.join(
                output_dir, f"{species}_{attack.lower()}worm_p{perc}_talfabeta.txt"
            )
            with open(output_file, "w") as f:
                for row in matrice_talfabeta_rnd_tot:
                    f.write(" ".join(f"{value:.6f}" for value in row))
                    f.write("\n")

            print(f"    Processed {int(numero_realizzazioni)} realizations for {species}, {perc}%, {attack}")

print("Processing completed.")

# Output path for resilience
resilience_output_dir = "./outputs/Resilience/"
os.makedirs(resilience_output_dir, exist_ok=True)

# Function to compute 2-norm for a submatrix
def compute_2_norm(real_matrix, attacked_matrix):
    # Extract 2x2 submatrices (row-column indices 1 and 2)
    real_submatrix = np.array(real_matrix)[1:, 1:]
    attacked_submatrix = np.array(attacked_matrix)[1:, 1:]

    # Compute the element-wise difference
    diff = real_submatrix - attacked_submatrix

    # Compute the Frobenius norm (square root of the sum of squared differences)
    norm_2 = np.sqrt(np.sum(diff**2))
    return norm_2

# Process each attack, species, and percentage
for attack in attacks:
    for species in species_list:
        print(f"Processing resilience for {species}, attack: {attack}")

        # Load the real matrix
        real_file = os.path.join("./outputs/TauAlfaBetaAttacked/Real/", f"{species}_talfabeta.txt")
        if not os.path.exists(real_file):
            print(f"  Warning: Real matrix for {species} not found. Skipping.")
            continue
        real_matrix = np.loadtxt(real_file)

        # Prepare output file
        output_file = os.path.join(resilience_output_dir, f"{species}_{attack.lower()}_resilience.txt")
        with open(output_file, "w") as f:
            # Process each percentage
            for perc in percentages:
                # Initialize variables to calculate average norm
                norms_sum = 0
                realization_count = 0

                # Loop through realizations for the current percentage
                for r in range(realizations):
                    attacked_file = os.path.join(
                        "./outputs/TauAlfaBetaAttacked/Attacked/",
                        f"{species}_{attack.lower()}worm_p{perc}_talfabeta.txt"
                    )
                    if not os.path.exists(attacked_file):
                        print(f"  Warning: Attacked matrix for {species}, realization {r}, {perc}% not found. Skipping.")
                        continue

                    # Load the attacked matrix
                    attacked_matrix = np.loadtxt(attacked_file)

                    # Compute the 2-norm between the real and attacked matrix
                    norm = compute_2_norm(real_matrix, attacked_matrix)
                    norms_sum += norm
                    realization_count += 1

                # Calculate average norm and resilience
                if realization_count > 0:
                    average_norm = norms_sum / realization_count
                    resilience = 1 / average_norm if average_norm != 0 else float('inf')
                else:
                    resilience = float('NaN')  # Handle missing realizations

                # Save the resilience value
                f.write(f"{perc}: {resilience:.6f}\n")

        print(f"  Resilience saved for {species}, attack: {attack}")

print("Resilience calculation completed.")

# Input path for resilience files
resilience_input_dir = "./outputs/Resilience/"

# Define constants
colors = ["red", "orange", "yellow", "lightgreen", "green", "darkgreen", 
          "turquoise", "blue", "purple", "violet", "magenta", "pink", "grey", "darkred"]
species_colors = dict(zip(species_list, colors))  # Map species to colors

# Prepare data for alluvial plot
alluvial_data = []

# Process each percentage and attack
for attack in attacks:
    for perc in percentages:
        # Dictionary to store resilience values for this percentage
        resilience_values = {}

        # Read resilience files and extract values for this percentage
        for species in species_list:
            resilience_file = os.path.join(resilience_input_dir, f"{species}_{attack.lower()}_resilience.txt")
            if not os.path.exists(resilience_file):
                print(f"Warning: Resilience file for {species}, attack {attack} not found. Skipping.")
                continue

            # Extract resilience for the current percentage
            with open(resilience_file, "r") as f:
                for line in f:
                    if line.startswith(f"{perc}:"):
                        resilience = float(line.split(":")[1].strip())
                        resilience_values[species] = resilience
                        break

        # Rank species by resilience for this percentage in descending order
        sorted_species = sorted(resilience_values.items(), key=lambda x: x[1], reverse=True)
        ranked_species = [item[0] for item in sorted_species]

        # Normalize sizes to maintain ranking but equalize visual block size
        block_size = 1.0
        size_values = {species: block_size + i * 0.01 for i, species in enumerate(ranked_species)}

        # Add to alluvial data
        for species in ranked_species:
            alluvial_data.append({
                "Species": species,
                "year": perc / 100.0,  # Convert to fractions for x-axis
                "size": size_values[species],
                "attack": attack
            })

# Save alluvial data to CSV
output_file = "./outputs/Resilience/alluvial_data.csv"
df_alluvial = pd.DataFrame(alluvial_data)
df_alluvial.to_csv(output_file, index=False)
print(f"Alluvial data saved to {output_file}")

# Save species-to-color mapping to a text file
mapping_file = "./outputs/Resilience/species_colors.txt"
with open(mapping_file, "w") as f:
    f.write("Species\tColor\n")
    for species, color in species_colors.items():
        f.write(f"{species}\t{color}\n")
print(f"Species-to-color mapping saved to {mapping_file}")
