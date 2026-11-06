# Real-Time Emotion Detection Using CNN and OpenCV

A Python deep-learning project that detects faces from a live webcam
feed and classifies the visible facial expression using a Convolutional
Neural Network (CNN).

> **Note:** This project classifies visible facial expressions. It does
> not determine a person's true internal emotional state.

## Features

-   Face detection from a live webcam using OpenCV Haar Cascade.
-   Facial-image preprocessing: grayscale conversion, resizing to
    `48 × 48`, and pixel normalization.
-   CNN-based multi-class expression classification.
-   Softmax class probabilities and confidence display.
-   Bounding boxes and predicted labels on webcam frames.
-   Training and evaluation plots for accuracy and loss.

## Emotion classes

The FER-2013 dataset contains seven classes:

`angry`, `disgust`, `fear`, `happy`, `neutral`, `sad`, `surprise`

The model predicts the classes it was trained on. If you want only five
classes, remove `disgust` and `fear` from both training and test data,
then retrain the model.

## Project structure

``` text
Real_Time_Emotion_Detection/
├── archive/
│   ├── train/
│   │   ├── angry/
│   │   ├── disgust/
│   │   ├── fear/
│   │   ├── happy/
│   │   ├── neutral/
│   │   ├── sad/
│   │   └── surprise/
│   └── test/
│       ├── angry/
│       ├── disgust/
│       ├── fear/
│       ├── happy/
│       ├── neutral/
│       ├── sad/
│       └── surprise/
├── models/
│   ├── emotion_model.keras
│   ├── labels.json
│   ├── accuracy.png
│   └── loss.png
├── train_model.py
├── real_time_detection.py
├── requirements.txt
└── README.md
```

The `models/` directory and its output files are created when the
training script runs. Keep the dataset directory names consistent with
the paths configured in `train_model.py`.

## Dataset

This project is designed for a folder-based FER-2013 dataset.

-   Dataset: [FER-2013 on
    Kaggle](https://www.kaggle.com/datasets/msambare/fer2013)
-   Arrange the extracted images into `archive/train/<emotion>/` and
    `archive/test/<emotion>/`.
-   Each emotion folder must contain its corresponding images.
-   Use the same class folders in both training and test directories.

Check the dataset's license and terms before redistributing it.

## Requirements

-   Windows 10/11 (instructions below are for Windows).
-   Python 3.13 (64-bit) recommended for the package versions in
    `requirements.txt`.
-   A working webcam.
-   Internet connection for installing packages and downloading the
    dataset.

Python 3.14 may not have compatible wheels for every dependency in every
release. Use the Python version specified above for this environment.

## Setup on Windows

Open Command Prompt in the project directory.

### 1. Confirm Python 3.13 is installed

``` bat
py -3.13 --version
```

### 2. Create and activate a virtual environment

``` bat
py -3.13 -m venv emotion_env
emotion_env\Scripts\activate
```

After activation, the prompt should begin with `(emotion_env)`.

### 3. Upgrade pip and install dependencies

``` bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Verify OpenCV

``` bat
python -c "import cv2; print(cv2.__version__); print('CascadeClassifier:', hasattr(cv2, 'CascadeClassifier'))"
```

The final output should be:

``` text
CascadeClassifier: True
```

If it prints `False`, check that only one OpenCV package is installed:

``` bat
python -m pip list | findstr opencv
```

Keep `opencv-python` only; do not install `opencv-python-headless` or
multiple OpenCV variants in the same environment.

## Train the CNN

From the project directory, with the virtual environment activated:

``` bat
python train_model.py
```

The training script should:

1.  Load images from `archive/train` and `archive/test`.
2.  Create a training/validation split from the training folder.
3.  Train the CNN.
4.  Evaluate it on the test folder.
5.  Save the trained model and class labels under `models/`.
6.  Save accuracy and loss plots.

The training script must create the `models` folder before saving files.
For example:

``` python
import os
os.makedirs("models", exist_ok=True)
```

The paths in the training script should match this repository structure:

``` python
train_dir = "archive/train"
test_dir = "archive/test"
```

## Run real-time webcam detection

After training has successfully created `models/emotion_model.keras` and
`models/labels.json`, run:

``` bat
python real_time_detection.py
```

-   Allow camera access if Windows asks.
-   The webcam window should show detected faces, predicted expression
    labels, and confidence values.
-   Press **Q** to close the webcam window.

If the webcam does not open, try changing:

``` python
cap = cv2.VideoCapture(0)
```

to:

``` python
cap = cv2.VideoCapture(1)
```

Also close other applications that may be using the camera.

## Model overview

The example CNN architecture uses:

-   `Conv2D` layers to learn visual features.
-   `BatchNormalization` to stabilize training.
-   `MaxPooling2D` to reduce feature-map dimensions.
-   `Flatten` to convert feature maps into a vector.
-   `Dense` layers for classification.
-   `Dropout` to help reduce overfitting.
-   `Softmax` to produce class probabilities.

The webcam preprocessing must match the training preprocessing:
grayscale, `48 × 48`, and pixel values scaled to `[0, 1]`.

## Evaluation and limitations

-   Report test accuracy from the actual output of `model.evaluate`; do
    not assume a target accuracy.
-   A large gap between training and validation accuracy can indicate
    overfitting.
-   Results may vary with lighting, camera quality, pose, occlusion, and
    differences between webcam images and the training dataset.
-   The confidence score is the model's predicted class probability, not
    a guarantee that the prediction is correct.
-   Facial-expression classification should not be used as a definitive
    assessment of a person's feelings or for consequential decisions.

## Troubleshooting

  ------------------------------------------------------------------------
  Problem                              What to check
  ------------------------------------ -----------------------------------
  `FileNotFoundError: archive/train`   Confirm the dataset folder exists
                                       at the project root and contains
                                       emotion subfolders.

  `No module named cv2`                Activate `emotion_env`, then
                                       install `requirements.txt` in that
                                       environment.

  `cv2` has no `CascadeClassifier`     Check for conflicting OpenCV
                                       packages; keep only
                                       `opencv-python`.

  Model file not found                 Run `train_model.py` successfully
                                       before starting webcam detection.

  Webcam cannot open                   Check Windows camera permissions,
                                       close other camera apps, or try
                                       camera index `1`.

  Poor validation/test accuracy        Check labels and preprocessing;
                                       consider augmentation, class
                                       balancing, and early stopping.
  ------------------------------------------------------------------------

## Suggested GitHub description

A real-time facial-expression classification project using a CNN trained
on FER-2013 and OpenCV for webcam face detection and live prediction.
