-- ============================================
-- Orders Table Schema
-- ============================================

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    order_date DATE,
    customer_id INTEGER,

    product_category TEXT,
    region TEXT,

    sales_amount REAL,
    discount REAL,
    profit REAL,

    payment_method TEXT
);
