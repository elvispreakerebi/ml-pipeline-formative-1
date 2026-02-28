#!/usr/bin/env python3
"""
Load ecommerce_sales_data.csv into local MySQL.
Run schema.sql first to create the database and tables.
"""
import os
from pathlib import Path

import pandas as pd
import pymysql
# Project root (parent of task2/)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "ecommerce_sales_data.csv"

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass


def get_connection():
    """Connect to local MySQL using env vars or defaults."""
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "ecommerce_sales"),
        charset="utf8mb4",
    )


def load_data():
    """Load CSV and insert into MySQL."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df["Order Date"] = pd.to_datetime(df["Order Date"]).dt.date

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Clear existing data (optional, for re-runs)
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            cur.execute("TRUNCATE TABLE orders")
            cur.execute("TRUNCATE TABLE products")
            cur.execute("TRUNCATE TABLE regions")
            cur.execute("TRUNCATE TABLE categories")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")

            # Insert categories
            categories = df["Category"].unique().tolist()
            for cat in categories:
                cur.execute(
                    "INSERT IGNORE INTO categories (category_name) VALUES (%s)",
                    (cat,),
                )
            cur.execute("SELECT category_id, category_name FROM categories")
            cat_map = {row[1]: row[0] for row in cur.fetchall()}

            # Insert regions
            regions = df["Region"].unique().tolist()
            for reg in regions:
                cur.execute(
                    "INSERT IGNORE INTO regions (region_name) VALUES (%s)",
                    (reg,),
                )
            cur.execute("SELECT region_id, region_name FROM regions")
            reg_map = {row[1]: row[0] for row in cur.fetchall()}

            # Insert products (product_name, category_id)
            product_keys = df[["Product Name", "Category"]].drop_duplicates()
            for _, row in product_keys.iterrows():
                cur.execute(
                    """INSERT IGNORE INTO products (product_name, category_id)
                       VALUES (%s, %s)""",
                    (row["Product Name"], cat_map[row["Category"]]),
                )
            cur.execute("SELECT product_id, product_name, category_id FROM products")
            prod_map = {
                (row[1], row[2]): row[0] for row in cur.fetchall()
            }

            # Insert orders
            for _, row in df.iterrows():
                pid = prod_map[(row["Product Name"], cat_map[row["Category"]])]
                rid = reg_map[row["Region"]]
                cur.execute(
                    """INSERT INTO orders (order_date, product_id, region_id, quantity, sales, profit)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (
                        row["Order Date"],
                        pid,
                        rid,
                        int(row["Quantity"]),
                        float(row["Sales"]),
                        float(row["Profit"]),
                    ),
                )

        conn.commit()
        print(f"Loaded {len(df)} orders into MySQL.")
    finally:
        conn.close()


if __name__ == "__main__":
    load_data()
