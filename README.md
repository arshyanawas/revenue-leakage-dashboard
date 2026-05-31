![Python](https://img.shields.io/badge/Python-3.11-blue)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Business Intelligence](https://img.shields.io/badge/Domain-Business_Intelligence-green)
![SQL](https://img.shields.io/badge/SQL-Analytics-blue)

[![Live App](https://img.shields.io/badge/Streamlit-Live_App-red)](https://arshya-profitability-analytics.streamlit.app/)
# Revenue Leakage & Profitability Analytics Dashboard


**Problem:** High revenue but low profitability due to hidden leakage.

**Solution:** Identified loss-making transactions, discount impact, and regional imbalance using SQL + dashboarding.

## Executive Summary

This project focuses on identifying revenue leakage and profitability gaps using SQL and an interactive Streamlit dashboard. The analysis highlights loss-making transactions, the impact of discounting, and regional performance differences, with the goal of supporting more informed business decisions.

## Business Problem

Many businesses generate strong revenue but still struggle with profitability due to hidden leakages. These leakages often arise from excessive discounting, loss-making transactions, and uneven regional performance. The objective of this project is to identify where profits are being lost and suggest ways to improve overall financial performance.

## Tech Stack

The project was built using Python for data processing and dashboarding, MySQL for data storage and querying, Plotly for visualization, and dotenv for secure handling of database credentials.

# Analysis & Insights

## Sales Across India

![Sales Map](revenue-leakage-profitability-analytics/visualizations/Map.png)

**Path:**

```text
revenue-leakage-profitability-analytics/visualizations/Map.png
```

**Data Used:**

Region-wise sales data was aggregated from MySQL using a group by operation on the region field along with a sum of sales amount.

**Insight:**

The distribution of sales across regions is uneven, with certain regions contributing a significantly larger portion of total revenue.

**Interpretation:**

This indicates a dependency on a few key regions, which introduces risk and limits the business’s ability to scale evenly across markets.

**Mitigation:**

A more balanced regional strategy can be developed by investing in underperforming regions through targeted campaigns and better understanding of local demand patterns.

---

## Revenue Distribution by Category

![Donut](revenue-leakage-profitability-analytics/visualizations/Donut.png)

**Path:**

```text
revenue-leakage-profitability-analytics/visualizations/Donut.png
```

**Data Used:**

Revenue was grouped by product category to understand how different segments contribute to total sales.

**Insight:**

Revenue appears to be fairly distributed across categories, with no single category dominating the overall contribution.

**Interpretation:**

While diversification reduces dependency on a single category, it may also conceal categories that generate lower margins despite contributing to revenue.

**Mitigation:**

Revenue analysis should be paired with profitability metrics to identify which categories truly drive value, allowing better pricing and inventory decisions.

---

## Profit by Category

![Bar](revenue-leakage-profitability-analytics/visualizations/Bar.png)

**Path:**

```text
revenue-leakage-profitability-analytics/visualizations/Bar.png
```

**Data Used:**

Profit values were aggregated at the product category level to compare performance across segments.

**Insight:**

Certain categories generate noticeably lower profit despite having similar revenue levels.

**Interpretation:**

This suggests inefficiencies in pricing, discounting, or cost management within specific categories.

**Mitigation:**

Reducing unnecessary discounts and optimizing pricing strategies in low-margin categories can improve overall profitability.

---

## Monthly Revenue & Profit Trend

![Line](revenue-leakage-profitability-analytics/visualizations/Line.png)

**Path:**

```text
revenue-leakage-profitability-analytics/visualizations/Line.png
```

**Data Used:**

Sales and profit were aggregated on a monthly basis to observe trends over time.

**Insight:**

Revenue remains relatively stable across months, while profit shows noticeable fluctuations.

**Interpretation:**

Stable revenue combined with inconsistent profit indicates variability in cost structures or discounting practices.

**Mitigation:**

Implementing consistent discount policies and monitoring profitability alongside revenue can help stabilize financial performance.

---

## Full Dashboard

![Dashboard](revenue-leakage-profitability-analytics/visualizations/Dashboard.png)

**Path:**

```text
revenue-leakage-profitability-analytics/visualizations/Dashboard.png
```

**Description:**

The dashboard brings together key performance indicators, filters, and visualizations into a single interface, allowing users to interactively explore revenue, profit, and loss trends.

---

## Key Findings

The analysis shows that high discount levels have a direct impact on profitability, especially when they exceed reasonable thresholds. There is also a consistent presence of loss-making transactions, which contributes to revenue leakage. Profit trends do not always align with revenue patterns, indicating inefficiencies in cost or pricing strategies. Additionally, regional imbalance suggests that certain markets are underutilized.

###  Key Insights
- High discounts → direct profit loss
- Loss-making transactions consistently present
- Profit ≠ Revenue (misleading business metric)
- Regional imbalance affects scalability

## Strategic Recommendations

Improving profitability requires a shift from focusing solely on revenue to emphasizing margin-based decision-making. Discounting should be controlled through defined limits, and loss-making transactions should be identified and minimized. Strengthening performance in weaker regions and optimizing category-level pricing can further enhance overall business performance.

## How to Run

Clone the repository, install the required dependencies, and create a `.env` file with your database credentials. Load the dataset into MySQL using the provided ingestion script, and then run the Streamlit dashboard to interact with the analysis.

## Challenges

One of the main challenges was ensuring secure handling of database credentials while maintaining ease of use. Data consistency, particularly with date formats and aggregation logic, required careful handling. Additionally, aligning revenue-focused insights with profitability metrics required thoughtful analysis.

## Future Improvements

The project can be extended by integrating real-time data pipelines and adding predictive analytics for forecasting. 

## NOTE - SQL was used for data extraction, transformation, and business analysis before powering the Streamlit dashboard.







