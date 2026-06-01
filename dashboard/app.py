import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Revenue Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# THEME & STYLE
# ─────────────────────────────────────────────
COLORS = {
    "primary":   "#0F172A",
    "surface":   "#1E293B",
    "card":      "#263347",
    "accent":    "#38BDF8",
    "profit":    "#34D399",
    "loss":      "#F87171",
    "warning":   "#FBBF24",
    "text":      "#F1F5F9",
    "muted":     "#94A3B8",
}

PLOTLY_TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="'DM Sans', sans-serif", color=COLORS["text"], size=13),
        xaxis=dict(gridcolor="rgba(148,163,184,0.1)", linecolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor="rgba(148,163,184,0.1)", linecolor="rgba(0,0,0,0)"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=40, b=10),
        colorway=[COLORS["accent"], COLORS["profit"], COLORS["warning"], COLORS["loss"]],
    )
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {COLORS["primary"]};
    color: {COLORS["text"]};
}}

.stApp {{
    background-color: {COLORS["primary"]};
}}

section[data-testid="stSidebar"] {{
    background-color: {COLORS["surface"]};
    border-right: 1px solid rgba(148,163,184,0.1);
}}

div[data-testid="metric-container"] {{
    background-color: {COLORS["card"]};
    border: 1px solid rgba(148,163,184,0.1);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
}}

div[data-testid="metric-container"] label {{
    color: {COLORS["muted"]} !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 500;
}}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    color: {COLORS["text"]} !important;
    font-family: 'DM Mono', monospace;
}}

.section-header {{
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {COLORS["muted"]};
    margin: 2rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.section-header::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(148,163,184,0.15);
}}

.insight-card {{
    background: {COLORS["card"]};
    border: 1px solid rgba(148,163,184,0.1);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    font-size: 0.875rem;
    line-height: 1.5;
}}

.insight-card.danger {{
    border-left: 3px solid {COLORS["loss"]};
}}

.insight-card.success {{
    border-left: 3px solid {COLORS["profit"]};
}}

.insight-card.warning {{
    border-left: 3px solid {COLORS["warning"]};
}}

.insight-card.info {{
    border-left: 3px solid {COLORS["accent"]};
}}

.tag {{
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-right: 0.4rem;
    font-family: 'DM Mono', monospace;
}}

.tag-danger {{ background: rgba(248,113,113,0.15); color: {COLORS["loss"]}; }}
.tag-success {{ background: rgba(52,211,153,0.15); color: {COLORS["profit"]}; }}
.tag-warning {{ background: rgba(251,191,36,0.15); color: {COLORS["warning"]}; }}
.tag-info {{ background: rgba(56,189,248,0.15); color: {COLORS["accent"]}; }}

.page-title {{
    font-size: 1.6rem;
    font-weight: 600;
    color: {COLORS["text"]};
    letter-spacing: -0.02em;
    margin-bottom: 0;
}}

.page-subtitle {{
    font-size: 0.85rem;
    color: {COLORS["muted"]};
    margin-top: 0.25rem;
}}

div[data-testid="stDataFrame"] {{
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(148,163,184,0.1);
}}

div.stMultiSelect > div {{
    background-color: {COLORS["card"]};
    border-color: rgba(148,163,184,0.2);
    border-radius: 8px;
}}

.stTabs [data-baseweb="tab-list"] {{
    background-color: {COLORS["surface"]};
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}}

.stTabs [data-baseweb="tab"] {{
    background-color: transparent;
    color: {COLORS["muted"]};
    border-radius: 7px;
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.03em;
}}

.stTabs [aria-selected="true"] {{
    background-color: {COLORS["card"]} !important;
    color: {COLORS["text"]} !important;
}}

