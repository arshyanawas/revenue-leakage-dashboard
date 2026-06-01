import sqlite3
import pandas as pd

# Load CSV
df = pd.read_csv("data/raw/sales_data.csv")

# Create SQLite database
conn = sqlite3.connect("data/sales.db")

# Store dataframe as SQL table
df.to_sql("orders", conn, if_exists="replace", index=False)

conn.close()

print("Database created successfully!")