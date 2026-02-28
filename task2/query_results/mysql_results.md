# MySQL Query Results

Run the schema and load data first:

```bash
mysql -u root < task2/database/sql/schema.sql
python task2/database/scripts/load_mysql.py
```

Then execute queries from `task2/database/sql/queries.sql`.

---

## Query 1: Latest Record

**SQL:**
```sql
SELECT o.order_id, o.order_date, p.product_name, c.category_name, r.region_name,
       o.quantity, o.sales, o.profit
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
JOIN regions r ON o.region_id = r.region_id
ORDER BY o.order_date DESC, o.order_id DESC
LIMIT 1;
```

**Result:**
| order_id | order_date | product_name | category_name | region_name | quantity | sales | profit |
|----------|------------|--------------|---------------|-------------|----------|-------|--------|
| 1175     | 2024-12-31 | Smartphone   | Electronics   | West        | 6        | 930.00| 213.60 |

---

## Query 2: Records by Date Range (2023)

**SQL:**
```sql
SELECT o.order_id, o.order_date, p.product_name, c.category_name, r.region_name,
       o.quantity, o.sales, o.profit
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
JOIN regions r ON o.region_id = r.region_id
WHERE o.order_date BETWEEN '2023-01-01' AND '2023-12-31'
ORDER BY o.order_date, o.order_id
LIMIT 20;
```

**Result:** 20 orders from 2023 (sample: Keyboard/Printer/Camera/Smartphone on 2023-01-01, Mouse/Laptop on 2023-01-02, etc.).

---

## Query 3: Total Sales by Category (2023)

**SQL:**
```sql
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
```

**Result:**
| category_name | order_count | total_quantity | total_sales | total_profit |
|---------------|-------------|----------------|-------------|--------------|
| Electronics   | 604         | 2919           | 1881367.00  | 331270.15    |
| Accessories   | 470         | 2333           | 1495723.00  | 261626.94    |
| Office        | 130         | 673            | 409502.00   | 73969.33     |

---

## Query 4: Daily Sales (March 2024)

**SQL:**
```sql
SELECT o.order_date,
       SUM(o.quantity) AS daily_quantity,
       SUM(o.sales) AS daily_sales,
       SUM(o.profit) AS daily_profit
FROM orders o
WHERE o.order_date BETWEEN '2024-03-01' AND '2024-03-31'
GROUP BY o.order_date
ORDER BY o.order_date;
```

**Result:** 25 days in March 2024 with daily_quantity, daily_sales, daily_profit (e.g. 2024-03-01: 14 units, 9444 sales; 2024-03-04: 47 units, 37581 sales).
