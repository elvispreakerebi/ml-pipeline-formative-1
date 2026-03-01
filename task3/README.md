# Task 3: CRUD and Time-Series Query API

API endpoints for the Task 2 databases (MySQL and MongoDB). Implements full CRUD and required time-series query endpoints.

## Prerequisites

- MySQL and MongoDB running (see [Task 2 SETUP](../task2/SETUP.md))
- Data loaded via Task 2 scripts
- `.env` in project root with `MYSQL_*` and `MONGODB_*` vars

## Run the API

From project root (ensure MySQL and MongoDB are running first):

```bash
pip install -r requirements.txt
python -m uvicorn task3.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### MySQL

| Method | Path | Description |
|--------|------|-------------|
| GET | `/mysql/orders` | List orders |
| GET | `/mysql/orders/{id}` | Get one order |
| POST | `/mysql/orders` | Create order |
| PUT | `/mysql/orders/{id}` | Update order |
| DELETE | `/mysql/orders/{id}` | Delete order |
| GET | `/mysql/orders/query/latest` | **Latest record** |
| GET | `/mysql/orders/query/date-range?start=...&end=...` | **Records by date range** |

### MongoDB

| Method | Path | Description |
|--------|------|-------------|
| GET | `/mongodb/orders` | List orders |
| GET | `/mongodb/orders/{id}` | Get one order |
| POST | `/mongodb/orders` | Create order |
| PUT | `/mongodb/orders/{id}` | Update order |
| DELETE | `/mongodb/orders/{id}` | Delete order |
| GET | `/mongodb/orders/query/latest` | **Latest record** |
| GET | `/mongodb/orders/query/date-range?start=...&end=...` | **Records by date range** |

### Example: Create order (POST body)

```json
{
  "order_date": "2024-01-15",
  "product_name": "Mouse",
  "category": "Accessories",
  "region": "North",
  "quantity": 3,
  "sales": 450.00,
  "profit": 85.50
}
```
