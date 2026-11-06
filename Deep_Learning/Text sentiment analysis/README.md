# Movie Review Sentiment Analysis using LSTM

## Overview
This project uses a Long Short-Term Memory (LSTM) neural network built with
TensorFlow/Keras to classify IMDb movie reviews as positive or negative.

The supplied `3_LSTM_model.py` script:
- Loads the IMDb dataset through `tensorflow.keras.datasets`.
- Uses the 10,000 most frequent words.
- Decodes and displays sample reviews.
- Pads/truncates reviews to 200 tokens.
- Uses a 32-dimensional Embedding layer.
- Uses an LSTM layer with 64 units.
- Uses a sigmoid output for binary sentiment prediction.
- Trains for 3 epochs with batch size 64 and a 20% validation split.
- Evaluates the model on the IMDb test dataset.
- Prints an example test review's actual and predicted sentiment.

## Technology stack
- Python
- TensorFlow / Keras

## Project structure
```text
IMDb_LSTM_Sentiment_Analysis/
├── 3_LSTM_model.py
├── requirements.txt
└── README.md
```

## Dataset
The script uses the IMDb dataset bundled with TensorFlow/Keras. You do not need
to download a separate Kaggle dataset or CSV file. An internet connection may
be required on the first run so Keras can download the dataset.

Labels:
- `0` = Negative
- `1` = Positive

## Model architecture
```text
IMDb encoded review
       |
       v
Padding / truncation (200 tokens)
       |
       v
Embedding (vocabulary=10,000, dimensions=32)
       |
       v
LSTM (64 units)
       |
       v
Dense (1 unit, sigmoid)
       |
       v
Positive / Negative
```

## Configuration in the supplied script

| Parameter | Value |
|---|---:|
| Vocabulary size | 10,000 |
| Maximum review length | 200 |
| Embedding dimensions | 32 |
| LSTM units | 64 |
| Output units | 1 |
| Output activation | Sigmoid |
| Optimizer | Adam |
| Loss | Binary cross-entropy |
| Metric | Accuracy |
| Epochs | 3 |
| Batch size | 64 |
| Validation split | 20% |

## Installation (Windows / VS Code)
Use a Python version supported by your TensorFlow release. Python 3.10 or 3.11
is a practical starting point for many TensorFlow environments.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run
```powershell
python 3_LSTM_model.py
```

The script prints dataset sizes, decoded sample reviews, training progress,
test evaluation results, and one example's actual and predicted sentiment.

## Current implementation scope and limitations
- This is a **binary** classifier. It does not currently predict neutral sentiment.
- The script evaluates the model but does not save the trained model.
- The example prediction is taken from the IMDb test set; custom user-entered
  review prediction is not implemented.
- The Embedding layer is trained with the model; pretrained Word2Vec/GloVe
  vectors are not loaded.
- `Tokenizer` is imported but is not used in the current script.
- The script reports the result of `model.evaluate`; it does not calculate
  precision, recall, F1-score, or a confusion matrix.

## Possible improvements
- Save the trained model and add custom review prediction.
- Add precision, recall, F1-score and a confusion matrix.
- Compare LSTM with SimpleRNN and GRU.
- Add a three-class dataset if neutral sentiment classification is required.
