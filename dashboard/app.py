import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Revenue Leakage Dashboard",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
}

.metric-card {
    background-color: white;
    padding: 1rem;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("Revenue Leakage & Profitability Dashboard")

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
@st.cache_resource
def get_connection():
    conn = sqlite3.connect("data/sales.db", check_same_thread=False)
    return conn

conn = get_connection()

# -----------------------------------
# LOAD DATA
# -----------------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM orders"
    return pd.read_sql_query(query, conn)

df = load_data()

# -----------------------------------
# FILTERS
# -----------------------------------
st.subheader("Filters")

c1, c2 = st.columns(2)

with c1:
    selected_region = st.multiselect(
        "Select Region",
        options=df["region"].unique(),
        default=df["region"].unique()
    )

with c2:
    selected_category = st.multiselect(
        "Select Category",
        options=df["product_category"].unique(),
        default=df["product_category"].unique()
    )

# -----------------------------------
# FILTER QUERY
# -----------------------------------
region_str = "','".join(selected_region)
category_str = "','".join(selected_category)

base_query = f"""
SELECT *
FROM orders
WHERE region IN ('{region_str}')
AND product_category IN ('{category_str}')
"""

filtered_df = pd.read_sql_query(base_query, conn)

# -----------------------------------
# HELPERS
# -----------------------------------
def format_inr(x):
    if abs(x) >= 1_00_00_000:
        return f"₹{x/1_00_00_000:.2f} Cr"
    elif abs(x) >= 1_00_000:
        return f"₹{x/1_00_000:.2f} L"
    else:
        return f"₹{x:,.0f}"

# -----------------------------------
# KPI SECTION
# -----------------------------------
kpi_query = f"""
SELECT
    SUM(sales_amount) AS total_revenue,
    SUM(profit) AS total_profit,
    ROUND(SUM(profit) * 100.0 / SUM(sales_amount), 2) AS margin_pct
FROM (
    {base_query}
)
"""

kpi_df = pd.read_sql_query(kpi_query, conn)

total_revenue = kpi_df["total_revenue"][0]
total_profit = kpi_df["total_profit"][0]
margin_pct = kpi_df["margin_pct"][0]

k1, k2, k3 = st.columns(3)

k1.metric("Total Revenue", format_inr(total_revenue))
k2.metric("Total Profit", format_inr(total_profit))
k3.metric("Profit Margin %", f"{margin_pct:.2f}%")

# -----------------------------------
# LOSS METRICS
# -----------------------------------
loss_query = f"""
SELECT *
FROM (
    {base_query}
)
WHERE profit < 0
"""

loss_df = pd.read_sql_query(loss_query, conn)

total_loss = loss_df["profit"].sum()

leakage_pct = (
    abs(total_loss) / total_revenue * 100
    if total_revenue != 0 else 0
)

l1, l2, l3 = st.columns(3)

l1.metric("Revenue Leakage", format_inr(total_loss))
l2.metric("Loss Orders", len(loss_df))
l3.metric("Leakage %", f"{leakage_pct:.2f}%")

# -----------------------------------
# REGION MAP
# -----------------------------------
st.subheader("Regional Sales Performance")

map_query = f"""
SELECT
    region,
    SUM(sales_amount) AS sales_amount
FROM (
    {base_query}
)
GROUP BY region
"""

map_df = pd.read_sql_query(map_query, conn)

region_coords = {
    "North": {"lat": 28.6, "lon": 77.2},
    "South": {"lat": 13.0, "lon": 80.2},
    "East": {"lat": 22.5, "lon": 88.3},
    "West": {"lat": 19.0, "lon": 72.8}
}

map_df["lat"] = map_df["region"].map(lambda x: region_coords[x]["lat"])
map_df["lon"] = map_df["region"].map(lambda x: region_coords[x]["lon"])

fig_map = px.scatter_geo(
    map_df,
    lat="lat",
    lon="lon",
    size="sales_amount",
    color="sales_amount",
    hover_name="region",
    projection="natural earth"
)

fig_map.update_geos(
    center={"lat": 22.5937, "lon": 78.9629},
    projection_scale=5,
    showcountries=True,
    showland=True
)

fig_map.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------------
# REVENUE DISTRIBUTION
# -----------------------------------
st.subheader("Revenue Distribution by Category")

category_query = f"""
SELECT
    product_category,
    SUM(sales_amount) AS sales_amount
FROM (
    {base_query}
)
GROUP BY product_category
"""

category_df = pd.read_sql_query(category_query, conn)

fig_donut = px.pie(
    category_df,
    names="product_category",
    values="sales_amount",
    hole=0.6
)

st.plotly_chart(fig_donut, use_container_width=True)

# -----------------------------------
# PROFIT ANALYSIS
# -----------------------------------
st.subheader("Profit by Category")

profit_query = f"""
SELECT
    product_category,
    SUM(profit) AS profit
FROM (
    {base_query}
)
GROUP BY product_category
ORDER BY profit DESC
"""

profit_df = pd.read_sql_query(profit_query, conn)

fig_bar = px.bar(
    profit_df,
    x="product_category",
    y="profit",
    text="profit"
)

fig_bar.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="outside"
)

st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------------
# MONTHLY TREND
# -----------------------------------
st.subheader("Monthly Revenue & Profit Trend")

monthly_query = f"""
SELECT
    strftime('%Y-%m', order_date) AS month,
    SUM(sales_amount) AS revenue,
    SUM(profit) AS profit
FROM (
    {base_query}
)
GROUP BY month
ORDER BY month
"""

monthly_df = pd.read_sql_query(monthly_query, conn)

fig_line = px.line(
    monthly_df,
    x="month",
    y=["revenue", "profit"],
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)

# -----------------------------------
# INSIGHTS SECTION
# -----------------------------------
st.subheader("Business Insights")

discount_query = f"""
SELECT
    AVG(discount) AS avg_discount
FROM (
    {base_query}
)
"""

discount_df = pd.read_sql_query(discount_query, conn)

avg_discount = discount_df["avg_discount"][0]

if avg_discount > 15:
    st.warning(
        "High average discounts are negatively impacting profitability."
    )

worst_category_query = f"""
SELECT
    product_category,
    SUM(profit) AS total_profit
FROM (
    {base_query}
)
GROUP BY product_category
ORDER BY total_profit ASC
LIMIT 1
"""

worst_category_df = pd.read_sql_query(worst_category_query, conn)

worst_category = worst_category_df["product_category"][0]

st.error(f"Worst Performing Category: {worst_category}")

worst_region_query = f"""
SELECT
    region,
    SUM(profit) AS total_profit
FROM (
    {base_query}
)
GROUP BY region
ORDER BY total_profit ASC
LIMIT 1
"""

worst_region_df = pd.read_sql_query(worst_region_query, conn)

worst_region = worst_region_df["region"][0]

st.info(f"Worst Performing Region: {worst_region}")

# -----------------------------------
# LOSS-MAKING ORDERS
# -----------------------------------
st.subheader("Loss-Making Orders")

loss_table_query = f"""
SELECT
    order_id,
    order_date,
    product_category,
    region,
    sales_amount,
    discount,
    profit
FROM (
    {base_query}
)
WHERE profit < 0
ORDER BY profit ASC
"""

loss_table_df = pd.read_sql_query(loss_table_query, conn)

st.dataframe(
    loss_table_df,
    use_container_width=True
)

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")
st.caption(
    "Built using Streamlit, SQLite, SQL, Pandas, and Plotly"
)