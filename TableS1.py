import pandas as pd
import matplotlib.pyplot as plt

# 1. Read the KS statistics files
ks_size_file = './outputs/KSStatistics/KS_Size.csv'
ks_treel_file = './outputs/KSStatistics/KS_Treel.csv'

ks_size_df = pd.read_csv(ks_size_file)
ks_treel_df = pd.read_csv(ks_treel_file)

# 2. Merge and format the data
merged_df = pd.merge(
    ks_size_df.rename(columns={'KS_Statistic': '$\omega_{S}$', 'P_Value': 'P_Value_S'}),
    ks_treel_df.rename(columns={'KS_Statistic': '$\omega_{\sigma}$', 'P_Value': 'P_Value_T'}),
    on='Species'
)

def format_ks(value, p_value):
    if p_value < 0.01:
        return f"{value:.2f} (0.0)**"
    elif p_value < 0.05:
        return f"{value:.2f} ({p_value:.2f})*"
    else:
        return f"{value:.2f} ({p_value:.2f})"

merged_df['$\omega_{S}$'] = merged_df.apply(lambda row: format_ks(row['$\omega_{S}$'], row['P_Value_S']), axis=1)
merged_df['$\omega_{\sigma}$'] = merged_df.apply(lambda row: format_ks(row['$\omega_{\sigma}$'], row['P_Value_T']), axis=1)

final_table = merged_df[['Species', '$\omega_{S}$', '$\omega_{\sigma}$']]

# 3. Create the table
fig, ax = plt.subplots(figsize=(12, 6))  # Adjust figure size for more space
ax.axis('tight')
ax.axis('off')

# Define the table properties
table_data = final_table.values.tolist()
columns = final_table.columns.tolist()

table = ax.table(cellText=table_data, colLabels=columns, cellLoc='center', loc='center', bbox=[0, 0, 1, 1])

# Adjust cell styles
for (row, col), cell in table.get_celld().items():
    if row == 0:  # Header row
        cell.set_text_props(fontsize=15)  # Bold header
        cell.set_facecolor("white")  # Keep the header white
    else:
        cell.set_facecolor("#ededed")  # Set background color for non-header cells
        cell.set_text_props(fontsize=11)  # Adjust font size for data cells
    cell.set_edgecolor("black")  # Ensure borders are visible

# 4. Save the table as a PDF
pdf_path = './generatedfigures/TableS1.pdf'
plt.savefig(pdf_path, format='pdf', bbox_inches='tight')

print(f"Table saved as PDF: {pdf_path}")
plt.show()
