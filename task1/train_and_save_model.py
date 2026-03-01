"""
Train and save the sales forecasting model (Task 1 pipeline).
Run this once to produce models/sales_model.pkl for Task 4.
"""
import sys
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "ecommerce_sales_data.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "sales_model.pkl"
FEATURES = ["Lag_1", "Lag_7", "MA_7", "MA_30"]


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Task 1 preprocessing: daily resample, fill missing, add lag/MA features."""
    df = df.copy()
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    daily = df.resample("D", on="Order Date").agg(
        {"Sales": "sum", "Quantity": "sum", "Profit": "sum"}
    )
    daily = daily.asfreq("D").fillna(0)
    daily["Lag_1"] = daily["Sales"].shift(1)
    daily["Lag_7"] = daily["Sales"].shift(7)
    daily["MA_7"] = daily["Sales"].rolling(window=7).mean()
    daily["MA_30"] = daily["Sales"].rolling(window=30).mean()
    return daily


def main():
    if not DATA_PATH.exists():
        print(f"Error: Data not found at {DATA_PATH}")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    daily = preprocess(df)
    model_df = daily.dropna(subset=FEATURES)

    X = model_df[FEATURES]
    y = model_df["Sales"]

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
    )
    model.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES}, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
