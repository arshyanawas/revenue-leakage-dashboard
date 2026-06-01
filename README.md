![Python](https://img.shields.io/badge/Python-3.11-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Business Intelligence](https://img.shields.io/badge/Domain-Business_Intelligence-green)
![SQL](https://img.shields.io/badge/SQL-Analytics-blue)

[![Live App](https://img.shields.io/badge/Streamlit-Live_App-red)](https://arshya-profitability-analytics.streamlit.app/)

# Revenue Leakage & Profitability Analytics Dashboard

**Business Problem:** A business generating ₹2.55 Cr in revenue is still only retaining ₹74.94 L in profit — a 29.37% margin with hidden leakage driven by excessive discounting and loss-making transactions.

**What this project does:** Uses SQL to locate exactly where profit is being lost, which discount bands destroy margin, and which region–category combinations are the worst offenders — then surfaces it in an interactive dashboard.

---

## Live Demo

https://arshya-profitability-analytics.streamlit.app/

---

## Key Numbers

| Metric | Value |
|---|---|
| Total Revenue | ₹2.55 Cr |
| Total Profit | ₹74.94 L |
| Profit Margin | 29.37% |
| Loss-Making Orders | 13 |
| Avg Discount on Loss Orders | Analysed by discount band |

---

## Business Questions Answered

1. Which region–category combinations are leaking the most money?
2. At what discount level does profit turn negative?
3. Does revenue growth actually translate into profit growth month-on-month?
4. Which payment methods have the worst profit margins?
5. Which single segment should be fixed first to recover the most leakage?

---

## SQL Investigation

All analysis is SQL-first. The Streamlit dashboard runs live `pd.read_sql_query()` calls against a SQLite database — no pre-aggregated DataFrames.

### KPI Summary

```sql
SELECT
    SUM(sales_amount)                                        AS total_revenue,
    SUM(profit)                                              AS total_profit,
    ROUND(SUM(profit) * 100.0 / NULLIF(SUM(sales_amount),0), 2) AS margin_pct,
    COUNT(*)                                                 AS total_orders,
    COUNT(DISTINCT customer_id)                              AS unique_customers,
    ROUND(AVG(sales_amount), 2)                              AS avg_order_value
FROM orders;
```

---

### Revenue Leakage — Loss-Making Orders

```sql
SELECT *
FROM orders
WHERE profit < 0
ORDER BY profit ASC;
```

13 transactions are loss-making. These are the highest-priority targets for operational review.

---

### Discount Band Analysis

```sql
SELECT
    CASE
        WHEN discount = 0   THEN '0% (No Discount)'
        WHEN discount <= 10 THEN '1–10%'
        WHEN discount <= 20 THEN '11–20%'
        ELSE '20%+'
    END AS discount_bucket,
    COUNT(*)                                                   AS orders,
    ROUND(AVG(profit), 2)                                      AS avg_profit,
    ROUND(SUM(profit)*100.0/NULLIF(SUM(sales_amount),0),2)    AS margin_pct,
    COUNT(CASE WHEN profit < 0 THEN 1 END)                    AS loss_orders
FROM orders
GROUP BY discount_bucket
ORDER BY MIN(discount);
```

Orders with discounts above 20% are disproportionately responsible for leakage. This query quantifies exactly how much margin each discount tier destroys.

---

### Worst Segments by Leakage

```sql
SELECT
    region || ' · ' || product_category AS segment,
    SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END) AS leakage,
    COUNT(CASE WHEN profit < 0 THEN 1 END)           AS loss_orders,
    ROUND(SUM(profit)*100.0/NULLIF(SUM(sales_amount),0),1) AS margin_pct
FROM orders
GROUP BY region, product_category
ORDER BY leakage ASC
LIMIT 8;
```

Identifies the specific region–category combinations responsible for the most leakage. Actionable at a segment level, not just a category level.

---

### Profit Margin Heatmap — Region × Category

```sql
SELECT
    region,
    product_category,
    ROUND(SUM(profit)*100.0/NULLIF(SUM(sales_amount),0),1) AS margin_pct
FROM orders
GROUP BY region, product_category;
```

Pivoted into a heatmap in the dashboard. Instantly shows which intersections are profitable vs bleeding.

---

### Regional Performance

```sql
SELECT
    region,
    SUM(sales_amount) AS total_sales,
    SUM(profit)       AS total_profit,
    ROUND(SUM(profit)*100.0/NULLIF(SUM(sales_amount),0),1) AS margin_pct
FROM orders
GROUP BY region
ORDER BY total_profit DESC;
```

---

### Monthly Trend — Revenue, Profit & Leakage

```sql
SELECT
    strftime('%Y-%m', order_date)                           AS month,
    SUM(sales_amount)                                       AS revenue,
    SUM(profit)                                             AS profit,
    SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END)       AS leakage,
    ROUND(SUM(profit)*100.0/NULLIF(SUM(sales_amount),0),2) AS margin_pct
FROM orders
GROUP BY month
ORDER BY month;
```

Revenue is stable month-on-month. Profit fluctuates — confirming leakage is not a seasonal issue but a structural one tied to discounting behaviour.

---

## Dashboard

![Dashboard](revenue-leakage-profitability-analytics/visualizations/Dashboard.png)

**Four tabs:**
- **Breakdown** — Revenue vs Profit by category, margin heatmap by region × category, payment method analysis
- **Trends** — Monthly revenue, profit and leakage on a single chart, margin % over time, order volume
- **Deep Dive** — Discount band impact, worst leaking segments ranked, auto-generated insight cards
- **Orders** — Filterable table of all orders or loss-making orders only, colour-coded by profit

---

## Findings

- Overall margin is 29.37% but hides segment-level variance — some region–category pairs are significantly below average
- Loss-making orders are concentrated in high-discount transactions (20%+)
- Revenue is evenly split across categories (~25% each) but profit is not — the margin heatmap reveals the real picture
- Monthly revenue is stable; profit dips correlate with discount spikes, not revenue drops

## Recommendations

- **Cap discounts at 20%** — orders above this threshold account for a disproportionate share of losses
- **Investigate the 13 loss-making orders** — identify if they share a salesperson, customer, or promotion
- **Use margin % as the primary KPI**, not revenue — the two move independently month-on-month
- **Prioritise the worst region–category segment** identified in the deep dive tab for immediate pricing review

---

## Tech Stack

- Python 3.11
- SQLite (migrated from MySQL for deployment compatibility)
- SQL — all aggregations and filters run as live queries via `pd.read_sql_query()`
- Streamlit
- Plotly
- Pandas

---

## Running the Project

```bash
git clone https://github.com/arshyanawas/revenue-leakage-dashboard
cd revenue-leakage-profitability-analytics
pip install -r requirements.txt
python scripts/create_database.py   # builds data/sales.db from CSV
streamlit run dashboard/app.py
```