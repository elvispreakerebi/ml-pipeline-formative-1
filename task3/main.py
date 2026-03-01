"""
Task 3: CRUD and Time-Series Query API
Endpoints for MySQL and MongoDB (Task 2 databases).
"""
from datetime import date

from fastapi import FastAPI, HTTPException, Query

from task3.models import OrderCreate, OrderResponse, OrderUpdate
from task3 import db_mysql, db_mongodb

app = FastAPI(
    title="Ecommerce Sales API",
    description="Task 3: CRUD and time-series endpoints for MySQL and MongoDB",
    version="1.0.0",
)


# ---------- MySQL Endpoints ----------

@app.get("/mysql/orders", response_model=list[OrderResponse])
def mysql_list_orders(limit: int = Query(100, ge=1, le=500)):
    """GET: List orders from MySQL."""
    return db_mysql.mysql_get_all(limit=limit)


@app.get("/mysql/orders/query/latest", response_model=OrderResponse)
def mysql_latest_order():
    """GET: Latest record (time-series endpoint)."""
    order = db_mysql.mysql_get_latest()
    if not order:
        raise HTTPException(status_code=404, detail="No orders found")
    return order


@app.get("/mysql/orders/query/date-range", response_model=list[OrderResponse])
def mysql_orders_by_date_range(
    start: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end: date = Query(..., description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=500),
):
    """GET: Records by date range (time-series endpoint)."""
    if start > end:
        raise HTTPException(status_code=400, detail="start must be <= end")
    return db_mysql.mysql_get_by_date_range(start, end, limit=limit)


@app.get("/mysql/orders/{order_id}", response_model=OrderResponse)
def mysql_get_order(order_id: int):
    """GET: Get one order from MySQL by id."""
    order = db_mysql.mysql_get_one(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/mysql/orders", response_model=OrderResponse, status_code=201)
def mysql_create_order(order: OrderCreate):
    """POST: Create order in MySQL."""
    return db_mysql.mysql_create(order.model_dump())


@app.put("/mysql/orders/{order_id}", response_model=OrderResponse)
def mysql_update_order(order_id: int, order: OrderUpdate):
    """PUT: Update order in MySQL."""
    result = db_mysql.mysql_update(order_id, order.model_dump(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return result


@app.delete("/mysql/orders/{order_id}", status_code=204)
def mysql_delete_order(order_id: int):
    """DELETE: Delete order from MySQL."""
    if not db_mysql.mysql_delete(order_id):
        raise HTTPException(status_code=404, detail="Order not found")


# ---------- MongoDB Endpoints ----------

@app.get("/mongodb/orders", response_model=list[OrderResponse])
def mongo_list_orders(limit: int = Query(100, ge=1, le=500)):
    """GET: List orders from MongoDB."""
    return db_mongodb.mongo_get_all(limit=limit)


@app.get("/mongodb/orders/query/latest", response_model=OrderResponse)
def mongo_latest_order():
    """GET: Latest record (time-series endpoint)."""
    order = db_mongodb.mongo_get_latest()
    if not order:
        raise HTTPException(status_code=404, detail="No orders found")
    return order


@app.get("/mongodb/orders/query/date-range", response_model=list[OrderResponse])
def mongo_orders_by_date_range(
    start: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end: date = Query(..., description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=500),
):
    """GET: Records by date range (time-series endpoint)."""
    if start > end:
        raise HTTPException(status_code=400, detail="start must be <= end")
    return db_mongodb.mongo_get_by_date_range(start, end, limit=limit)


@app.get("/mongodb/orders/{order_id}", response_model=OrderResponse)
def mongo_get_order(order_id: str):
    """GET: Get one order from MongoDB by _id."""
    order = db_mongodb.mongo_get_one(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/mongodb/orders", response_model=OrderResponse, status_code=201)
def mongo_create_order(order: OrderCreate):
    """POST: Create order in MongoDB."""
    return db_mongodb.mongo_create(order.model_dump())


@app.put("/mongodb/orders/{order_id}", response_model=OrderResponse)
def mongo_update_order(order_id: str, order: OrderUpdate):
    """PUT: Update order in MongoDB."""
    result = db_mongodb.mongo_update(order_id, order.model_dump(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return result


@app.delete("/mongodb/orders/{order_id}", status_code=204)
def mongo_delete_order(order_id: str):
    """DELETE: Delete order from MongoDB."""
    if not db_mongodb.mongo_delete(order_id):
        raise HTTPException(status_code=404, detail="Order not found")


# ---------- Health ----------

@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}
