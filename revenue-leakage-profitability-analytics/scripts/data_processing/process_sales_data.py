import pandas as pd
import os

# Paths
raw_path = "data/raw/sales_data.csv"
processed_path = "data/processed/clean_sales_data.csv"

# Load data
df = pd.read_csv(raw_path)

# Basic cleaning
df.dropna(inplace=True)

# Example transformation
df['order_date'] = pd.to_datetime(df['order_date'])

# Save processed data
os.makedirs("data/processed", exist_ok=True)
df.to_csv(processed_path, index=False)

print("Processed data saved!")