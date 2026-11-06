"""
AI-Based Financial Time Series Forecasting Using LSTM
Dataset: Reliance Industries historical stock data downloaded from Kaggle.

Put the downloaded CSV/XLSX file inside the dataset/ folder.
The script automatically finds it and detects the Date and Close columns.
Run: python main.py
"""

from pathlib import Path
import json
import re
import warnings

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

warnings.filterwarnings("ignore")
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "dataset"
MODEL_DIR = ROOT / "models"
GRAPH_DIR = ROOT / "graphs"

SEQUENCE_LENGTH = 60
TRAIN_RATIO = 0.80
EPOCHS = 50
BATCH_SIZE = 32


def normalize_name(name):
    """Make column names comparable despite spaces, punctuation or case."""
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def load_dataset():
    """Load the first supported CSV/Excel file from dataset/."""
    supported = {".csv", ".xlsx", ".xls"}
    files = sorted(
        p for p in DATA_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in supported
    )
    if not files:
        raise FileNotFoundError(
            f"No CSV/Excel dataset found in: {DATA_DIR}\n"
            "Copy your Reliance Kaggle .csv or .xlsx file into the dataset folder."
        )

    file_path = files[0]
    print(f"\nLoading dataset: {file_path.name}")

    if file_path.suffix.lower() == ".csv":
        try:
            df = pd.read_csv(file_path)
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding="latin1")
    else:
        df = pd.read_excel(file_path)

    # Flatten multi-level column headers, if present.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join(str(part) for part in col if str(part) != "nan").strip("_")
            for col in df.columns
        ]

    # Find date and closing-price columns.
    normalized = {normalize_name(col): col for col in df.columns}

    date_col = None
    for candidate in ("date", "datetime", "timestamp", "tradingdate"):
        if candidate in normalized:
            date_col = normalized[candidate]
            break

    close_col = None
    # Prefer Close, not Adj Close or Last.
    for candidate in ("close", "closingprice", "closeprice", "closing"):
        if candidate in normalized:
            close_col = normalized[candidate]
            break

    if close_col is None:
        # Fallbacks for differently named Kaggle datasets.
        for candidate in ("adjclose", "last", "ltp"):
            if candidate in normalized:
                close_col = normalized[candidate]
                break

    # Some CSVs save Date as the first unnamed/index column.
    if date_col is None:
        first_col = df.columns[0]
        if str(first_col).lower().startswith("unnamed"):
            date_col = first_col
        else:
            parsed = pd.to_datetime(df[first_col], errors="coerce")
            if parsed.notna().mean() > 0.8:
                date_col = first_col

    if close_col is None:
        raise ValueError(
            "Could not identify the closing-price column.\n"
            f"Columns found: {list(df.columns)}\n"
            "Expected a column named Close, Closing Price, Adj Close, Last or LTP."
        )

    if date_col is None:
        raise ValueError(
            "Could not identify the date column. "
            f"Columns found: {list(df.columns)}"
        )

    data = pd.DataFrame({
        "Date": pd.to_datetime(df[date_col], errors="coerce", dayfirst=True),
        "Close": pd.to_numeric(
            df[close_col].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        )
    })

    data = data.dropna(subset=["Date", "Close"])
    data = data[data["Close"] > 0]
    data = data.sort_values("Date")
    data = data.drop_duplicates(subset=["Date"], keep="last")
    data = data.reset_index(drop=True)

    if len(data) <= SEQUENCE_LENGTH + 10:
        raise ValueError(
            f"Only {len(data)} valid rows found. At least "
            f"{SEQUENCE_LENGTH + 11} rows are required."
        )

    print(f"Detected date column : {date_col}")
    print(f"Detected price column: {close_col}")
    print(f"Rows after cleaning  : {len(data)}")
    print(f"Date range           : {data['Date'].min().date()} to {data['Date'].max().date()}")
    return data


