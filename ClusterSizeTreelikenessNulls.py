#!/usr/bin/env python
# coding: utf-8

import os
import collections

# Define the directory for the nulls
nulls_directory = "./plants_nulls/"
nets_directory = "./plants_nets/"

# Collect paths to all network files
net_paths = {
    os.path.basename(file).split("_")[0]: os.path.join(nets_directory, file)
    for file in os.listdir(nets_directory)
    if file.endswith("net_relabel.txt") and "Equisetum" not in file
}

# Collect paths to all null reshufflings for each species
nulls_paths = {}
for file in os.listdir(nulls_directory):
    if file.endswith(".txt") and "Equisetum" not in file:
        species_name = file.split("_null_")[0]
        if species_name not in nulls_paths:
            nulls_paths[species_name] = []
        nulls_paths[species_name].append(os.path.join(nulls_directory, file))

# Sort nulls for each species to ensure consistent ordering
for species_name in nulls_paths:
    nulls_paths[species_name].sort()

# Print the paths for a specific species (e.g., Arabidopsis)
print("Net path:", net_paths["Arabidopsis"])
print("Null paths:", nulls_paths["Arabidopsis"][:5])  # Print the first 5 nulls to check

# Initialize a dictionary to store data for all species nulls
species_nulls_col_dict = {}

# Loop through each species
for species_name, null_paths in nulls_paths.items():
    species_nulls_col_dict[species_name] = []  # Initialize list for this species

    # Process each null reshuffling file for the species
    for null_path in null_paths:
        dict_nodes = {}  # Initialize the node dictionary for this null
        
        # Read the null reshuffling file and populate the dict_nodes
        with open(null_path, "r") as fp:
            for line in fp:
                line = line.strip().split(" ")
                node_id = int(line[0])  # Convert node ID to integer
                node_type = int(line[1])  # Convert type (colour identifier) to integer

                # Assign colours and initialize sets based on type
                if node_type == 0:
                    first_colour = set()
                    dict_nodes[node_id] = ["colour_1", first_colour]
                elif node_type == 1:
                    second_colour = set()
                    dict_nodes[node_id] = ["colour_2", second_colour]
                else:
                    third_colour = set()
                    dict_nodes[node_id] = ["colour_3", third_colour]
        
        # Add this null's dict_nodes to the species list
        species_nulls_col_dict[species_name].append(dict_nodes)

# Check the data for Arabidopsis
# Number of null reshufflings for Arabidopsis
len(species_nulls_col_dict["Arabidopsis"])
# Check the first null reshuffling for Arabidopsis
species_nulls_col_dict["Arabidopsis"][0]

# Initialize a dictionary to store nets for all species
species_net_dict = {}

# Loop through each species and populate the nets
for species_name, net_path in net_paths.items():
    net = []  # Initialize the net list for this species
    
    # Read the network file and populate the net list
    with open(net_path, "r") as fp:
        for line in fp:
            line = line.strip().split(" ")
            pair = [int(line[0]), int(line[1])]  # Create a pair of node IDs
            net.append(pair)
    
    # Save the net list in the species dictionary
    species_net_dict[species_name] = net

# Check the data
# Number of species processed
len(species_net_dict)
# Check the net for Arabidopsis
species_net_dict["Arabidopsis"]

# Initialize a dictionary to store adjacency structure for all species
species_adj_dict = {}

# Process each species to compute the adjacency structure
for species_name, net in species_net_dict.items():
    # Initialize dict_nodes with adjacency sets
    dict_nodes = {}
    for edge in net:
        current_sx, current_dx = edge
        if current_sx not in dict_nodes:
            dict_nodes[current_sx] = ["", set()]
        if current_dx not in dict_nodes:
            dict_nodes[current_dx] = ["", set()]
        dict_nodes[current_sx][1].add(current_dx)
        dict_nodes[current_dx][1].add(current_sx)

    # Save the adjacency structure for the species
    species_adj_dict[species_name] = dict_nodes

# Check the adjacency structure for a species (e.g., Arabidopsis)
species_adj_dict["Arabidopsis"]

# Transform the adjacency sets to lists for all species in the precomputed adjacency dictionary
for species_name in species_adj_dict:
    dict_nodes = species_adj_dict[species_name]  # Get the precomputed adjacency structure for the species
    
    # Transform sets into lists for each node
    for node_id in dict_nodes:
        transformed = list(dict_nodes[node_id][1])
        dict_nodes[node_id][1] = transformed
    
    # Update the species_adj_dict with the transformed adjacency lists
    species_adj_dict[species_name] = dict_nodes

# Check the transformed adjacency lists for a species (e.g., Arabidopsis)
species_adj_dict["Arabidopsis"]

# Initialize a dictionary to store clusters for all species, nulls, and colours
species_nulls_clusters_dict = {"colour_2": {}, "colour_3": {}}

# Process each species for both colours
for species_name in species_nulls_col_dict:  # Process each species
    for colour_cluster in ["colour_2", "colour_3"]:
        # Use the precomputed adjacency structure for the species
        adjacency = species_adj_dict[species_name]

        # Initialize a list to store clusters for all nulls for this species and colour
        species_nulls_clusters_dict[colour_cluster][species_name] = []

        # Process each null reshuffling
        for null_index, null_dict_nodes in enumerate(species_nulls_col_dict[species_name]):
            collection_cluster = []  # Initialize the list to store clusters for this null
            visited_nodes = set()  # Initialize the visited nodes set for this null

            # Explore the network and collect clusters
            for node in adjacency:
                if null_dict_nodes[node][0] == colour_cluster and node not in visited_nodes:
                    # Perform a breadth-first search (BFS) to collect the cluster
                    cluster = []
                    stack = [node]

                    while stack:
                        current_node = stack.pop()
                        if current_node not in visited_nodes:
                            visited_nodes.add(current_node)
                            cluster.append(current_node)
                            # Add neighbors of the same colour to the stack
                            for neighbor in adjacency[current_node][1]:
                                if (
                                    neighbor not in visited_nodes
                                    and null_dict_nodes[neighbor][0] == colour_cluster
                                ):
                                    stack.append(neighbor)

                    collection_cluster.append(cluster)

            # Save the clusters for the current null reshuffling
            species_nulls_clusters_dict[colour_cluster][species_name].append(collection_cluster)

    # Print progress for the species after processing all nulls for both colours
    print(f"Finished processing all nulls for species: {species_name}")

