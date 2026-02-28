# MongoDB Query Results

Run the load script first:

```bash
python task2/database/scripts/load_mongodb.py
```

Then run queries:

```bash
python task2/database/mongodb/queries.py
```

---

## Query 1: Latest Record

**Code:**
```python
coll.find_one(sort=[("order_date", -1)])
```

**Expected result:** Single document with the most recent order_date. Example:

```json
{
  "_id": ObjectId("..."),
  "order_date": ISODate("2024-12-31T00:00:00Z"),
  "product": { "name": "Printer", "category": "Office" },
  "region": "North",
  "quantity": 4,
  "sales": 3640.0,
  "profit": 348.93
}
```

---

## Query 2: Records by Date Range (2023)

**Code:**
```python
coll.find({"order_date": {"$gte": datetime(2023,1,1), "$lte": datetime(2023,12,31)}})
  .sort("order_date", 1).limit(20)
```

**Expected result:** Up to 20 documents from 2023, sorted by order_date.

---

## Query 3: Total Sales by Category (2023)

**Aggregation pipeline:**
```python
[
  {"$match": {"order_date": {"$gte": datetime(2023,1,1), "$lte": datetime(2023,12,31)}}},
  {"$group": {
    "_id": "$product.category",
    "order_count": {"$sum": 1},
    "total_quantity": {"$sum": "$quantity"},
    "total_sales": {"$sum": "$sales"},
    "total_profit": {"$sum": "$profit"},
  }},
  {"$sort": {"total_sales": -1}},
]
```

**Expected result:** One document per category (Accessories, Electronics, Office) with aggregated metrics.

---

## Query 4: Daily Aggregation (March 2024)

**Aggregation pipeline:**
```python
[
  {"$match": {"order_date": {"$gte": datetime(2024,3,1), "$lte": datetime(2024,3,31)}}},
  {"$group": {
    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$order_date"}},
    "daily_quantity": {"$sum": "$quantity"},
    "daily_sales": {"$sum": "$sales"},
    "daily_profit": {"$sum": "$profit"},
  }},
  {"$sort": {"_id": 1}},
]
```

**Expected result:** One document per day in March 2024 with daily totals.
