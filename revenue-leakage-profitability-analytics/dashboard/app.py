import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from dotenv import load_dotenv
import os

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.markdown("""
<style>
.main {background-color: #f8fafc;}
.block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

st.title("Sales and Revenue Dashboard")

# -------------------------------
# Load ENV
# -------------------------------
load_dotenv()

# -------------------------------
# Load data
# -------------------------------
@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()
    return df

df = load_data()   

# -------------------------------
# Filters
# -------------------------------
st.subheader("Filters")

c1, c2 = st.columns(2)

with c1:
    region = st.multiselect(
        "Region",
        df["region"].unique(),
        default=df["region"].unique()
    )

with c2:
    category = st.multiselect(
        "Category",
        df["product_category"].unique(),
        default=df["product_category"].unique()
    )

# ✅ CREATE filtered_df BEFORE USING
filtered_df = df[
    (df["region"].isin(region)) &
    (df["product_category"].isin(category))
].copy()

# -------------------------------
# Helpers
# -------------------------------
def format_inr(x):
    if x >= 1_00_00_000:
        return f"₹{x/1_00_00_000:.2f} Cr"
    elif x >= 1_00_000:
        return f"₹{x/1_00_000:.2f} L"
    else:
        return f"₹{x:,.0f}"

def rupee_axis(fig):
    fig.update_layout(
        yaxis_tickprefix="₹",
        yaxis_tickformat=",",
        separators=","
    )
    return fig

# -------------------------------
# KPI metrics
# -------------------------------
total_revenue = filtered_df["sales_amount"].sum()
total_profit = filtered_df["profit"].sum()
margin = (total_profit / total_revenue) * 100 if total_revenue else 0

k1, k2, k3 = st.columns(3)

k1.metric("Revenue", format_inr(total_revenue))
k2.metric("Profit", format_inr(total_profit))
k3.metric("Margin %", f"{margin:.2f}%")

# -------------------------------
# Loss metrics
# -------------------------------
loss_df = filtered_df[filtered_df["profit"] < 0]
loss = loss_df["profit"].sum()
leak_pct = abs(loss) / total_revenue * 100 if total_revenue else 0

l1, l2, l3 = st.columns(3)

l1.metric("Loss", format_inr(loss))
l2.metric("Loss Orders", len(loss_df))
l3.metric("Leakage %", f"{leak_pct:.2f}%")

# -------------------------------
# Map
# -------------------------------
st.subheader("Sales Across India")

map_df = filtered_df.groupby("region")["sales_amount"].sum().reset_index()

region_coords = {
    "North": {"lat": 28.6, "lon": 77.2},
    "South": {"lat": 13.0, "lon": 80.2},
    "East": {"lat": 22.5, "lon": 88.3},
    "West": {"lat": 19.0, "lon": 72.8}
}

map_df["lat"] = map_df["region"].map(lambda x: region_coords[x]["lat"])
map_df["lon"] = map_df["region"].map(lambda x: region_coords[x]["lon"])

fig = px.scatter_geo(
    map_df,
    lat="lat",
    lon="lon",
    size="sales_amount",
    color="sales_amount",
    hover_name="region",
    projection="natural earth"
)

fig.update_geos(
    center={"lat": 22.5937, "lon": 78.9629},
    projection_scale=5,
    showcountries=True,
    showland=True,
    landcolor="rgb(240,240,240)"
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Donut chart
# -------------------------------
st.subheader("Revenue Distribution")

cat_df = filtered_df.groupby("product_category")["sales_amount"].sum().reset_index()

fig = px.pie(cat_df, names="product_category", values="sales_amount", hole=0.6)
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Profit chart
# -------------------------------
st.subheader("Profit by Category")

bar_df = filtered_df.groupby("product_category")["profit"].sum().reset_index()

fig = px.bar(bar_df, x="product_category", y="profit", text="profit")
fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
fig = rupee_axis(fig)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Monthly trend
# -------------------------------
st.subheader("Monthly Trend")

filtered_df["order_date"] = pd.to_datetime(filtered_df["order_date"])

monthly = filtered_df.groupby(
    filtered_df["order_date"].dt.to_period("M")
)[["sales_amount","profit"]].sum().reset_index()

monthly["order_date"] = monthly["order_date"].astype(str)

fig = px.line(monthly, x="order_date", y=["sales_amount","profit"], markers=True)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Insights
# -------------------------------
st.subheader("Insights")

if not filtered_df[filtered_df["discount"] > 15].empty:
    st.warning("High discounts are reducing profit. Reduce discounts above 15 percent.")

worst_cat = filtered_df.groupby("product_category")["profit"].sum().idxmin()
st.error(f"Worst category: {worst_cat}")

worst_region = filtered_df.groupby("region")["profit"].sum().idxmin()
st.info(f"Worst region: {worst_region}")

# -------------------------------
# Loss table
# -------------------------------
st.subheader("Loss Making Orders")

st.dataframe(loss_df.sort_values(by="profit"), use_container_width=True)