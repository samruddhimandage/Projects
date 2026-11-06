# LSTM Stock Prediction - Starter Project

## Your dataset
Copy the Reliance Kaggle CSV or Excel file into `dataset/`.
The script detects the first `.csv`, `.xlsx`, or `.xls` file and attempts
to identify `Date` and `Close` columns automatically.

## Setup (Windows)
Open a terminal in this project folder:

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run training and evaluation
```bash
python main.py
```

## Run next-session prediction
```bash
python predict.py
```

## Optional dashboard
```bash
streamlit run app.py
```

## Outputs
- `dataset/reliance_cleaned.csv`
- `models/lstm_model.keras`
- `models/scaler.pkl`
- `models/metrics.json`
- `graphs/stock_price.png`
- `graphs/actual_vs_predicted.png`
- `graphs/training_loss.png`
- `graphs/test_predictions.csv`

The model predicts the next observation in the supplied dataset's trading-day
sequence. It is an educational estimate, not financial advice. Historical
accuracy does not guarantee future performance.
