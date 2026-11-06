"""
Optional Streamlit dashboard.
Run after main.py: streamlit run app.py
"""

from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from tensorflow.keras.models import load_model

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "dataset"
MODEL_DIR = ROOT / "models"
GRAPH_DIR = ROOT / "graphs"

st.set_page_config(page_title="Reliance LSTM Forecast", page_icon="📈", layout="wide")
st.title("AI-Based Financial Time Series Forecasting")
st.caption("Reliance Industries | LSTM model")

required = [
    DATA_DIR / "reliance_cleaned.csv",
    MODEL_DIR / "lstm_model.keras",
    MODEL_DIR / "scaler.pkl"
]
if not all(p.exists() for p in required):
    st.error("Required files are missing. Run `python main.py` first.")
    st.stop()

data = pd.read_csv(DATA_DIR / "reliance_cleaned.csv", parse_dates=["Date"])
model = load_model(MODEL_DIR / "lstm_model.keras")
scaler = joblib.load(MODEL_DIR / "scaler.pkl")

latest_close = float(data["Close"].iloc[-1])
last_60 = data["Close"].tail(60).to_numpy().reshape(-1, 1)
x = scaler.transform(last_60).reshape(1, 60, 1)
pred_scaled = model.predict(x, verbose=0)
predicted_close = float(scaler.inverse_transform(pred_scaled)[0, 0])

c1, c2, c3 = st.columns(3)
c1.metric("Latest historical close", f"₹{latest_close:,.2f}")
c2.metric("Next-session model estimate", f"₹{predicted_close:,.2f}")
c3.metric("Estimated difference", f"₹{predicted_close-latest_close:,.2f}")

st.subheader("Historical closing prices")
chart_data = data.set_index("Date")[["Close"]]
st.line_chart(chart_data)

prediction_file = GRAPH_DIR / "actual_vs_predicted.png"
if prediction_file.exists():
    st.subheader("Test-set: actual vs predicted")
    st.image(str(prediction_file), use_container_width=True)

metrics_file = MODEL_DIR / "metrics.json"
if metrics_file.exists():
    with open(metrics_file, encoding="utf-8") as f:
        metrics = json.load(f)
    st.subheader("Test-set evaluation")
    m1, m2 = st.columns(2)
    m1.metric("RMSE (₹)", f"{metrics['RMSE']:.4f}")
    m2.metric("MAE (₹)", f"{metrics['MAE']:.4f}")

st.warning(
    "This is an educational forecasting model. Stock prices are uncertain; "
    "the output is not a trading signal or financial advice."
)
