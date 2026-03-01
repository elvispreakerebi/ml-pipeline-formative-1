# Task 4: Prediction/Forecast Script

End-to-end script that:
- **A.** Fetches time series records from the Task 3 API
- **B.** Preprocesses data (Task 1 pipeline: daily aggregate, Lag_1, Lag_7, MA_7, MA_30)
- **C.** Loads the trained Random Forest model
- **D.** Makes a prediction/forecast for next-day sales

## Prerequisites

1. **Task 3 API running** (MySQL + MongoDB + uvicorn)
2. **Trained model** – run once to create it:

```bash
python task1/train_and_save_model.py
```

This saves `models/sales_model.pkl` using the Task 1 preprocessing and tuned Random Forest.

## Run the prediction

```bash
# Default: fetch from http://localhost:8000, use last 35 days
python task4/predict.py

# Custom API URL (e.g. deployed API)
python task4/predict.py --api-url https://your-api.onrender.com

# More history for feature computation
python task4/predict.py --days-back 60

# Use dataset end date (2024-12-31) when testing with historical data
python task4/predict.py --end-date 2024-12-31
```

## Output

```
Predicted next-day sales: $9,234.56
```
