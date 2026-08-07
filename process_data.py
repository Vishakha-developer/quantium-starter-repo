import pandas as pd
import os

# Folder containing CSV files
data_folder = "data"

# CSV files to process
files = [
    "daily_sales_data_0.csv",
    "daily_sales_data_1.csv",
    "daily_sales_data_2.csv"
]

all_data = []

for file in files:
    file_path = os.path.join(data_folder, file)

    # Read CSV
    df = pd.read_csv(file_path)

    # Convert column names to lowercase and remove extra spaces
    df.columns = df.columns.str.strip().str.lower()

    # Keep only Pink Morsel
    df = df[df["product"].str.strip().str.lower() == "pink morsel"]

    # Remove '$' from price and convert to float
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # Convert quantity to integer
    df["quantity"] = df["quantity"].astype(int)

    # Calculate Sales
    df["Sales"] = df["quantity"] * df["price"]

    # Keep only required columns
    df = df[["Sales", "date", "region"]]

    # Rename columns
    df.columns = ["Sales", "Date", "Region"]

    all_data.append(df)

# Merge all CSV files
final_df = pd.concat(all_data, ignore_index=True)

# Save output file
output_file = "formatted_sales_data.csv"
final_df.to_csv(output_file, index=False)

print("✅ Processing complete!")
print(f"Total rows: {len(final_df)}")
print(f"Output file created: {output_file}")
print()
print(final_df.head())