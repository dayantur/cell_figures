import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kendalltau

# Input path for resilience files
resilience_input_dir = "./outputs/Resilience/"

# Define constants
percentages = [10, 20, 30, 40, 50, 60]
species_list = [
    "Arabidopsis", "Asplenium", "Brachypodium", "Barley", "Isoetes", "Lemna",
    "Lilium", "Marislea", "Selaginella", "Sweetpea", "Switchgrass", "Tomato", "Triticum", "Brassica"
]
attacks = ["EGM", "RND"]  # Include multiple attacks for comparison

# Prepare data for resilience rankings
resilience_data = []

# Process each attack and percentage
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
                        resilience_data.append({
                            "Species": species,
                            "Attack": attack,
                            "Percentage": perc,
                            "Resilience": resilience
                        })
                        break

# Convert resilience data to a DataFrame
resilience_df = pd.DataFrame(resilience_data)

# Shorten species names for easier display
resilience_df["Short_Name"] = resilience_df["Species"].str[:4]

# Rank species by resilience for each attack and percentage
resilience_ranking = resilience_df.sort_values(
    by=["Attack", "Percentage", "Resilience"], ascending=[True, True, False]
)

# Split into rankings for EGM and RND for clarity
ranked_egm = (
    resilience_ranking[resilience_ranking["Attack"] == "EGM"]
    .groupby("Percentage")["Short_Name"]
    .apply(list)
)
ranked_rnd = (
    resilience_ranking[resilience_ranking["Attack"] == "RND"]
    .groupby("Percentage")["Short_Name"]
    .apply(list)
)

# Define RND and EGM rankings at p=0.5
p_50 = 50  # percentage value
rnd_ranking = ranked_rnd[p_50]
egm_ranking = ranked_egm[p_50]

# 1. Load the KS size and treel data
ks_size_file = "./outputs/KSStatistics/KS_Size.csv"
ks_treel_file = "./outputs/KSStatistics/KS_Treel.csv"

ks_size_data = pd.read_csv(ks_size_file)
ks_treel_data = pd.read_csv(ks_treel_file)

# Merge the two datasets on species
data = pd.merge(ks_size_data, ks_treel_data, on="Species", suffixes=("_size", "_treel"))

# Shorten species names to the first three letters
data["Short_Name"] = data["Species"].str[:4]

# Sort species by KS statistics for size and treelikeness
ranked_by_size = data.sort_values(by="KS_Statistic_size", ascending=False)["Short_Name"].tolist()
ranked_by_treel = data.sort_values(by="KS_Statistic_treel", ascending=False)["Short_Name"].tolist()

# Adjusted parameters
box_padding = 0.05  # Smaller padding around each text line
text_fontsize = 14  # Font size for species names
line_spacing = 0.15  # Spacing between lines
lines_y = [0.9, 0.9 - line_spacing, 0.9 - 2 * line_spacing, 0.9 - 3 * line_spacing]  # Y-coordinates for each line (RND, EGM, Size, Treel)

# Plot configuration
plt.figure(figsize=(10, 3))

# Assign colours based on RND ranking
colors = plt.cm.plasma(np.linspace(0, 1, len(rnd_ranking)))  # Gradient colouring
species_to_color = {species: color for species, color in zip(rnd_ranking, colors)}  # Map RND ranking to colours

# Plot each ranking
rankings = [rnd_ranking, egm_ranking, ranked_by_size, ranked_by_treel]
labels = [r"$\rho_{p=0.5}^{RND}$", r"$\rho_{p=0.5}^{EGM}$", "Size KS\n($\omega_{S}$)", "Stringiness KS\n($\omega_{\sigma}$)"]

for i, (ranking, label, y) in enumerate(zip(rankings, labels, lines_y)):
    # Plot species names
    for j, name in enumerate(ranking):
        plt.text(
            j + 0.5, y, name, ha='center', va='center',
            fontsize=text_fontsize, color=species_to_color.get(name, "black"),
            weight='bold', style='italic'
        )
    # Draw rectangle around the ranking
    plt.plot([0, len(ranking)], [y + box_padding, y + box_padding], color="black", lw=1.5)  # Top border
    plt.plot([0, len(ranking)], [y - box_padding, y - box_padding], color="black", lw=1.5)  # Bottom border
    plt.plot([0, 0], [y - box_padding, y + box_padding], color="black", lw=1.5)  # Left border
    plt.plot([len(ranking), len(ranking)], [y - box_padding, y + box_padding], color="black", lw=1.5)  # Right border
    # Add label on the left of each row
    plt.text(-1.5, y, label, ha='center', va='center', fontsize=text_fontsize)

# Remove axes and tidy up
plt.axis('off')
plt.tight_layout()

# Save the figure as a PDF
output_dir = "./generatedfigures/"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
output_file = os.path.join(output_dir, "Fig4D.pdf")
plt.savefig(output_file, format="pdf", bbox_inches="tight")

print(f"Figure saved as PDF: {output_file}")

# Show the plot
plt.show()

# Map species to their ranks in each ranking
rnd_ranks = {species: rank for rank, species in enumerate(rnd_ranking, start=1)}
egm_ranks = {species: rank for rank, species in enumerate(egm_ranking, start=1)}
size_ranks = {species: rank for rank, species in enumerate(ranked_by_size, start=1)}
treel_ranks = {species: rank for rank, species in enumerate(ranked_by_treel, start=1)}

# Create numeric sequences for Kendall's Tau calculation
rnd_numeric = [rnd_ranks[species] for species in rnd_ranking]  # Reference: RND ranking
egm_numeric = [rnd_ranks[species] for species in egm_ranking]  # Map RND ranks to EGM ranking order
size_numeric = [rnd_ranks[species] for species in ranked_by_size]  # Map RND ranks to Size KS order
treel_numeric = [rnd_ranks[species] for species in ranked_by_treel]  # Map RND ranks to Stringiness KS order

# Calculate Kendall's Tau for each pair
kt_rnd_egm, p_rnd_egm = kendalltau(rnd_numeric, egm_numeric)
kt_rnd_size, p_rnd_size = kendalltau(rnd_numeric, size_numeric)
kt_rnd_treel, p_rnd_treel = kendalltau(rnd_numeric, treel_numeric)

# Print the results
print(f"Kendall's Tau (RND vs. EGM): {kt_rnd_egm:.2f}, p-value: {p_rnd_egm}")
print(f"Kendall's Tau (RND vs. Size KS): {kt_rnd_size:.2f}, p-value: {p_rnd_size}")
print(f"Kendall's Tau (RND vs. Stringiness KS): {kt_rnd_treel:.2f}, p-value: {p_rnd_treel}")
