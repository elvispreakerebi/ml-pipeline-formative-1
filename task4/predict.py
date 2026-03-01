#!/usr/bin/env python3
"""
Task 4: Prediction/Forecast Script
A. Fetch time series records from API
B. Preprocess (Task 1 pipeline)
C. Load trained model
D. Make prediction/forecast
"""
import argparse
import sys
from pathlib import Path

import pandas as pd
import requests
import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "sales_model.pkl"
DEFAULT_API_URL = "http://localhost:8000"


def fetch_records(api_url: str, start_date: str, end_date: str) -> list[dict]:
    """Fetch records by date range from Task 3 API (MySQL)."""
    url = f"{api_url.rstrip('/')}/mysql/orders/query/date-range"
    resp = requests.get(url, params={"start": start_date, "end": end_date, "limit": 500})
    resp.raise_for_status()
    return resp.json()


def records_to_daily_df(
    records: list[dict], start_date: str, end_date: str
) -> pd.DataFrame:
    """Convert API records to daily aggregated DataFrame (Sales sum per day)."""
    if not records:
        raise ValueError("No records to aggregate")
    df = pd.DataFrame(records)
    df["order_date"] = pd.to_datetime(df["order_date"])
    daily = (
        df.groupby(df["order_date"].dt.date)
        .agg({"sales": "sum", "quantity": "sum", "profit": "sum"})
        .rename(columns={"sales": "Sales", "quantity": "Quantity", "profit": "Profit"})
    )
    daily.index = pd.DatetimeIndex(daily.index)
    # Reindex to full date range (Task 1: asfreq D, fill missing with 0)
    full_range = pd.date_range(start=start_date, end=end_date, freq="D")
    daily = daily.reindex(full_range).fillna(0)
    return daily


def preprocess(daily: pd.DataFrame) -> pd.DataFrame:
    """Task 1 preprocessing: add Lag_1, Lag_7, MA_7, MA_30."""
    daily = daily.copy()
    daily["Lag_1"] = daily["Sales"].shift(1)
    daily["Lag_7"] = daily["Sales"].shift(7)
    daily["MA_7"] = daily["Sales"].rolling(window=7).mean()
    daily["MA_30"] = daily["Sales"].rolling(window=30).mean()
    return daily


def load_model():
    """Load trained model from disk."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run: python task1/train_and_save_model.py"
        )
    data = joblib.load(MODEL_PATH)
    return data["model"], data["features"]


def predict(
    api_url: str = DEFAULT_API_URL,
    days_back: int = 35,
    end_date: str | None = None,
) -> float:
    """
    Full pipeline: fetch -> preprocess -> load model -> predict.
    Uses last `days_back` days to build features for next-day forecast.
    """
    # A. Fetch from API (need ~35 days for MA_30 + buffer)
    if end_date:
        end = pd.to_datetime(end_date).date()
    else:
        end = pd.Timestamp.now().date()
    start = end - pd.Timedelta(days=days_back)
    records = fetch_records(api_url, str(start), str(end))

    # B. Preprocess
    daily = records_to_daily_df(records, str(start), str(end))
    daily = preprocess(daily)
    last_row = daily.dropna(subset=["Lag_1", "Lag_7", "MA_7", "MA_30"]).iloc[-1:]

    if last_row.empty:
        raise ValueError(
            "Insufficient data for features (need 30+ days with sales). Try a wider date range."
        )

    # C. Load model
    model, features = load_model()
    X = last_row[features]

    # D. Predict
    pred = model.predict(X)[0]
    return float(pred)


def main():
    parser = argparse.ArgumentParser(description="Task 4: Sales forecast from API")
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"Task 3 API base URL (default: {DEFAULT_API_URL})",
    )
    parser.add_argument(
        "--days-back",
        type=int,
        default=35,
        help="Days of history to fetch for features (default: 35)",
    )
    parser.add_argument(
        "--end-date",
        default=None,
        help="End date for fetch (YYYY-MM-DD). Default: today. Use 2024-12-31 for dataset.",
    )
    args = parser.parse_args()

    try:
        forecast = predict(
            api_url=args.api_url,
            days_back=args.days_back,
            end_date=args.end_date,
        )
        print(f"Predicted next-day sales: ${forecast:,.2f}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
