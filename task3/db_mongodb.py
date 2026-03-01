"""MongoDB database operations for Task 3."""
import os
from datetime import date, datetime
from pathlib import Path

from bson import ObjectId
from pymongo import MongoClient

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except ImportError:
    pass


def get_collection():
    """Get MongoDB orders collection."""
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DATABASE", "ecommerce_sales")
    return MongoClient(uri)[db_name]["orders"]


def _doc_to_order(doc: dict) -> dict:
    """Convert MongoDB doc to OrderResponse shape."""
    order_date = doc.get("order_date")
    if isinstance(order_date, datetime):
        order_date = order_date.date()
    return {
        "id": str(doc["_id"]),
        "order_date": order_date,
        "product_name": doc["product"]["name"],
        "category": doc["product"]["category"],
        "region": doc["region"],
        "quantity": doc["quantity"],
        "sales": float(doc["sales"]),
        "profit": float(doc["profit"]),
    }


def mongo_get_all(limit: int = 100) -> list[dict]:
    """Get all orders."""
    coll = get_collection()
    docs = coll.find().sort("order_date", -1).limit(limit)
    return [_doc_to_order(d) for d in docs]


def mongo_get_one(order_id: str) -> dict | None:
    """Get one order by _id."""
    if not ObjectId.is_valid(order_id):
        return None
    doc = get_collection().find_one({"_id": ObjectId(order_id)})
    return _doc_to_order(doc) if doc else None


def mongo_create(data: dict) -> dict:
    """Create order."""
    doc = {
        "order_date": datetime.combine(data["order_date"], datetime.min.time()),
        "product": {"name": data["product_name"], "category": data["category"]},
        "region": data["region"],
        "quantity": data["quantity"],
        "sales": data["sales"],
        "profit": data["profit"],
    }
    result = get_collection().insert_one(doc)
    return mongo_get_one(str(result.inserted_id))


def mongo_update(order_id: str, data: dict) -> dict | None:
    """Update order."""
    if not ObjectId.is_valid(order_id):
        return None
    existing = mongo_get_one(order_id)
    if not existing:
        return None

    updates = {k: v for k, v in data.items() if v is not None}
    if not updates:
        return existing

    set_doc = {}
    if "order_date" in updates:
        set_doc["order_date"] = datetime.combine(updates["order_date"], datetime.min.time())
    if "product_name" in updates or "category" in updates:
        product = existing.get("product", {}) or {}
        if "product_name" in updates:
            product["name"] = updates["product_name"]
        if "category" in updates:
            product["category"] = updates["category"]
        set_doc["product"] = product
    if "region" in updates:
        set_doc["region"] = updates["region"]
    if "quantity" in updates:
        set_doc["quantity"] = updates["quantity"]
    if "sales" in updates:
        set_doc["sales"] = updates["sales"]
    if "profit" in updates:
        set_doc["profit"] = updates["profit"]

    get_collection().update_one(
        {"_id": ObjectId(order_id)},
        {"$set": set_doc},
    )
    return mongo_get_one(order_id)


def mongo_delete(order_id: str) -> bool:
    """Delete order."""
    if not ObjectId.is_valid(order_id):
        return False
    result = get_collection().delete_one({"_id": ObjectId(order_id)})
    return result.deleted_count > 0


def mongo_get_latest() -> dict | None:
    """Get latest order by date."""
    doc = get_collection().find_one(sort=[("order_date", -1)])
    return _doc_to_order(doc) if doc else None


def mongo_get_by_date_range(start: date, end: date, limit: int = 100) -> list[dict]:
    """Get orders by date range."""
    start_dt = datetime.combine(start, datetime.min.time())
    end_dt = datetime.combine(end, datetime.max.time())
    docs = get_collection().find(
        {"order_date": {"$gte": start_dt, "$lte": end_dt}}
    ).sort("order_date", 1).limit(limit)
    return [_doc_to_order(d) for d in docs]
