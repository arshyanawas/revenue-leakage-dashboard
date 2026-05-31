import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# -------------------------
# Config
# -------------------------
NUM_ROWS = 10000

regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Clothing", "Grocery", "Furniture"]
payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash"]

# -------------------------
# Generate Data
# -------------------------
data = []

start_date = datetime(2023, 1, 1)

for i in range(NUM_ROWS):
    order_id = i + 1
    order_date = start_date + timedelta(days=random.randint(0, 365))
    customer_id = random.randint(1000, 5000)

    category = random.choice(categories)
    region = random.choice(regions)

    sales_amount = round(random.uniform(100, 5000), 2)
    discount = round(random.uniform(0, 30), 2)

    # Profit logic (important for analysis)
    cost = sales_amount * random.uniform(0.5, 0.9)
    profit = round(sales_amount - cost - discount, 2)

    payment_method = random.choice(payment_methods)

    data.append([
        order_id,
        order_date,
        customer_id,
        category,
        region,
        sales_amount,
        discount,
        profit,
        payment_method
    ])

# -------------------------
# Create DataFrame
# -------------------------
df = pd.DataFrame(data, columns=[
    "order_id",
    "order_date",
    "customer_id",
    "product_category",
    "region",
    "sales_amount",
    "discount",
    "profit",
    "payment_method"
])

# -------------------------
# Save to CSV
# -------------------------
df.to_csv("data/raw/sales_data.csv", index=False)

print("✅ Data generated successfully!")