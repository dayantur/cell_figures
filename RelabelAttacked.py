import os

# Define constants

species_name = "Brassica"
percentages = ["10", "20", "30", "40", "50", "60"]

realizations = 100

# Parameters
att = "rnd"  # Attack type
att_u = att.upper()

# Input and output paths
input_colors_path = f"./plants_nets/{species_name}_colours_relabel_p.txt"
attacked_nets_dir = f"./outputs/Attacks/{att_u}/{species_name}"
relabel_output_dir = f"./outputs/Attacks/{att_u}/{species_name}/Relabel/"

os.makedirs(relabel_output_dir, exist_ok=True)

# Load color relabel data
id_real = []
class_real = []
with open(input_colors_path) as fp:
    for line in fp:
        line = line.split(" ")
        id_real.append(int(line[0]))
        class_real.append(int(line[1]))

# Process attacked networks for each percentage
for p in percentages:
    for r in range(realizations):
        # Attacked network input file
        attacked_net_file = os.path.join(attacked_nets_dir, f"{species_name}_net_{att}att_p{p}_{r}.txt")
        if not os.path.exists(attacked_net_file):
            print(f"Warning: {attacked_net_file} not found. Skipping.")
            continue

        in_ed = []
        out_ed = []
        with open(attacked_net_file) as fp:
            for line in fp:
                line = line.split(" ")
                in_ed.append(int(line[0]))
                out_ed.append(int(line[1]))

        # Identify nodes in the attacked network
        nodes_att = set(in_ed + out_ed)

        # Filter and relabel nodes and classes
        id_att = [node for node in id_real if node in nodes_att]
        class_att = [class_real[id_real.index(node)] for node in id_att]
        dict_rel = {node: idx for idx, node in enumerate(id_att)}

        # Relabel edges
        in_ed_r = [dict_rel[node] for node in in_ed]
        out_ed_r = [dict_rel[node] for node in out_ed]

        # Save relabeled network
        relabel_net_file = os.path.join(relabel_output_dir, f"{species_name}_net_{att}att_p{p}_{r}_r.txt")
        with open(relabel_net_file, "w") as f:
            for u, v in zip(in_ed_r, out_ed_r):
                f.write(f"{u} {v}\n")

        # Save relabeled class file
        relabel_class_file = os.path.join(relabel_output_dir, f"{species_name}_colours_{att}att_p{p}_{r}_r.txt")
        with open(relabel_class_file, "w") as f:
            for idx, class_label in enumerate(class_att):
                f.write(f"{idx} {class_label}\n")

print("Node relabeling for RND completed.")

att = "egm"
att_u = att.upper()

# Input and output paths
input_colors_path = f"./plants_nets/{species_name}_colours_relabel_p.txt"
attacked_nets_dir = f"./outputs/Attacks/{att_u}/{species_name}"
relabel_output_dir = f"./outputs/Attacks/{att_u}/{species_name}/Relabel/"

os.makedirs(relabel_output_dir, exist_ok=True)

# Load color relabel data
id_real = []
class_real = []
with open(input_colors_path) as fp:
    for line in fp:
        line = line.split(" ")
        id_real.append(int(line[0]))
        class_real.append(int(line[1]))

# Process attacked networks for each percentage
for p in percentages:
    for r in range(realizations):
        # Attacked network input file
        attacked_net_file = os.path.join(attacked_nets_dir, f"{species_name}_net_{att}att_p{p}_{r}.txt")
        if not os.path.exists(attacked_net_file):
            print(f"Warning: {attacked_net_file} not found. Skipping.")
            continue

        in_ed = []
        out_ed = []
        with open(attacked_net_file) as fp:
            for line in fp:
                line = line.split(" ")
                in_ed.append(int(line[0]))
                out_ed.append(int(line[1]))

        # Identify nodes in the attacked network
        nodes_att = set(in_ed + out_ed)

        # Filter and relabel nodes and classes
        id_att = [node for node in id_real if node in nodes_att]
        class_att = [class_real[id_real.index(node)] for node in id_att]
        dict_rel = {node: idx for idx, node in enumerate(id_att)}

        # Relabel edges
        in_ed_r = [dict_rel[node] for node in in_ed]
        out_ed_r = [dict_rel[node] for node in out_ed]

        # Save relabeled network
        relabel_net_file = os.path.join(relabel_output_dir, f"{species_name}_net_{att}att_p{p}_{r}_r.txt")
        with open(relabel_net_file, "w") as f:
            for u, v in zip(in_ed_r, out_ed_r):
                f.write(f"{u} {v}\n")

        # Save relabeled class file
        relabel_class_file = os.path.join(relabel_output_dir, f"{species_name}_colours_{att}att_p{p}_{r}_r.txt")
        with open(relabel_class_file, "w") as f:
            for idx, class_label in enumerate(class_att):
                f.write(f"{idx} {class_label}\n")

print("Node relabeling for EGM completed.")
