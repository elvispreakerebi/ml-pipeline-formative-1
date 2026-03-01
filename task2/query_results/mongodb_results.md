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

**Result:**
```python
{'_id': '69a35067681963129a35a046', 'order_date': datetime(2024, 12, 31, 0, 0), 'product': {'name': 'Smartphone', 'category': 'Electronics'}, 'region': 'West', 'quantity': 6, 'sales': 930.0, 'profit': 213.6}
```

---

## Query 2: Records by Date Range (2023)

**Code:**
```python
coll.find({"order_date": {"$gte": datetime(2023,1,1), "$lte": datetime(2023,12,31)}})
  .sort("order_date", 1).limit(20)
```

**Result:** Multiple documents from 2023, sorted by order_date (first 5 shown in output).

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

**Result:**
```
{'_id': 'Electronics', 'order_count': 604, 'total_quantity': 2919, 'total_sales': 1881367.0, 'total_profit': 331270.15}
{'_id': 'Accessories', 'order_count': 470, 'total_quantity': 2333, 'total_sales': 1495723.0, 'total_profit': 261626.94}
{'_id': 'Office', 'order_count': 130, 'total_quantity': 673, 'total_sales': 409502.0, 'total_profit': 73969.33}
```

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

**Result:** One document per day in March 2024 with daily_quantity, daily_sales, daily_profit (25 days with data).
