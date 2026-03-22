#!/usr/bin/env python
# coding: utf-8

import os
import collections

directory = "plants_nets"

# Collect paths to all colours_relabel_p.txt files, excluding "Equisetum"
idcol_paths = [
    os.path.join(directory, file)
    for file in os.listdir(directory)
    if file.endswith("colours_relabel_p.txt") and "Equisetum" not in file
]

#Initialize a dictionary to store data for all species
species_col_dict = {}

#Loop through each file and populate the dictionary
for file_path in idcol_paths:
    species_name = os.path.basename(file_path).split("_")[0]  # Extract species name from file
    dict_nodes = {}  # Initialize the node dictionary for this species
    
    # Read the file and populate the dict_nodes
    with open(file_path, "r") as fp:
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
    
    # Save the dict_nodes in the species dictionary
    species_col_dict[species_name] = dict_nodes

# Collect paths to all net_relabel.txt files, excluding "Equisetum"
net_paths = [
    os.path.join(directory, file)
    for file in os.listdir(directory)
    if file.endswith("net_relabel.txt") and "Equisetum" not in file
]

# Initialize a dictionary to store nets for all species
species_net_dict = {}

# Loop through each file and populate the dictionary
for file_path in net_paths:
    species_name = os.path.basename(file_path).split("_")[0]  # Extract species name from file
    net = []  # Initialize the net list for this species
    
    # Read the file and populate the net list
    with open(file_path, "r") as fp:
        for line in fp:
            line = line.strip().split(" ")
            pair = [int(line[0]), int(line[1])]  # Create a pair of node IDs
            net.append(pair)
    
    # Save the net list in the species dictionary
    species_net_dict[species_name] = net

# Process each species
for species_name in species_net_dict:

    net = species_net_dict[species_name]  # Get the net (list of edges) for the species
    dict_nodes = species_col_dict[species_name]  # Get the corresponding dict_nodes

    # Process edges to populate the adjacency sets
    for i in range(len(net)):
        current_sx = net[i][0]
        dict_nodes[current_sx][1].add(net[i][1])

    for i in range(len(net)):
        current_dx = net[i][1]
        dict_nodes[current_dx][1].add(net[i][0])

    # Update the species_col_dict with the modified dict_nodes
    species_col_dict[species_name] = dict_nodes

# Transform the adjacency sets to lists for all species
for species_name in species_col_dict:
    dict_nodes = species_col_dict[species_name]  # Get the dict_nodes for the species
    
    # Transform sets into lists for each node
    for node_id in dict_nodes:
        transformed = list(dict_nodes[node_id][1])
        dict_nodes[node_id][1] = transformed
    
    # Update the species_col_dict with the transformed dict_nodes
    species_col_dict[species_name] = dict_nodes

# Initialize a dictionary to store clusters for all species and both colours
species_clusters_dict = {"colour_2": {}, "colour_3": {}}

# Process each species for both colours
for colour_cluster in ["colour_2", "colour_3"]:
    for species_name in species_col_dict:
        dict_nodes = species_col_dict[species_name]  # Get the dict_nodes for the species
        collection_cluster = []  # Initialize the list to store clusters for this species
        visited_nodes = set()  # Initialize the visited nodes set for this species

        for node in dict_nodes:
            if dict_nodes[node][0] == colour_cluster and node not in visited_nodes:
                visited_nodes.add(node)
                key_current_node = node
                current_cluster = []
                current_node = dict_nodes[key_current_node]

                control_set = set()
                control_list = []
                flag_set = set()

                current_cluster.append(key_current_node)
                flag_set.add(key_current_node)

                for i in range(len(current_node[1])):
                    current = current_node[1][i]
                    control_set.add(current)
                    if dict_nodes[current][0] == current_node[0]:
                        current_cluster.append(current)

                control_list = list(control_set)

                count = 1

                while count > 0:
                    control_list = list(control_set)
                    for j in range(len(control_list)):
                        current = control_list[j]
                        if dict_nodes[current][0] == current_node[0]:
                            current_bis = dict_nodes[control_list[j]][1]
                            for q in range(len(current_bis)):
                                control_list.append(current_bis[q])
                                if dict_nodes[current_bis[q]][0] == current_node[0]:
                                    current_cluster.append(current_bis[q])
                        flag_set.add(control_list[j])

                    control_set = set(control_list)

                    for j in flag_set:
                        if j in control_set:
                            control_set.remove(j)

                    count = len(control_set)

                for element in set(current_cluster):
                    visited_nodes.add(element)
                current_cluster = list(set(current_cluster))
                collection_cluster.append(current_cluster)

        # Save the clusters for the current species and colour
        species_clusters_dict[colour_cluster][species_name] = collection_cluster

