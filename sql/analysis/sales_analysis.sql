-- ============================================
-- Revenue Leakage & Profitability Analysis
-- ============================================

-- 1. KPI SUMMARY
SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        SUM(profit) * 100.0 / SUM(sales_amount),
        2
    ) AS profit_margin_pct
FROM orders;


-- 2. REGION-WISE PERFORMANCE
SELECT
    region,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY region
ORDER BY total_profit DESC;


-- 3. CATEGORY-WISE PERFORMANCE
SELECT
    product_category,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY product_category
ORDER BY total_profit DESC;


-- 4. REVENUE LEAKAGE ANALYSIS
SELECT
    COUNT(*) AS loss_orders,
    ROUND(SUM(profit), 2) AS total_loss
FROM orders
WHERE profit < 0;


-- 5. HIGH DISCOUNT IMPACT
SELECT
    product_category,
    ROUND(AVG(discount), 2) AS avg_discount,
    ROUND(AVG(profit), 2) AS avg_profit
FROM orders
GROUP BY product_category
ORDER BY avg_discount DESC;


-- 6. MONTHLY REVENUE & PROFIT TREND
SELECT
    strftime('%Y-%m', order_date) AS month,
    ROUND(SUM(sales_amount), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM orders
GROUP BY month
ORDER BY month;


-- 7. WORST PERFORMING REGIONS
SELECT
    region,
    ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY region
ORDER BY total_profit ASC
LIMIT 3;


-- 8. LOSS-MAKING ORDERS
SELECT
    order_id,
    order_date,
    region,
    product_category,
    sales_amount,
    discount,
    profit
FROM orders
WHERE profit < 0
ORDER BY profit ASC
LIMIT 10;


-- 9. REVENUE LEAKAGE PERCENTAGE
SELECT
    ROUND(
        ABS(SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END))
        * 100.0 /
        SUM(sales_amount),
        2
    ) AS leakage_percentage
FROM orders;


-- 10. TOP PERFORMING CATEGORY
SELECT
    product_category,
    ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY product_category
ORDER BY total_profit DESC
LIMIT 1;
