"""MySQL database connection and operations for Task 3."""
import os
from contextlib import contextmanager
from datetime import date
from pathlib import Path

import pymysql

try:
    from dotenv import load_dotenv
    # .env is in project root (parent of task3)
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except ImportError:
    pass


def get_connection():
    """Get MySQL connection."""
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3307")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "task2local"),
        database=os.getenv("MYSQL_DATABASE", "ecommerce_sales"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


@contextmanager
def mysql_cursor():
    """Context manager for MySQL cursor."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            yield cur
        conn.commit()
    finally:
        conn.close()


def _resolve_product_id(cur, product_name: str, category: str) -> int:
    """Get or create product and return product_id."""
    cur.execute(
        "SELECT category_id FROM categories WHERE category_name = %s",
        (category,),
    )
    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO categories (category_name) VALUES (%s)", (category,))
        category_id = cur.lastrowid
    else:
        category_id = row["category_id"]

    cur.execute(
        "SELECT product_id FROM products WHERE product_name = %s AND category_id = %s",
        (product_name, category_id),
    )
    row = cur.fetchone()
    if not row:
        cur.execute(
            "INSERT INTO products (product_name, category_id) VALUES (%s, %s)",
            (product_name, category_id),
        )
        return cur.lastrowid
    return row["product_id"]


def _resolve_region_id(cur, region: str) -> int:
    """Get or create region and return region_id."""
    cur.execute("SELECT region_id FROM regions WHERE region_name = %s", (region,))
    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO regions (region_name) VALUES (%s)", (region,))
        return cur.lastrowid
    return row["region_id"]


def _row_to_order(row: dict) -> dict:
    """Convert MySQL row to OrderResponse shape."""
    return {
        "id": row["order_id"],
        "order_date": row["order_date"],
        "product_name": row["product_name"],
        "category": row["category_name"],
        "region": row["region_name"],
        "quantity": row["quantity"],
        "sales": float(row["sales"]),
        "profit": float(row["profit"]),
    }


def mysql_get_all(limit: int = 100) -> list[dict]:
    """Get all orders (with joins)."""
    with mysql_cursor() as cur:
        cur.execute("""
            SELECT o.order_id, o.order_date, o.quantity, o.sales, o.profit,
                   p.product_name, c.category_name, r.region_name
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            JOIN categories c ON p.category_id = c.category_id
            JOIN regions r ON o.region_id = r.region_id
            ORDER BY o.order_date DESC, o.order_id DESC
            LIMIT %s
        """, (limit,))
        return [_row_to_order(r) for r in cur.fetchall()]


def mysql_get_one(order_id: int) -> dict | None:
    """Get one order by id."""
    with mysql_cursor() as cur:
        cur.execute("""
            SELECT o.order_id, o.order_date, o.quantity, o.sales, o.profit,
                   p.product_name, c.category_name, r.region_name
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            JOIN categories c ON p.category_id = c.category_id
            JOIN regions r ON o.region_id = r.region_id
            WHERE o.order_id = %s
        """, (order_id,))
        row = cur.fetchone()
        return _row_to_order(row) if row else None


def mysql_create(data: dict) -> dict:
    """Create order."""
    with mysql_cursor() as cur:
        product_id = _resolve_product_id(cur, data["product_name"], data["category"])
        region_id = _resolve_region_id(cur, data["region"])
        cur.execute(
            """INSERT INTO orders (order_date, product_id, region_id, quantity, sales, profit)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                data["order_date"],
                product_id,
                region_id,
                data["quantity"],
                data["sales"],
                data["profit"],
            ),
        )
        order_id = cur.lastrowid
    return mysql_get_one(order_id)


def mysql_update(order_id: int, data: dict) -> dict | None:
    """Update order."""
    existing = mysql_get_one(order_id)
    if not existing:
        return None

    updates = {k: v for k, v in data.items() if v is not None}
    if not updates:
        return existing

    with mysql_cursor() as cur:
        if "product_name" in updates or "category" in updates:
            product_id = _resolve_product_id(
                cur,
                updates.get("product_name", existing["product_name"]),
                updates.get("category", existing["category"]),
            )
            updates["product_id"] = product_id
        if "region" in updates:
            updates["region_id"] = _resolve_region_id(cur, updates["region"])

        set_parts = []
        params = []
        for k, v in updates.items():
            if k == "order_date":
                set_parts.append("order_date = %s")
                params.append(v)
            elif k == "product_id":
                set_parts.append("product_id = %s")
                params.append(v)
            elif k == "region_id":
                set_parts.append("region_id = %s")
                params.append(v)
            elif k == "quantity":
                set_parts.append("quantity = %s")
                params.append(v)
            elif k == "sales":
                set_parts.append("sales = %s")
                params.append(v)
            elif k == "profit":
                set_parts.append("profit = %s")
                params.append(v)

        if set_parts:
            params.append(order_id)
            cur.execute(
                f"UPDATE orders SET {', '.join(set_parts)} WHERE order_id = %s",
                params,
            )

    return mysql_get_one(order_id)


def mysql_delete(order_id: int) -> bool:
    """Delete order."""
    with mysql_cursor() as cur:
        cur.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        return cur.rowcount > 0


def mysql_get_latest() -> dict | None:
    """Get latest order by date."""
    with mysql_cursor() as cur:
        cur.execute("""
            SELECT o.order_id, o.order_date, o.quantity, o.sales, o.profit,
                   p.product_name, c.category_name, r.region_name
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            JOIN categories c ON p.category_id = c.category_id
            JOIN regions r ON o.region_id = r.region_id
            ORDER BY o.order_date DESC, o.order_id DESC
            LIMIT 1
        """)
        row = cur.fetchone()
        return _row_to_order(row) if row else None


def mysql_get_by_date_range(start: date, end: date, limit: int = 100) -> list[dict]:
    """Get orders by date range."""
    with mysql_cursor() as cur:
        cur.execute("""
            SELECT o.order_id, o.order_date, o.quantity, o.sales, o.profit,
                   p.product_name, c.category_name, r.region_name
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            JOIN categories c ON p.category_id = c.category_id
            JOIN regions r ON o.region_id = r.region_id
            WHERE o.order_date BETWEEN %s AND %s
            ORDER BY o.order_date, o.order_id
            LIMIT %s
        """, (start, end, limit))
        return [_row_to_order(r) for r in cur.fetchall()]
