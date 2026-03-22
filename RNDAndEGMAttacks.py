import os
import random
import networkx as nx

# Define the species and percentages
species_name = "Brassica"  # Replace with your species name
percentages = [10, 20, 30, 40, 50, 60]

# Number of realizations
realizations = 100

# Paths for input and output
input_dir = "./plants_nets/"

# Base directories for outputs
rnd_output_dir_base = "./outputs/Attacks/RND/"
egm_output_dir_base = "./outputs/Attacks/EGM/"
os.makedirs(rnd_output_dir_base, exist_ok=True)
os.makedirs(egm_output_dir_base, exist_ok=True)

# Helper function to load the network and node colors
def load_network_and_colors(plant_name):
    dict_nodes = {}
    net = []

    # Load node colors
    with open(os.path.join(input_dir, f"{plant_name}_colours_relabel_p.txt")) as fp:
        for line in fp:
            line = line.split(" ")
            node = int(line[0])
            color = int(line[1])

            if color == 1:
                dict_nodes[node] = ["green", set()]
            elif color == 2:
                dict_nodes[node] = ["blue", set()]
            else:
                dict_nodes[node] = ["grey", set()]

    # Load edges
    with open(os.path.join(input_dir, f"{plant_name}_net_relabel.txt")) as fp:
        for line in fp:
            line = line.split(" ")
            net.append([int(line[0]), int(line[1])])

    # Populate connections
    for edge in net:
        dict_nodes[edge[0]][1].add(edge[1])
        dict_nodes[edge[1]][1].add(edge[0])

    # Convert sets to lists
    for node in dict_nodes:
        dict_nodes[node][1] = list(dict_nodes[node][1])

    return dict_nodes, net

# Random Removal Attack
print(f"Starting random removal attack simulation for {species_name}...")
rnd_output_dir = os.path.join(rnd_output_dir_base, f"{species_name}")
os.makedirs(rnd_output_dir, exist_ok=True)

for perc in percentages:
    count = 0
    remaining_realizations = realizations

    while remaining_realizations > 0:
        output_file = os.path.join(rnd_output_dir, f"{species_name}_net_rndatt_p{perc}_{count}.txt")
        dict_nodes, net = load_network_and_colors(species_name)

        # Calculate number of nodes to attack
        n_attacks = (len(dict_nodes) * perc) // 100

        # Randomly remove nodes
        key_list = list(dict_nodes.keys())
        removed_keys = random.sample(key_list, n_attacks)

        for key in removed_keys:
            del dict_nodes[key]

        # Remove edges connected to removed nodes
        for key in dict_nodes:
            dict_nodes[key][1] = [n for n in dict_nodes[key][1] if n not in removed_keys]

        # Create the attacked network
        net_att = []
        for key in dict_nodes:
            for neighbor in dict_nodes[key][1]:
                if key < neighbor:
                    net_att.append([key, neighbor])

        G_att = nx.Graph()
        G_att.add_edges_from(net_att)

        if nx.is_connected(G_att):
            # Save the attacked network
            with open(output_file, "w") as f:
                for edge in net_att:
                    f.write(f"{edge[0]} {edge[1]}\n")

            count += 1
            remaining_realizations -= 1

print("Random removal attack simulation completed.")

import os
import random
import networkx as nx
from datetime import datetime

# Paths for input and output
input_dir = "./plants_nets/"

# Base directories for outputs
egm_output_dir_base = "./outputs/Attacks/EGM/"
os.makedirs(egm_output_dir_base, exist_ok=True)

# Helper function to load the network and node colors
def load_network_and_colors(plant_name):
    dict_nodes = {}
    net = []

    # Load node colors
    with open(os.path.join(input_dir, f"{plant_name}_colours_relabel_p.txt")) as fp:
        for line in fp:
            line = line.split(" ")
            node = int(line[0])
            color = int(line[1])

            if color == 1:
                dict_nodes[node] = ["green", set()]
            elif color == 2:
                dict_nodes[node] = ["blue", set()]
            else:
                dict_nodes[node] = ["grey", set()]

    # Load edges
    with open(os.path.join(input_dir, f"{plant_name}_net_relabel.txt")) as fp:
        for line in fp:
            line = line.split(" ")
            net.append([int(line[0]), int(line[1])])

    # Populate connections
    for edge in net:
        dict_nodes[edge[0]][1].add(edge[1])
        dict_nodes[edge[1]][1].add(edge[0])

    # Convert sets to lists
    for node in dict_nodes:
        dict_nodes[node][1] = list(dict_nodes[node][1])

    return dict_nodes, net

# EGM Worm Attack
print(f"[{datetime.now()}] Starting EGM worm attack simulation for {species_name}...")
egm_output_dir = os.path.join(egm_output_dir_base, f"{species_name}")
os.makedirs(egm_output_dir, exist_ok=True)

for perc in percentages:
    count = 0
    remaining_realizations = realizations

    while remaining_realizations > 0:
        output_file = os.path.join(egm_output_dir, f"{species_name}_net_egmatt_p{perc}_{count}.txt")
        dict_nodes, net = load_network_and_colors(species_name)

        # Calculate number of nodes to attack
        n_attacks = (len(dict_nodes) * perc) // 100

        if n_attacks > 0:
            # Initialize EGM worm
            key_list = list(dict_nodes.keys())
            choice = random.choice(key_list)
            egm_worm = {choice}
            borders = list(dict_nodes[choice][1])

            # Expand EGM worm
            while len(egm_worm) < n_attacks:
                choice_int = random.choice(borders)
                egm_worm.add(choice_int)
                borders.remove(choice_int)
                for neighbor in dict_nodes[choice_int][1]:
                    if neighbor not in egm_worm:
                        borders.append(neighbor)
                borders = list(set(borders))

            # Remove nodes in EGM worm
            removed_nodes = list(egm_worm)
            for node in removed_nodes:
                if node in dict_nodes:
                    del dict_nodes[node]

            for node in dict_nodes:
                dict_nodes[node][1] = [n for n in dict_nodes[node][1] if n not in removed_nodes]

        # Create the attacked network
        net_att = []
        for key in dict_nodes:
            for neighbor in dict_nodes[key][1]:
                if key < neighbor:  # Avoid duplicate edges
                    net_att.append([key, neighbor])

        G_att = nx.Graph()
        G_att.add_edges_from(net_att)

        # Extract the largest connected component
        largest_component = max(nx.connected_components(G_att), key=len)
        G_largest = G_att.subgraph(largest_component).copy()

        # Sort edges of the largest connected component
        sorted_edges = sorted(G_largest.edges)

        # Save the sorted edges to the file
        with open(output_file, "w") as f:
            for edge in sorted_edges:
                f.write(f"{edge[0]} {edge[1]}\n")

        count += 1
        remaining_realizations -= 1
        # Print timestamp and remaining realizations
        print(f"[{datetime.now()}] Remaining realizations: {remaining_realizations}")

print("EGM worm attack simulation completed.")
