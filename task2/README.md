# Task 2: Design Databases (SQL and MongoDB)

Database design and implementation for the ecommerce sales time-series dataset.

## Prerequisites

- Local MySQL 8.x
- Local MongoDB
- Python 3.8+ with `pip install -r requirements.txt`

## Setup

1. **MySQL**: Create schema and load data
   ```bash
   mysql -u root < task2/database/sql/schema.sql
   python task2/database/scripts/load_mysql.py
   ```

2. **MongoDB**: Load data
   ```bash
   python task2/database/scripts/load_mongodb.py
   ```

## Structure

- `database/erd/` - ERD diagram (Mermaid)
- `database/sql/` - MySQL schema and queries
- `database/mongodb/` - Collection design, sample docs, queries
- `database/scripts/` - Data loading scripts
- `query_results/` - Query definitions and expected results

## Running Queries

- **MySQL**: `mysql -u root ecommerce_sales < task2/database/sql/queries.sql`
- **MongoDB**: `python task2/database/mongodb/queries.py`
