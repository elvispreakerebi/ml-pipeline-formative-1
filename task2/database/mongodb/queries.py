#!/usr/bin/env python3
"""
MongoDB queries for ecommerce sales time-series data.
Run after loading data with load_mongodb.py.
"""
import os
from datetime import datetime
from pathlib import Path

from pymongo import MongoClient

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[3] / ".env")
except ImportError:
    pass


def get_db():
    """Connect to MongoDB and return database."""
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DATABASE", "ecommerce_sales")
    return MongoClient(uri)[db_name]


def run_queries():
    """Execute and print all required queries."""
    db = get_db()
    coll = db["orders"]

    # Query 1: Latest record
    print("=== Query 1: Latest record ===\n")
    latest = coll.find_one(sort=[("order_date", -1)])
    if latest:
        latest["_id"] = str(latest["_id"])
        print(latest)
    print()

    # Query 2: Records by date range (2023)
    print("=== Query 2: Records by date range (2023) ===\n")
    start = datetime(2023, 1, 1)
    end = datetime(2023, 12, 31, 23, 59, 59)
    for doc in coll.find(
        {"order_date": {"$gte": start, "$lte": end}}
    ).sort("order_date", 1).limit(5):
        doc["_id"] = str(doc["_id"])
        print(doc)
    print("... (showing first 5 of many)\n")

    # Query 3: Total sales by product category (2023)
    print("=== Query 3: Total sales by category (2023) ===\n")
    pipeline = [
        {"$match": {"order_date": {"$gte": datetime(2023, 1, 1), "$lte": datetime(2023, 12, 31)}}},
        {"$group": {
            "_id": "$product.category",
            "order_count": {"$sum": 1},
            "total_quantity": {"$sum": "$quantity"},
            "total_sales": {"$sum": "$sales"},
            "total_profit": {"$sum": "$profit"},
        }},
        {"$sort": {"total_sales": -1}},
    ]
    for doc in coll.aggregate(pipeline):
        print(doc)
    print()

    # Query 4: Documents for a specific month (March 2024), sorted by date
    print("=== Query 4: Daily aggregation for March 2024 ===\n")
    pipeline = [
        {"$match": {"order_date": {"$gte": datetime(2024, 3, 1), "$lte": datetime(2024, 3, 31)}}},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$order_date"}},
            "daily_quantity": {"$sum": "$quantity"},
            "daily_sales": {"$sum": "$sales"},
            "daily_profit": {"$sum": "$profit"},
        }},
        {"$sort": {"_id": 1}},
    ]
    for doc in coll.aggregate(pipeline):
        print(doc)


if __name__ == "__main__":
    run_queries()
