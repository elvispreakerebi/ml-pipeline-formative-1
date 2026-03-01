#!/usr/bin/env python3
"""
Load ecommerce_sales_data.csv into local MongoDB.
Creates the orders collection with embedded product documents.
"""
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from pymongo import MongoClient

# Project root (parent of task2/)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "ecommerce_sales_data.csv"

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass


def get_client():
    """Connect to local MongoDB using env vars or defaults."""
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    return MongoClient(uri)


def load_data():
    """Load CSV and insert into MongoDB."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    client = get_client()
    db_name = os.getenv("MONGODB_DATABASE", "ecommerce_sales")
    db = client[db_name]
    coll = db["orders"]

    # Clear existing documents
    coll.delete_many({})

    # Build documents
    documents = []
    for _, row in df.iterrows():
        doc = {
            "order_date": row["Order Date"],
            "product": {
                "name": row["Product Name"],
                "category": row["Category"],
            },
            "region": row["Region"],
            "quantity": int(row["Quantity"]),
            "sales": float(row["Sales"]),
            "profit": float(row["Profit"]),
        }
        documents.append(doc)

    coll.insert_many(documents)

    # Create indexes for time-series queries
    coll.create_index("order_date")
    coll.create_index([("order_date", 1), ("product.category", 1)])

    print(f"Loaded {len(documents)} documents into MongoDB {db_name}.orders")
    client.close()


if __name__ == "__main__":
    load_data()
