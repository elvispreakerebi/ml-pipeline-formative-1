# ML Pipeline Formative 1 – Time Series Data Pipeline

[![Colab Notebook](https://img.shields.io/badge/GitHub-elvispreakerebi%2Fml--pipeline--formative--1-blue)](https://colab.research.google.com/drive/1wm0G0mBj3AbPZ4ERzcSDDcJ-woeVrZaN?usp=sharing)

End-to-end time-series pipeline for **ecommerce sales forecasting** using MySQL, MongoDB, FastAPI, and a Random Forest model.

---

## Team

| Member | Task | Components |
|--------|------|------------|
| Nformi Modestine Girbong | Task 1 | EDA, preprocessing, model training |
| Elvis Preye Kerebi | Task 2 | MySQL/MongoDB design, load scripts, queries |
| Kakooza Mahad | Task 3 | FastAPI CRUD and time-series endpoints |
| David Nwanze Akachi | Task 4 | Prediction script, model integration |

---

## Overview

This project implements a four-task pipeline:

| Task | Description |
|------|-------------|
| **Task 1** | Time-series preprocessing, exploratory analysis, and model training |
| **Task 2** | Relational (MySQL) and document (MongoDB) database design |
| **Task 3** | CRUD and time-series query API |
| **Task 4** | Prediction script: fetch from API → preprocess → load model → forecast |

**Dataset:** Ecommerce sales (3,500 orders, 2022–2024)  
**Target:** Daily sales forecasting  
**Model:** Random Forest (Lag_1, Lag_7, MA_7, MA_30 features)

---

## Repository Structure

```
ml-pipeline-formative-1/
├── data/                    # Dataset
│   └── ecommerce_sales_data.csv
├── task1/                   # EDA, preprocessing, modeling
│   ├── ML_Pipeline_Formative1_Group10_Task1.ipynb
│   └── train_and_save_model.py
├── task2/                   # Database design (SQL + MongoDB)
│   ├── database/erd/        # ERD diagram
│   ├── database/sql/        # Schema, queries, load scripts
│   ├── database/mongodb/     # Collection design, sample docs, queries
│   ├── query_results/       # Query outputs
│   └── SETUP.md
├── task3/                   # CRUD and time-series API
│   ├── main.py
│   ├── db_mysql.py
│   ├── db_mongodb.py
│   └── models.py
├── task4/                   # Prediction script
│   ├── predict.py
│   └── README.md
├── models/                  # Trained model (generated)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Prerequisites

- **Python 3.8+**
- **Docker** (for MySQL and MongoDB)
- **Git**

---

## Quick Start – Reproducing Results

### 1. Clone and install

```bash
git clone https://github.com/elvispreakerebi/ml-pipeline-formative-1
cd ml-pipeline-formative-1
pip install -r requirements.txt
```

### 2. Start databases (Docker)

```bash
docker run -d --name mysql-ecommerce -p 3307:3306 \
  -e MYSQL_ROOT_PASSWORD=task2local \
  -e MYSQL_DATABASE=ecommerce_sales \
  mysql:8

docker run -d --name mongodb -p 27017:27017 mongo:latest
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set:

```
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_PASSWORD=task2local
```

### 4. Load data (Task 2)

```bash
mysql -h 127.0.0.1 -P 3307 -u root -ptask2local < task2/database/sql/schema.sql
python task2/database/scripts/load_mysql.py
python task2/database/scripts/load_mongodb.py
```

### 5. Start API (Task 3)

```bash
python -m uvicorn task3.main:app --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  

### 6. Train model and run prediction (Task 4)

```bash
# Train model (run once)
python task1/train_and_save_model.py

# Run prediction (with API running in another terminal)
python task4/predict.py --end-date 2024-12-31
```

**Expected output:** `Predicted next-day sales: $9,542.42`

---

## Task Details

### Task 1 – EDA and Modeling

- Notebook: `task1/ML_Pipeline_Formative1_Group10_Task1.ipynb`
- Preprocessing: daily resample, Lag_1, Lag_7, MA_7, MA_30
- Model: Random Forest (tuned)
- Model export: `python task1/train_and_save_model.py` → `models/sales_model.pkl`

### Task 2 – Databases

- **MySQL:** 4 tables (categories, products, regions, orders)
- **MongoDB:** `orders` collection with embedded product
- Setup: [task2/SETUP.md](task2/SETUP.md)
- Queries: 3+ per database (latest, date range, aggregations)

### Task 3 – API

- **CRUD:** POST, GET, PUT, DELETE for MySQL and MongoDB
- **Time-series:** `/query/latest`, `/query/date-range`
- Docs: http://localhost:8000/docs

### Task 4 – Prediction

- Fetches from Task 3 API
- Reuses Task 1 preprocessing
- Loads trained model and outputs next-day sales forecast

---

## Dependencies

See [requirements.txt](requirements.txt):

- pandas, numpy, scikit-learn, joblib
- pymysql, pymongo
- fastapi, uvicorn
- requests, python-dotenv

---

## License

This project is for educational purposes (ALU Formative 1).
