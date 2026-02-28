# Task 2: Design Databases (SQL and MongoDB)

Database design and implementation for the ecommerce sales time-series dataset.

## Prerequisites

- Local MySQL 8.x
- Local MongoDB (or Docker)
- Python 3.8+ with `pip install -r requirements.txt`

## Quick Start

**1. Start the databases** – see [SETUP.md](SETUP.md) for MySQL and MongoDB startup commands.

**2. Create `.env`** – copy from `.env.example` and set your `MYSQL_PASSWORD`:
   ```bash
   cp .env.example .env
   # Edit .env and add your MySQL root password
   ```

**3. Run everything:**
   ```bash
   ./task2/run_all.sh
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