import os
import zipfile

# Define the zip archive path
output_dir = "./outputs/ClusterSizeTreelikeness/"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
zip_output_path = os.path.join(output_dir, "ClusterSizeTreelikeness.zip")

# Define a mapping from colours to their names
colour_mapping = {
    "colour_2": "green",
    "colour_3": "blue"
}

# Create the zip archive
with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Process and save cluster sizes for each species
    for colour_cluster, species_data in species_clusters_dict.items():
        for species_name, collection_cluster in species_data.items():
            collection_size = []

            # Compute cluster sizes
            for cluster in collection_cluster:
                current_size = len(cluster)
                collection_size.append(current_size)

            # Determine the colour name for the output file
            colour_name = colour_mapping[colour_cluster]

            # Generate the output file content
            file_content = "\n".join(map(str, collection_size))

            # Generate the file name
            file_name = f"{species_name}_{colour_name}_clustersize.txt"

            # Write directly into the zip archive
            zipf.writestr(file_name, file_content)
            #print(f"Added to zip: {file_name}")

print(f"All files zipped into: {zip_output_path}")

# Initialize a dictionary to store treelikeness for all species and colours
species_treel_dict = {"colour_2": {}, "colour_3": {}}

# Process each species and each colour
for colour_cluster, species_data in species_clusters_dict.items():
    for species_name, collection_cluster in species_data.items():
        dict_nodes = species_col_dict[species_name]  # Get the dict_nodes for the species
        collection_treel = []  # Initialize the list to store treelikeness values for this species

        # Compute treelikeness for each cluster
        for q in range(len(collection_cluster)):
            current_cluster = collection_cluster[q]
            edges_in = 0

            # Count internal edges
            for i in range(len(current_cluster)):
                check_node = dict_nodes[current_cluster[i]]
                for j in range(len(check_node[1])):
                    if dict_nodes[check_node[1][j]][0] == colour_cluster:
                        edges_in += 1
            edges_in /= 2  # Each edge is counted twice

            # Compute treelikeness
            if edges_in == 0 or (len(current_cluster) - 1) == 0:
                treel = 0.0
            else:
                treel = (len(current_cluster) - 1) / edges_in

            collection_treel.append(treel)

        # Save the treelikeness values for the current species and colour
        species_treel_dict[colour_cluster][species_name] = collection_treel

# Define the zip archive path
output_dir = "./outputs/ClusterSizeTreelikeness/"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
zip_output_path = os.path.join(output_dir, "ClusterSizeTreelikeness.zip")

# Define a mapping from colours to their names
colour_mapping = {
    "colour_2": "green",
    "colour_3": "blue"
}

# Create the zip archive
with zipfile.ZipFile(zip_output_path, 'a', zipfile.ZIP_DEFLATED) as zipf:  # Append mode ('a')
    # Process each species and each colour
    for colour_cluster, species_data in species_clusters_dict.items():
        for species_name, collection_cluster in species_data.items():
            dict_nodes = species_col_dict[species_name]  # Get the dict_nodes for the species
            collection_treel = []  # Initialize the list to store treelikeness values for this species

            # Compute treelikeness for each cluster
            for q in range(len(collection_cluster)):
                current_cluster = collection_cluster[q]
                edges_in = 0

                # Count internal edges
                for i in range(len(current_cluster)):
                    check_node = dict_nodes[current_cluster[i]]
                    for j in range(len(check_node[1])):
                        if dict_nodes[check_node[1][j]][0] == colour_cluster:
                            edges_in += 1
                edges_in /= 2  # Each edge is counted twice

                # Compute treelikeness
                if edges_in == 0 or (len(current_cluster) - 1) == 0:
                    treel = 0.0
                else:
                    treel = (len(current_cluster) - 1) / edges_in

                collection_treel.append(treel)

            # Determine the colour name for the output file
            colour_name = colour_mapping[colour_cluster]

            # Generate the output file name
            file_name = f"{species_name}_{colour_name}_treel.txt"

            # Generate the file content
            file_content = "\n".join(f"{treel:.6f}" for treel in collection_treel)

            # Write directly into the zip archive
            zipf.writestr(file_name, file_content)

print(f"Treelikeness files zipped into: {zip_output_path}")

