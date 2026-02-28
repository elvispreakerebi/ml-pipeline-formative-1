-- Task 2: MySQL Queries for Ecommerce Sales
-- Run these after loading data with load_mysql.py

USE ecommerce_sales;

-- Query 1: Latest record (most recent order by date)
SELECT o.order_id, o.order_date, p.product_name, c.category_name, r.region_name,
       o.quantity, o.sales, o.profit
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
JOIN regions r ON o.region_id = r.region_id
ORDER BY o.order_date DESC, o.order_id DESC
LIMIT 1;

-- Query 2: Records by date range (e.g., 2023-01-01 to 2023-12-31)
SELECT o.order_id, o.order_date, p.product_name, c.category_name, r.region_name,
       o.quantity, o.sales, o.profit
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
JOIN regions r ON o.region_id = r.region_id
WHERE o.order_date BETWEEN '2023-01-01' AND '2023-12-31'
ORDER BY o.order_date, o.order_id
LIMIT 20;

-- Query 3: Aggregation - Total sales by category for a given period (2023)
SELECT c.category_name,
       COUNT(o.order_id) AS order_count,
       SUM(o.quantity) AS total_quantity,
       SUM(o.sales) AS total_sales,
       SUM(o.profit) AS total_profit
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
WHERE o.order_date BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY c.category_name
ORDER BY total_sales DESC;

-- Query 4: Time-series - Daily sales totals for a specific month (March 2024)
SELECT o.order_date,
       SUM(o.quantity) AS daily_quantity,
       SUM(o.sales) AS daily_sales,
       SUM(o.profit) AS daily_profit
FROM orders o
WHERE o.order_date BETWEEN '2024-03-01' AND '2024-03-31'
GROUP BY o.order_date
ORDER BY o.order_date;
