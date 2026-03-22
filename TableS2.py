import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kendalltau

# Input path for resilience files
resilience_input_dir = "./outputs/Resilience/"

# Define constants
percentages = [10, 20, 30, 40, 50, 60]
species_list = [
    "Arabidopsis", "Asplenium", "Brachypodium", "Barley", "Isoetes", "Lemna",
    "Lilium", "Marislea", "Selaginella", "Sweetpea", "Switchgrass", "Tomato", "Triticum", "Brassica"
]
attacks = ["EGM", "RND"]

# Prepare data for resilience rankings
resilience_data = []

# Process each attack and percentage
for attack in attacks:
    for perc in percentages:
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
resilience_df["Short_Name"] = resilience_df["Species"].str[:4]

# Rank species by resilience for each attack and percentage
resilience_ranking = resilience_df.sort_values(
    by=["Attack", "Percentage", "Resilience"], ascending=[True, True, False]
)

# Split into rankings for EGM and RND
ranked_egm = resilience_ranking[resilience_ranking["Attack"] == "EGM"].groupby("Percentage")["Short_Name"].apply(list)
ranked_rnd = resilience_ranking[resilience_ranking["Attack"] == "RND"].groupby("Percentage")["Short_Name"].apply(list)

# Load the KS size and treel data
ks_size_file = "./outputs/KSStatistics/KS_Size.csv"
ks_treel_file = "./outputs/KSStatistics/KS_Treel.csv"

ks_size_data = pd.read_csv(ks_size_file)
ks_treel_data = pd.read_csv(ks_treel_file)

# Merge the two datasets on species
ks_data = pd.merge(ks_size_data, ks_treel_data, on="Species", suffixes=("_size", "_treel"))
ks_data["Short_Name"] = ks_data["Species"].str[:4]

# Sort species by KS statistics for size and treelikeness
ranked_by_size = ks_data.sort_values(by="KS_Statistic_size", ascending=False)["Short_Name"].tolist()
ranked_by_treel = ks_data.sort_values(by="KS_Statistic_treel", ascending=False)["Short_Name"].tolist()

# Define columns and rows for the tables
columns = [f"p={p / 100}" for p in percentages]

# Placeholder for Kendall's Tau results
table_data_rnd_egm = []
table_data_size_egm = []
table_data_treel_egm = []

def format_result(value, p_value):
    """Format the Kendall's Tau result with significance stars."""
    if p_value < 0.001:
        return f"{value:.2f} ({p_value:.2f})***"
    elif p_value < 0.01:
        return f"{value:.2f} ({p_value:.2f})**"
    elif p_value < 0.05:
        return f"{value:.2f} ({p_value:.2f})*"
    else:
        return f"{value:.2f} ({p_value:.2f})"

# Calculate Kendall's Tau for each percentage
for perc in percentages:
    rnd_ranks = {species: rank for rank, species in enumerate(ranked_rnd[perc], start=1)}
    egm_ranks = {species: rank for rank, species in enumerate(ranked_egm[perc], start=1)}
    size_ranks = {species: rank for rank, species in enumerate(ranked_by_size, start=1)}
    treel_ranks = {species: rank for rank, species in enumerate(ranked_by_treel, start=1)}

    rnd_numeric = [rnd_ranks[species] for species in ranked_rnd[perc]]
    egm_numeric = [rnd_ranks[species] for species in ranked_egm[perc]]
    size_numeric = [rnd_ranks[species] for species in ranked_by_size]
    treel_numeric = [rnd_ranks[species] for species in ranked_by_treel]

    kt_rnd_egm, p_rnd_egm = kendalltau(rnd_numeric, egm_numeric)
    kt_size_egm, p_size_egm = kendalltau(size_numeric, egm_numeric)
    kt_treel_egm, p_treel_egm = kendalltau(treel_numeric, egm_numeric)

    table_data_rnd_egm.append(format_result(kt_rnd_egm, p_rnd_egm))
    table_data_size_egm.append(format_result(kt_size_egm, p_size_egm))
    table_data_treel_egm.append(format_result(kt_treel_egm, p_treel_egm))

# Create DataFrames
df_rnd_egm = pd.DataFrame([table_data_rnd_egm], columns=columns, index=["\t"+r"$K_{\tau}$"+"\t"])
df_size_egm = pd.DataFrame([table_data_size_egm], columns=columns, index=["\t"+r"$K_{\tau}$"+"\t"])
df_treel_egm = pd.DataFrame([table_data_treel_egm], columns=columns, index=["\t"+r"$K_{\tau}$"+"\t"])

# Plot the tables
for df, title, file_name in zip(
    [df_rnd_egm, df_size_egm, df_treel_egm],
    [r"Correlation between rankings by RND and EGM Resilience ($\rho$)", 
     r"Correlation between rankings by Size KS ($\omega_{S}$) and EGM Resilience ($\rho$)", 
     r"Correlation between rankings by Stringiness KS ($\omega_{\sigma}$) and EGM Resilience ($\rho$)"],
    ["TableS2_part1.pdf", "TableS2_part2.pdf", "TableS2_part3.pdf"]
):
    fig, ax = plt.subplots(figsize=(12, 2.5))
    ax.axis("tight")
    ax.axis("off")

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        rowLabels=df.index,
        cellLoc="center",
        loc="center",
        bbox=[0, 0, 1, 0.7]  # Adjusted to create better spacing for the title
    )

    # Add a title above the table
    ax.text(
        0.5, 0.7, title, fontsize=14, fontweight="bold", ha="center",
        transform=ax.transAxes
    )

    # Style table
    for key, cell in table.get_celld().items():
        if key[0] == 0:  # Header cells
            cell.set_facecolor("#ffffff")  # White header
            cell.set_text_props(fontsize=12)  # Larger font size for headers
        elif key[0] == 1:  # "Kτ" row
            cell.set_facecolor("#f2f2f2")  # Light grey for content cells
            cell.set_text_props(fontsize=12)  # Larger font size
        else:
            cell.set_facecolor("#f2f2f2")  # Light grey cells
        cell.set_edgecolor("black" if key[0] > 0 and key[1] > -1 else "none")  # Remove outer borders

    plt.savefig(f"./generatedfigures/{file_name}", bbox_inches="tight")
    print(f"Saved {title} as ./generatedfigures/{file_name}")
