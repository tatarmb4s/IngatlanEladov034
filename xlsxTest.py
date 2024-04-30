import pandas as pd

# Specify the path to your XLSX file
file_path = "statisztika_18megye.xlsx"

# Load the XLSX file and read the 'Lakóingatlanok' sheet
df = pd.read_excel(file_path, sheet_name="Sorház", skiprows=1)

# Extract data from the first 2 columns (columns 0 and 1)
selected_columns = df.iloc[:, :2]

# Print the resulting DataFrame
print(selected_columns)
