-- Total Revenue
SELECT SUM(revenue) AS total_revenue FROM orders;

-- Revenue by Category
SELECT category, SUM(revenue) AS revenue
FROM orders
GROUP BY category
ORDER BY revenue DESC;

-- Top 5 Products
SELECT product, SUM(revenue) AS revenue
FROM orders
GROUP BY product
ORDER BY revenue DESC
LIMIT 5;