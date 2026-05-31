-- Remove duplicates
DELETE FROM orders
WHERE order_id NOT IN (
    SELECT MIN(order_id)
    FROM orders
    GROUP BY order_id
);