# Check the clusters for a species, null, and colour (e.g., Arabidopsis, first null, colour_2)
species_nulls_clusters_dict["colour_2"]["Arabidopsis"][0]

import os
import zipfile

# Define the zip archive path
output_dir = "./outputs/ClusterSizeTreelikenessNulls/"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
zip_output_path = os.path.join(output_dir, "ClusterSizeTreelikenessNulls.zip")

# Define a mapping from colours to their names
colour_mapping = {
    "colour_2": "green",
    "colour_3": "blue"
}

# Check if the output directory exists
if not os.path.exists(output_dir):
    raise ValueError(f"Output directory does not exist: {output_dir}")
else:
    print(f"Output directory exists: {output_dir}")

# Create the zip archive
with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Process and save cluster sizes for each species' nulls
    for colour_cluster, species_data in species_nulls_clusters_dict.items():
        for species_name, nulls in species_data.items():
            for null_index, collection_cluster in enumerate(nulls):
                collection_size = []

                # Compute cluster sizes
                for cluster in collection_cluster:
                    current_size = len(cluster)
                    collection_size.append(current_size)

                # Determine the colour name for the output file
                colour_name = colour_mapping[colour_cluster]

                # Generate the file name
                file_name = f"{species_name}_{colour_name}_null{null_index + 1}_clustersize.txt"

                # Generate the file content
                file_content = "\n".join(map(str, collection_size))

                # Write directly into the zip archive
                zipf.writestr(file_name, file_content)
                print(f"Added to zip: {file_name}")

# Verify the zip file creation
if os.path.exists(zip_output_path):
    print(f"Zip file successfully created: {zip_output_path}")
else:
    print(f"Failed to create zip file: {zip_output_path}")

import os
import zipfile

# Define the zip archive path
output_dir = "./outputs/ClusterSizeTreelikenessNulls/"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
zip_output_path = os.path.join(output_dir, "ClusterSizeTreelikenessNulls.zip")

# Define a mapping from colours to their names
colour_mapping = {
    "colour_2": "green",
    "colour_3": "blue"
}

# Initialize a dictionary to store treelikeness for all species, nulls, and colours
species_nulls_treel_dict = {"colour_2": {}, "colour_3": {}}

# Create the zip archive
with zipfile.ZipFile(zip_output_path, 'a', zipfile.ZIP_DEFLATED) as zipf:  # Append mode ('a')
    # Process each species for both colours
    for colour_cluster, species_data in species_nulls_clusters_dict.items():
        for species_name, nulls in species_data.items():
            # Initialize a list to store treelikeness for all nulls for this species and colour
            species_nulls_treel_dict[colour_cluster][species_name] = []

            # Process each null reshuffling
            for null_index, collection_cluster in enumerate(nulls):
                null_dict_nodes = species_nulls_col_dict[species_name][null_index]  # Use the null reshuffling
                collection_treel = []  # Initialize the list to store treelikeness for this null

                # Compute treelikeness for each cluster
                for current_cluster in collection_cluster:
                    edges_in = 0

                    # Count internal edges
                    for node in current_cluster:
                        for neighbor in species_adj_dict[species_name][node][1]:
                            # Ensure the edge connects nodes of the same colour in the null reshuffling
                            if null_dict_nodes[neighbor][0] == colour_cluster:
                                edges_in += 1
                    edges_in /= 2  # Each edge is counted twice

                    # Compute treelikeness
                    cluster_size = len(current_cluster)
                    if edges_in == 0 or (cluster_size - 1) == 0:
                        treel = 0.0
                    else:
                        treel = (cluster_size - 1) / edges_in

                    collection_treel.append(treel)

                # Save the treelikeness for the current null reshuffling
                species_nulls_treel_dict[colour_cluster][species_name].append(collection_treel)

                # Generate the file name
                colour_name = colour_mapping[colour_cluster]
                file_name = f"{species_name}_{colour_name}_null{null_index + 1}_treel.txt"

                # Generate the file content
                file_content = "\n".join(f"{treel:.6f}" for treel in collection_treel)

                # Write directly into the zip archive
                zipf.writestr(file_name, file_content)
                print(f"Added to zip: {file_name}")

print(f"All treelikeness files for nulls zipped into: {zip_output_path}")

# Access the clusters for the first null model of Arabidopsis for colour_2
arabidopsis_null1_clusters_colour2 = species_nulls_clusters_dict["colour_2"]["Arabidopsis"][0]

# Compute the sizes of the clusters
arabidopsis_null1_cluster_sizes_colour2 = [len(cluster) for cluster in arabidopsis_null1_clusters_colour2]

# Print the cluster sizes
print("Cluster sizes for Arabidopsis, null 1, colour_2:", arabidopsis_null1_cluster_sizes_colour2)

species_nulls_clusters_dict["colour_2"]["Arabidopsis"][0][2]