hr {{
    border-color: rgba(148,163,184,0.1);
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────
@st.cache_resource
def get_connection():
    return sqlite3.connect("data/sales.db", check_same_thread=False)

conn = get_connection()


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def fmt_inr(x):
    if x is None:
        return "₹0"
    if abs(x) >= 1_00_00_000:
        return f"₹{x/1_00_00_000:.2f} Cr"
    elif abs(x) >= 1_00_000:
        return f"₹{x/1_00_000:.1f} L"
    return f"₹{x:,.0f}"

def build_filter_clause(regions, categories):
    r = "','".join(regions)
    c = "','".join(categories)
    return f"region IN ('{r}') AND product_category IN ('{c}')"

def run_query(sql):
    return pd.read_sql_query(sql, conn)


# ─────────────────────────────────────────────
# SIDEBAR — FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding: 1rem 0 1.5rem 0;'>
        <div style='font-size:1.1rem; font-weight:600; color:{COLORS["text"]};'>Revenue Intelligence</div>
        <div style='font-size:0.75rem; color:{COLORS["muted"]}; margin-top:4px;'>Leakage & Profitability</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; color:{COLORS['muted']}; margin-bottom:0.5rem;'>Filters</div>", unsafe_allow_html=True)

    all_regions = run_query("SELECT DISTINCT region FROM orders ORDER BY region")["region"].tolist()
    all_categories = run_query("SELECT DISTINCT product_category FROM orders ORDER BY product_category")["product_category"].tolist()

    selected_regions = st.multiselect("Region", all_regions, default=all_regions)
    selected_categories = st.multiselect("Category", all_categories, default=all_categories)

    if not selected_regions or not selected_categories:
        st.warning("Select at least one region and category.")
        st.stop()

    st.markdown("---")
    st.markdown(f"<div style='font-size:0.7rem; color:{COLORS['muted']};'>Filters active: {len(selected_regions)} regions · {len(selected_categories)} categories</div>", unsafe_allow_html=True)

WHERE = build_filter_clause(selected_regions, selected_categories)


# ─────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class='page-title'>Revenue Leakage & Profitability</div>
<div class='page-subtitle'>SQL-powered analysis · Indian Sales Data</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# KPI ROW 1 — Revenue & Profit
# ─────────────────────────────────────────────
st.markdown("<div class='section-header'> Performance Overview</div>", unsafe_allow_html=True)

kpi = run_query(f"""
    SELECT
        SUM(sales_amount)                                        AS total_revenue,
        SUM(profit)                                              AS total_profit,
        ROUND(SUM(profit) * 100.0 / NULLIF(SUM(sales_amount),0), 2) AS margin_pct,
        COUNT(*)                                                 AS total_orders,
        COUNT(DISTINCT customer_id)                              AS unique_customers,
        ROUND(AVG(sales_amount), 2)                              AS avg_order_value
    FROM orders
    WHERE {WHERE}
""").iloc[0]

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Revenue",    fmt_inr(kpi.total_revenue))
k2.metric("Total Profit",     fmt_inr(kpi.total_profit))
k3.metric("Profit Margin",    f"{kpi.margin_pct:.1f}%")
k4.metric("Total Orders",     f"{int(kpi.total_orders):,}")
k5.metric("Unique Customers", f"{int(kpi.unique_customers):,}")
k6.metric("Avg Order Value",  fmt_inr(kpi.avg_order_value))


# ─────────────────────────────────────────────
# KPI ROW 2 — Leakage
# ─────────────────────────────────────────────
st.markdown("<div class='section-header'> Revenue Leakage</div>", unsafe_allow_html=True)

leakage = run_query(f"""
    SELECT
        SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END)         AS total_leakage,
        COUNT(CASE WHEN profit < 0 THEN 1 END)                   AS loss_orders,
        ROUND(COUNT(CASE WHEN profit < 0 THEN 1 END) * 100.0
              / NULLIF(COUNT(*), 0), 2)                           AS loss_order_pct,
        ROUND(AVG(CASE WHEN profit < 0 THEN discount END), 2)    AS avg_discount_on_losses
    FROM orders
    WHERE {WHERE}
""").iloc[0]

leakage_pct = abs(leakage.total_leakage) / kpi.total_revenue * 100 if kpi.total_revenue else 0

l1, l2, l3, l4 = st.columns(4)
l1.metric("Total Leakage",         fmt_inr(leakage.total_leakage))
l2.metric("Loss-Making Orders",    f"{int(leakage.loss_orders):,}")
l3.metric("Loss Order Rate",       f"{leakage.loss_order_pct:.1f}%")
l4.metric("Avg Discount on Losses",f"{leakage.avg_discount_on_losses:.1f}%")


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([" Breakdown", " Trends", "Deep Dive", " Orders"])


# ══════════════════════════════════════════════
# TAB 1 — BREAKDOWN
# ══════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns(2)

    # Category profitability
    with col_left:
        cat_df = run_query(f"""
            SELECT
                product_category,
                SUM(sales_amount)                                      AS revenue,
                SUM(profit)                                            AS profit,
                ROUND(SUM(profit)*100.0/NULLIF(SUM(sales_amount),0),1) AS margin_pct,
                COUNT(*)                                               AS orders
            FROM orders
            WHERE {WHERE}
            GROUP BY product_category
            ORDER BY profit DESC
        """)

        fig = px.bar(
            cat_df, x="product_category", y=["revenue", "profit"],
            barmode="group",
            title="Revenue vs Profit by Category",
            labels={"value": "Amount (₹)", "product_category": ""},
            color_discrete_map={"revenue": COLORS["accent"], "profit": COLORS["profit"]},
            template=PLOTLY_TEMPLATE,
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    # Margin heatmap by region x category
    with col_right:
        heat_df = run_query(f"""
            SELECT
                region,
                product_category,
                ROUND(SUM(profit)*100.0/NULLIF(SUM(sales_amount),0),1) AS margin_pct
            FROM orders
            WHERE {WHERE}
            GROUP BY region, product_category
        """)

        pivot = heat_df.pivot(index="region", columns="product_category", values="margin_pct")

        fig2 = px.imshow(
            pivot,
            title="Profit Margin % — Region × Category",
            color_continuous_scale=["#F87171", "#1E293B", "#34D399"],
            color_continuous_midpoint=0,
            text_auto=".1f",
            template=PLOTLY_TEMPLATE,
        )
        fig2.update_coloraxes(showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Payment method breakdown
    pay_df = run_query(f"""
        SELECT
            payment_method,
            COUNT(*)         AS orders,
            SUM(sales_amount) AS revenue,
            SUM(profit)       AS profit,
            ROUND(SUM(profit)*100.0/NULLIF(SUM(sales_amount),0),1) AS margin_pct
        FROM orders
        WHERE {WHERE}
        GROUP BY payment_method
        ORDER BY revenue DESC
    """)

    col_a, col_b = st.columns(2)
    with col_a:
        fig3 = px.pie(
            pay_df, names="payment_method", values="revenue",
            hole=0.65, title="Revenue by Payment Method",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=[COLORS["accent"], COLORS["profit"], COLORS["warning"], COLORS["loss"]],
        )
        fig3.update_traces(textposition="outside", textinfo="label+percent")
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        fig4 = px.bar(
            pay_df, x="payment_method", y="margin_pct",
            title="Profit Margin % by Payment Method",
            labels={"margin_pct": "Margin %", "payment_method": ""},
            color="margin_pct",
            color_continuous_scale=["#F87171", "#34D399"],
            template=PLOTLY_TEMPLATE,
        )
        fig4.update_coloraxes(showscale=False)
        fig4.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 2 — TRENDS
# ══════════════════════════════════════════════
with tab2:
    monthly_df = run_query(f"""
        SELECT
            strftime('%Y-%m', order_date)                              AS month,
            SUM(sales_amount)                                          AS revenue,
            SUM(profit)                                                AS profit,
            COUNT(*)                                                   AS orders,
            ROUND(SUM(profit)*100.0/NULLIF(SUM(sales_amount),0),2)    AS margin_pct,
            SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END)          AS leakage
        FROM orders
        WHERE {WHERE}
        GROUP BY month
        ORDER BY month
    """)

    # Revenue + Profit trend
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly_df["month"], y=monthly_df["revenue"],
        name="Revenue", line=dict(color=COLORS["accent"], width=2.5),
        fill="tozeroy", fillcolor="rgba(56,189,248,0.07)",
        mode="lines+markers", marker=dict(size=5)
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly_df["month"], y=monthly_df["profit"],
        name="Profit", line=dict(color=COLORS["profit"], width=2.5),
        mode="lines+markers", marker=dict(size=5)
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly_df["month"], y=monthly_df["leakage"],
        name="Leakage", line=dict(color=COLORS["loss"], width=1.5, dash="dot"),
        mode="lines+markers", marker=dict(size=4)
    ))
    fig_trend.update_layout(
        **PLOTLY_TEMPLATE["layout"].to_plotly_json(),
        title="Monthly Revenue, Profit & Leakage",
        hovermode="x unified"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_margin = px.line(
            monthly_df, x="month", y="margin_pct",
            title="Profit Margin % Over Time",
            labels={"margin_pct": "Margin %", "month": ""},
            markers=True, template=PLOTLY_TEMPLATE,
            color_discrete_sequence=[COLORS["warning"]]
        )
        fig_margin.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        st.plotly_chart(fig_margin, use_container_width=True)

    with col2:
        fig_orders = px.bar(
            monthly_df, x="month", y="orders",
            title="Monthly Order Volume",
            labels={"orders": "Orders", "month": ""},
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=[COLORS["accent"]]
        )
        st.plotly_chart(fig_orders, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 3 — DEEP DIVE
# ══════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-header'>Discount Impact Analysis</div>", unsafe_allow_html=True)

    discount_df = run_query(f"""
        SELECT
            CASE
                WHEN discount = 0        THEN '0% (No Discount)'
                WHEN discount <= 10      THEN '1–10%'
                WHEN discount <= 20      THEN '11–20%'
                ELSE '20%+'
            END AS discount_bucket,
            COUNT(*)                                                   AS orders,
            ROUND(AVG(profit), 2)                                      AS avg_profit,
            ROUND(SUM(profit)*100.0/NULLIF(SUM(sales_amount),0),2)    AS margin_pct,
            COUNT(CASE WHEN profit < 0 THEN 1 END)                    AS loss_orders
        FROM orders
        WHERE {WHERE}
        GROUP BY discount_bucket
        ORDER BY MIN(discount)
    """)

    col1, col2 = st.columns(2)
    with col1:
        fig_disc = px.bar(
            discount_df, x="discount_bucket", y="avg_profit",
            title="Avg Profit by Discount Band",
            color="avg_profit",
            color_continuous_scale=["#F87171", "#34D399"],
            template=PLOTLY_TEMPLATE,
            labels={"avg_profit": "Avg Profit (₹)", "discount_bucket": "Discount Band"}
        )
        fig_disc.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")
        fig_disc.update_coloraxes(showscale=False)
        st.plotly_chart(fig_disc, use_container_width=True)

    with col2:
        fig_loss_rate = px.bar(
            discount_df, x="discount_bucket", y="loss_orders",
            title="Loss-Making Orders by Discount Band",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=[COLORS["loss"]],
            labels={"loss_orders": "Loss Orders", "discount_bucket": "Discount Band"}
        )
        st.plotly_chart(fig_loss_rate, use_container_width=True)

    # Top leaking segments
    st.markdown("<div class='section-header'>Top Leaking Segments</div>", unsafe_allow_html=True)

    segment_df = run_query(f"""
        SELECT
            region || ' · ' || product_category AS segment,
            SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END)          AS leakage,
            COUNT(CASE WHEN profit < 0 THEN 1 END)                    AS loss_orders,
            ROUND(SUM(profit)*100.0/NULLIF(SUM(sales_amount),0),1)    AS margin_pct
        FROM orders
        WHERE {WHERE}
        GROUP BY region, product_category
        ORDER BY leakage ASC
        LIMIT 8
    """)

    fig_seg = px.bar(
        segment_df, x="leakage", y="segment",
        orientation="h",
        title="Worst Segments by Revenue Leakage",
        template=PLOTLY_TEMPLATE,
        color="leakage",
        color_continuous_scale=["#F87171", "#FBBF24"],
        labels={"leakage": "Total Leakage (₹)", "segment": ""}
    )
    fig_seg.update_coloraxes(showscale=False)
    st.plotly_chart(fig_seg, use_container_width=True)

    # Auto-generated insights
    st.markdown("<div class='section-header'>🤖 Auto Insights</div>", unsafe_allow_html=True)

    insights = run_query(f"""
        SELECT
            ROUND(AVG(discount), 2)                                              AS avg_discount,
            (SELECT product_category FROM orders WHERE {WHERE}
             GROUP BY product_category ORDER BY SUM(profit) ASC LIMIT 1)        AS worst_cat,
            (SELECT region FROM orders WHERE {WHERE}
             GROUP BY region ORDER BY SUM(profit) ASC LIMIT 1)                  AS worst_region,
            (SELECT product_category FROM orders WHERE {WHERE}
             GROUP BY product_category ORDER BY SUM(profit) DESC LIMIT 1)       AS best_cat,
            ROUND(SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END)*-1
                  /NULLIF(SUM(sales_amount),0)*100, 2)                           AS leakage_pct
        FROM orders
        WHERE {WHERE}
    """).iloc[0]

    st.markdown(f"""
    <div class='insight-card danger'>
        <span class='tag tag-danger'>Critical</span>
        <strong>{insights.worst_region}</strong> region combined with <strong>{insights.worst_cat}</strong> category
        is your worst-performing segment. Consider reviewing pricing or discount caps here first.
    </div>
    <div class='insight-card warning'>
        <span class='tag tag-warning'>Watch</span>
        Average discount across loss-making orders is <strong>{leakage.avg_discount_on_losses:.1f}%</strong>.
        Orders with discounts above 20% are disproportionately responsible for leakage.
    </div>
    <div class='insight-card success'>
        <span class='tag tag-success'>Strength</span>
        <strong>{insights.best_cat}</strong> is your highest-profit category.
        Prioritising this in marketing and inventory can offset losses elsewhere.
    </div>
    <div class='insight-card info'>
        <span class='tag tag-info'>Info</span>
        Overall leakage rate is <strong>{insights.leakage_pct:.2f}%</strong> of total revenue.
        Industry benchmark for retail is typically under 2% — use this to contextualise your performance.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — ORDERS TABLE
# ══════════════════════════════════════════════
with tab4:
    col1, col2 = st.columns([2, 1])
    with col1:
        view_mode = st.radio("Show", ["Loss-Making Orders", "All Orders"], horizontal=True)
    with col2:
        sort_col = st.selectbox("Sort by", ["profit", "sales_amount", "discount", "order_date"])

    profit_filter = "AND profit < 0" if view_mode == "Loss-Making Orders" else ""

    orders_df = run_query(f"""
        SELECT
            order_id,
            order_date,
            product_category       AS category,
            region,
            payment_method,
            ROUND(sales_amount, 2) AS revenue,
            ROUND(discount, 2)     AS discount_pct,
            ROUND(profit, 2)       AS profit
        FROM orders
        WHERE {WHERE}
        {profit_filter}
        ORDER BY {sort_col} ASC
        LIMIT 500
    """)

    st.dataframe(
        orders_df.style.applymap(
            lambda v: f"color: {COLORS['loss']}; font-weight:600" if isinstance(v, float) and v < 0 else "",
            subset=["profit"]
        ),
        use_container_width=True,
        height=450
    )

    st.caption(f"Showing {len(orders_df):,} orders (max 500) · sorted by {sort_col}")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style='display:flex; justify-content:space-between; color:{COLORS["muted"]}; font-size:0.75rem;'>
    <span>Revenue Intelligence Dashboard · Built with Streamlit, SQLite & Plotly</span>
    <span>arshyanawas · github.com/arshyanawas</span>
</div>
""", unsafe_allow_html=True)