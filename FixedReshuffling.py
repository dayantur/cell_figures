#!/usr/bin/env python
# coding: utf-8

import os
import random

# Define the directory containing the files
directory = "./plants_nets/"

# Collect paths for all species
idcol_paths = [
    os.path.join(directory, file)
    for file in os.listdir(directory)
    if file.endswith("colours_relabel_p.txt")
]

# Initialize a dictionary to store node-colour data for each species
species_node_colour = {}

# Process each species file
for file_path in idcol_paths:
    species_name = os.path.basename(file_path).split("_")[0]  # Extract species name from file
    node_colour = {}

    # Read the file and collect node-colour data
    with open(file_path, "r") as fp:
        for line in fp:
            node, colour = map(int, line.strip().split(" "))
            node_colour[node] = colour

    # Save node-colour data for the species
    species_node_colour[species_name] = node_colour

# Define the number of null reshufflings
num_nulls = 1000

# Initialize a dictionary to store reshuffled data
species_nulls = {}

# Process each species
for species_name, node_colour in species_node_colour.items():
    # Separate nodes by colour
    grey_nodes = [node for node, colour in node_colour.items() if colour == 0]
    other_nodes = [node for node, colour in node_colour.items() if colour in [1, 2]]

    print(species_name)

    # Initialize a list to store null reshufflings for this species
    nulls = []

    # Perform reshuffling
    for _ in range(num_nulls):
        # Copy the current colours for reshuffling
        reshuffled_colours = {node: colour for node, colour in node_colour.items()}
        
        # Shuffle only the colours for nodes with 1 or 2
        reshuffled_values = [node_colour[node] for node in other_nodes]
        random.shuffle(reshuffled_values)

        # Update reshuffled colours for non-grey nodes
        for i, node in enumerate(other_nodes):
            reshuffled_colours[node] = reshuffled_values[i]

        # Save the reshuffled node-colour data
        nulls.append(reshuffled_colours)

    # Save all nulls for the species
    species_nulls[species_name] = nulls

# Define the directory for saving nulls
output_dir = "./plants_nulls/"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

# Save reshuffled nulls for each species
for species_name, nulls in species_nulls.items():
    for null_number, null_data in enumerate(nulls, start=1):
        # Generate the output file name
        output_file = os.path.join(output_dir, f"{species_name}_null_{null_number}.txt")

        # Save the null reshuffling to the file
        with open(output_file, "w") as f:
            for node, colour in sorted(null_data.items()):  # Sort nodes for consistency
                f.write(f"{node} {colour}\n")

