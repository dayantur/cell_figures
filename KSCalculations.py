#!/usr/bin/env python
# coding: utf-8

# 1. Introduction and Setup
import os
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import zipfile

# Define zip archive paths
real_data_zip = "./outputs/ClusterSizeTreelikeness/ClusterSizeTreelikeness.zip"
null_data_zip = "./outputs/ClusterSizeTreelikenessNulls/ClusterSizeTreelikenessNulls.zip"

# Define output directory
output_dir = "./outputs/KSStatistics/"
os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

# Define parameters
colour = "green"  # We are focusing on green (colour_2)

# Prepare output files
ks_size_file = os.path.join(output_dir, "KS_Size.csv")
ks_treel_file = os.path.join(output_dir, "KS_Treel.csv")

# Initialize dataframes to save results
ks_size_results = []
ks_treel_results = []

# Open zip files for access
real_data_zipf = zipfile.ZipFile(real_data_zip, 'r')
null_data_zipf = zipfile.ZipFile(null_data_zip, 'r')

def load_real_data(species, colour, zipf):
    """Load real data for a species and colour from the zip archive."""
    # Load cluster sizes
    size_file = f"{species}_{colour}_clustersize.txt"
    with zipf.open(size_file, 'r') as f:
        real_sizes = [float(line.strip()) for line in f]
    
    # Load treelikeness values
    treel_file = f"{species}_{colour}_treel.txt"
    with zipf.open(treel_file, 'r') as f:
        real_treels = [float(line.strip()) for line in f]
    
    return real_sizes, real_treels

def load_null_data(species, colour, metric, zipf):
    """Load null data for a species, colour, and metric (size or treel) from the zip archive."""
    all_nulls = []
    for null_index in range(1, 1001):
        null_file = f"{species}_{colour}_null{null_index}_{metric}.txt"
        with zipf.open(null_file, 'r') as f:
            null_data = [float(line.strip()) for line in f]
            all_nulls.extend(null_data)
    return all_nulls

# 3. Process Data
def compute_cumulative_distribution(data):
    """Compute the cumulative distribution for a given dataset."""
    sorted_data = np.sort(data)
    cumulative = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    return sorted_data, cumulative

# 4. Calculate KS Statistics
def calculate_ks(real, null):
    """Calculate the KS statistic and p-value."""
    ks_stat, p_value = ks_2samp(real, null)
    return ks_stat, p_value

# 5. Main Analysis Loop
# Extract the list of species from the zip file
species_list = sorted({f.split("_")[0] for f in real_data_zipf.namelist() if f.endswith(f"_{colour}_clustersize.txt")})

for species in species_list:
    # Load data from the zip archives
    real_sizes, real_treels = load_real_data(species, colour, real_data_zipf)
    null_sizes = load_null_data(species, colour, "clustersize", null_data_zipf)
    null_treels = load_null_data(species, colour, "treel", null_data_zipf)
    
    # Compute cumulative distributions
    real_sizes_sorted, real_sizes_cumulative = compute_cumulative_distribution(real_sizes)
    null_sizes_sorted, null_sizes_cumulative = compute_cumulative_distribution(null_sizes)
    real_treels_sorted, real_treels_cumulative = compute_cumulative_distribution(real_treels)
    null_treels_sorted, null_treels_cumulative = compute_cumulative_distribution(null_treels)
    
    # Calculate KS statistics
    ks_size, p_size = calculate_ks(real_sizes_sorted, null_sizes_sorted)
    ks_treel, p_treel = calculate_ks(real_treels_sorted, null_treels_sorted)
    
    # Append results
    ks_size_results.append({"Species": species, "KS_Statistic": ks_size, "P_Value": p_size})
    ks_treel_results.append({"Species": species, "KS_Statistic": ks_treel, "P_Value": p_treel})

# Close the zip files after processing
real_data_zipf.close()
null_data_zipf.close()

# 6. Save Results
# Convert to DataFrame and save as CSV
pd.DataFrame(ks_size_results).to_csv(ks_size_file, index=False)
pd.DataFrame(ks_treel_results).to_csv(ks_treel_file, index=False)

print(f"KS statistics for size saved to {ks_size_file}")
print(f"KS statistics for treelikeness saved to {ks_treel_file}")

