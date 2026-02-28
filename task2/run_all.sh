#!/bin/bash
# Run Task 2 database setup and queries.
# Prerequisites: MySQL and MongoDB running, .env with MYSQL_PASSWORD

set -e
cd "$(dirname "$0")/.."

echo "=== Task 2: Database Setup and Queries ==="

# Check .env exists and source it
if [ ! -f .env ]; then
    echo "Error: Create .env from .env.example and set MYSQL_PASSWORD"
    exit 1
fi
set -a
source .env
set +a

# Install deps if needed
pip install -q pandas pymysql pymongo python-dotenv 2>/dev/null || true

MYSQL_AUTH="-h ${MYSQL_HOST:-localhost} -P ${MYSQL_PORT:-3306} -u ${MYSQL_USER:-root} -p${MYSQL_PASSWORD}"

echo ""
echo "1. Creating MySQL schema..."
mysql $MYSQL_AUTH < task2/database/sql/schema.sql

echo "2. Loading MySQL data..."
python task2/database/scripts/load_mysql.py

echo ""
echo "3. Loading MongoDB data..."
python task2/database/scripts/load_mongodb.py

echo ""
echo "4. Running MySQL queries..."
mysql $MYSQL_AUTH ${MYSQL_DATABASE:-ecommerce_sales} < task2/database/sql/queries.sql

echo ""
echo "5. Running MongoDB queries..."
python task2/database/mongodb/queries.py

echo ""
echo "=== Done ==="
