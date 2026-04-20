import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

# Load CSV (relative path)
df = pd.read_csv("data/raw/sales_data.csv")

# Get DB credentials
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = conn.cursor()

# Drop table if exists
cursor.execute("DROP TABLE IF EXISTS orders")

# Create table
cursor.execute("""
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    order_date DATE,
    customer_id INT,
    product_category VARCHAR(100),
    region VARCHAR(50),
    sales_amount FLOAT,
    discount FLOAT,
    profit FLOAT,
    payment_method VARCHAR(50)
)
""")

# Insert data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO orders VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(row))

conn.commit()
cursor.close()
conn.close()

print("Data loaded successfully!")