def main():
    DATA_DIR.mkdir(exist_ok=True)
    MODEL_DIR.mkdir(exist_ok=True)
    GRAPH_DIR.mkdir(exist_ok=True)

    data = load_dataset()
    data.to_csv(DATA_DIR / "reliance_cleaned.csv", index=False)

    # Historical price graph.
    plt.figure(figsize=(13, 6))
    plt.plot(data["Date"], data["Close"], linewidth=1)
    plt.title("Reliance Industries Historical Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (INR)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "stock_price.png", dpi=150)
    plt.close()

    prices = data["Close"].to_numpy(dtype=np.float32).reshape(-1, 1)
    split_index = int(len(prices) * TRAIN_RATIO)

    # Fit scaler on training data only to avoid test-data leakage.
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(prices[:split_index])
    scaled_prices = scaler.transform(prices)

    X_train, y_train = [], []
    X_test, y_test = [], []

    # Test sequences use the 60 immediately preceding observations as context.
    for i in range(SEQUENCE_LENGTH, len(scaled_prices)):
        x_sequence = scaled_prices[i - SEQUENCE_LENGTH:i]
        target = scaled_prices[i, 0]

        if i < split_index:
            X_train.append(x_sequence)
            y_train.append(target)
        else:
            X_test.append(x_sequence)
            y_test.append(target)

    X_train = np.asarray(X_train, dtype=np.float32)
    y_train = np.asarray(y_train, dtype=np.float32)
    X_test = np.asarray(X_test, dtype=np.float32)
    y_test = np.asarray(y_test, dtype=np.float32)

    if len(X_train) == 0 or len(X_test) == 0:
        raise ValueError("Not enough data to create training and testing sequences.")

    print("\nTraining data shape:", X_train.shape)
    print("Testing data shape :", X_test.shape)

    model = Sequential([
        Input(shape=(SEQUENCE_LENGTH, 1)),
        LSTM(50, return_sequences=True),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25, activation="relu"),
        Dense(1)
    ])

    model.compile(optimizer="adam", loss="mean_squared_error")
    model.summary()

    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=8,
        restore_best_weights=True
    )

    history = model.fit(
        X_train,
        y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=0.1,
        callbacks=[early_stopping],
        shuffle=False,
        verbose=1
    )

    model.save(MODEL_DIR / "lstm_model.keras")
    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")

    # Evaluate in original INR units.
    predictions_scaled = model.predict(X_test, verbose=0)
    predicted_prices = scaler.inverse_transform(predictions_scaled).ravel()
    actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1)).ravel()

    rmse = float(np.sqrt(mean_squared_error(actual_prices, predicted_prices)))
    mae = float(mean_absolute_error(actual_prices, predicted_prices))

    test_dates = data["Date"].iloc[split_index:].reset_index(drop=True)
    results = pd.DataFrame({
        "Date": test_dates,
        "Actual_Close": actual_prices,
        "Predicted_Close": predicted_prices
    })
    results.to_csv(GRAPH_DIR / "test_predictions.csv", index=False)

    # Actual vs predicted graph.
    plt.figure(figsize=(14, 7))
    plt.plot(test_dates, actual_prices, label="Actual Price")
    plt.plot(test_dates, predicted_prices, label="Predicted Price")
    plt.title("Reliance Stock: Actual vs Predicted Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (INR)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "actual_vs_predicted.png", dpi=150)
    plt.close()

    # Training and validation loss graph.
    plt.figure(figsize=(10, 5))
    plt.plot(history.history["loss"], label="Training Loss")
    plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.title("LSTM Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Mean Squared Error")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "training_loss.png", dpi=150)
    plt.close()

    metrics = {
        "RMSE": rmse,
        "MAE": mae,
        "training_rows": int(len(X_train)),
        "testing_rows": int(len(X_test)),
        "sequence_length": SEQUENCE_LENGTH,
        "dataset_start": str(data["Date"].min().date()),
        "dataset_end": str(data["Date"].max().date())
    }
    with open(MODEL_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)

    print("\n========== MODEL EVALUATION ==========")
    print(f"RMSE: {rmse:.4f} INR")
    print(f"MAE : {mae:.4f} INR")
    print("======================================")
    print("\nSaved files:")
    print("- models/lstm_model.keras")
    print("- models/scaler.pkl")
    print("- models/metrics.json")
    print("- graphs/stock_price.png")
    print("- graphs/actual_vs_predicted.png")
    print("- graphs/training_loss.png")
    print("- graphs/test_predictions.csv")
    print("\nTraining and evaluation completed successfully.")


if __name__ == "__main__":
    main()
