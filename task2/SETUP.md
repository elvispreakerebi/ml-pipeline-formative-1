# Task 2: Local MySQL and MongoDB Setup

## Starting the Databases

### MySQL

**Option A: Docker** (recommended – no password to remember):

```bash
# Use port 3307 to avoid conflict with existing MySQL on 3306
docker run -d --name mysql-ecommerce -p 3307:3306 \
  -e MYSQL_ROOT_PASSWORD=task2local \
  -e MYSQL_DATABASE=ecommerce_sales \
  mysql:8
```

Then create `.env` with:
```
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_PASSWORD=task2local
```
(Use 127.0.0.1 instead of localhost for Docker MySQL.)

**Option B: Homebrew MySQL** (if you know your root password):

```bash
brew services start mysql
# Create .env with MYSQL_PASSWORD=your_password
```

**Note:** If you forgot your Homebrew MySQL password, use Option A (Docker) instead.

### MongoDB

**Option A: Docker** (recommended if Homebrew install fails):

```bash
docker run -d --name mongodb -p 27017:27017 mongo:latest
```

**Option B: Homebrew**

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Check MongoDB is running:** `mongosh --eval "db.version()"` or connect to `mongodb://localhost:27017`

---

## Running the Full Pipeline

Once both databases are running:

```bash
# 1. Create .env with your MySQL password (see above)

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Create MySQL schema and load data
mysql -u root -p < task2/database/sql/schema.sql
python task2/database/scripts/load_mysql.py

# 4. Load MongoDB data
python task2/database/scripts/load_mongodb.py

# 5. Run MySQL queries
mysql -u root -p ecommerce_sales < task2/database/sql/queries.sql

# 6. Run MongoDB queries
python task2/database/mongodb/queries.py
```

Or use the convenience script (after creating `.env`):

```bash
./task2/run_all.sh
```
