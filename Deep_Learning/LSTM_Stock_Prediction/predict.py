"""
Predict the next observation (next trading session) using the trained LSTM.
Run this after main.py: python predict.py
"""

from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "dataset"
MODEL_DIR = ROOT / "models"
SEQUENCE_LENGTH = 60


def main():
    model_path = MODEL_DIR / "lstm_model.keras"
    scaler_path = MODEL_DIR / "scaler.pkl"
    cleaned_path = DATA_DIR / "reliance_cleaned.csv"

    if not model_path.exists() or not scaler_path.exists():
        raise FileNotFoundError("Model files not found. Run 'python main.py' first.")
    if not cleaned_path.exists():
        raise FileNotFoundError("Cleaned dataset not found. Run 'python main.py' first.")

    data = pd.read_csv(cleaned_path, parse_dates=["Date"])
    data = data.sort_values("Date").dropna(subset=["Close"])

    if len(data) < SEQUENCE_LENGTH:
        raise ValueError(f"At least {SEQUENCE_LENGTH} observations are required.")

    model = load_model(model_path)
    scaler = joblib.load(scaler_path)

    recent_prices = data["Close"].tail(SEQUENCE_LENGTH).to_numpy().reshape(-1, 1)
    scaled_input = scaler.transform(recent_prices)
    X_input = scaled_input.reshape(1, SEQUENCE_LENGTH, 1)

    prediction_scaled = model.predict(X_input, verbose=0)
    predicted_price = float(scaler.inverse_transform(prediction_scaled)[0, 0])

    latest_date = data["Date"].iloc[-1].date()
    latest_close = float(data["Close"].iloc[-1])

    print("\n========== NEXT SESSION FORECAST ==========")
    print(f"Latest data date       : {latest_date}")
    print(f"Latest closing price   : INR {latest_close:.2f}")
    print(f"Predicted next close   : INR {predicted_price:.2f}")
    print(f"Predicted change       : INR {predicted_price - latest_close:.2f}")
    print("===========================================\n")
    print("This is an experimental model estimate, not financial advice.")


if __name__ == "__main__":
    main()
