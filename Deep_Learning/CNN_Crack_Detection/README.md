# Concrete Surface Crack Detection Using CNN

A binary image-classification project that uses a Convolutional Neural
Network (CNN) built with TensorFlow/Keras to classify concrete surface
images as **Crack** or **No Crack**. The project also includes a
webcam-based prediction script using OpenCV.

## Project files --- what each one does

  ---------------------------------------------------------------------------
  File                                    Purpose
  --------------------------------------- -----------------------------------
  `CNN_Surface_Crack_Detection.py`        Main training pipeline: prepares
                                          the dataset, creates train/test
                                          folders, preprocesses images,
                                          builds and trains the CNN,
                                          evaluates it, plots metrics, saves
                                          the model, and includes a
                                          single-image prediction function.

  `Marvellous_Crack_Detection_Model.h5`   Saved, trained CNN model used for
                                          predictions without retraining.

  `realtime_cnn.py`                       Opens the webcam, preprocesses each
                                          frame, predicts Crack/No Crack with
                                          the saved model, and displays the
                                          label and confidence.

  `check_model.py`                        Loads the saved model and prints
                                          its input shape, output shape,
                                          layer count, and model summary.

  `test_opencv.py`                        Checks the OpenCV installation,
                                          loads a Haar Cascade face detector,
                                          and tests whether the webcam can be
                                          opened. It is a diagnostic script;
                                          the crack-detection webcam script
                                          does not use face detection.

  `requirements.txt`                      Lists the Python packages needed to
                                          run the project.

  `README.md`                             Documents the project, setup,
                                          execution, and troubleshooting
                                          steps.
  ---------------------------------------------------------------------------

## Features

-   Binary classification of concrete surface images: Crack / No Crack.
-   Dataset split into training and testing folders.
-   Image resizing to `128 × 128`.
-   Pixel normalization using `1/255`.
-   Training augmentation with rotation, zoom, and horizontal flipping.
-   CNN with three convolution and max-pooling blocks, a dense layer,
    dropout, and sigmoid output.
-   Model evaluation with accuracy, confusion matrix, and classification
    report.
-   Training and validation accuracy/loss plots.
-   Single-image prediction function in the training script.
-   Webcam prediction with a displayed class label and confidence
    percentage.

## Dataset

The training script expects the original dataset to be arranged as
follows:

``` text
Concrete Crack Dataset/
├── Positive/    # Images containing cracks
└── Negative/    # Images without cracks
```

The script creates this working structure:

``` text
CrackDataset/
├── train/
│   ├── Crack/
│   └── NoCrack/
└── test/
    ├── Crack/
    └── NoCrack/
```

The script uses an 80:20 split for each source class by default. It
copies image files with `.jpg`, `.jpeg`, or `.png` extensions.

Place the `Concrete Crack Dataset` folder in the same directory as
`CNN_Surface_Crack_Detection.py`, or update `original_dataset_path` in
that script.

## Project directory

A recommended layout is:

``` text
Crack_Detection_Project/
├── Concrete Crack Dataset/
│   ├── Positive/
│   └── Negative/
├── CrackDataset/                  # Created by training script
│   ├── train/
│   └── test/
├── CNN_Surface_Crack_Detection.py
├── Marvellous_Crack_Detection_Model.h5
├── realtime_cnn.py
├── check_model.py
├── test_opencv.py
├── requirements.txt
└── README.md
```

The training script saves `Marvellous_Crack_Detection_Model.h5` in the
current working directory. Keep the model file in the same directory
from which `check_model.py` and `realtime_cnn.py` are run, or change
`MODEL_PATH` in those scripts.

## Installation (Windows)

Use a Python version supported by the TensorFlow release you install.
Python 3.12 or 3.13 (64-bit) is a suitable starting point; confirm
compatibility for your chosen TensorFlow version.

Open Command Prompt in the project folder.

### 1. Create a virtual environment

For Python 3.13:

``` bat
py -3.13 -m venv crack_env
crack_env\Scripts\activate
```

If using Python 3.12, replace `-3.13` with `-3.12`.

### 2. Upgrade pip and install dependencies

``` bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Verify OpenCV

``` bat
python -c "import cv2; print(cv2.__version__); print('CascadeClassifier available:', hasattr(cv2, 'CascadeClassifier'))"
```

The final value should be `True`. Install only one OpenCV distribution
in this environment. For this project, use `opencv-python`; do not also
install `opencv-python-headless` or another OpenCV variant.

## Run the project

Run commands from the project root with the virtual environment
activated.

### 1. Train the CNN

``` bat
python CNN_Surface_Crack_Detection.py
```

This script creates the `CrackDataset` folders, splits and copies the
source images, trains for 10 epochs, evaluates the model, displays plots
and metrics, and saves:

``` text
Marvellous_Crack_Detection_Model.h5
```

**Dataset note:** The current script uses `test_data` as
`validation_data` during training and then evaluates on that same data.
For a rigorous final evaluation, use a separate validation split and
keep the test set untouched until final evaluation.

**Repeat-run note:** The split function copies files only when the
destination file does not already exist. If you change the source
dataset or split settings, remove the generated `CrackDataset` folder
before rerunning so the split is rebuilt.

### 2. Inspect the saved model

``` bat
python check_model.py
```

This prints the model input/output shapes, number of layers, and Keras
model summary.

### 3. Run webcam crack classification

``` bat
python realtime_cnn.py
```

The webcam opens and each full frame is resized and passed to the CNN.
The window displays `CRACK` or `NO CRACK` and the model's class
confidence. Press **Q** to exit.

The current webcam script classifies the entire camera frame. It does
not locate a crack region or draw a bounding box around a crack. For
meaningful predictions, point the camera at a concrete surface and keep
the surface filling most of the frame.

### 4. Test OpenCV and webcam separately

``` bat
python test_opencv.py
```

This checks the OpenCV Haar Cascade installation and whether the webcam
can be opened. Haar Cascade detects faces; it is not part of the
concrete crack classification pipeline.

## CNN architecture

The training script defines this sequence:

1.  `Conv2D(32)` + `MaxPooling2D`
2.  `Conv2D(64)` + `MaxPooling2D`
3.  `Conv2D(128)` + `MaxPooling2D`
4.  `Flatten`
5.  `Dense(128, activation="relu")`
6.  `Dropout(0.5)`
7.  `Dense(1, activation="sigmoid")`

The model is compiled with the Adam optimizer, binary cross-entropy
loss, and accuracy metric.

## Troubleshooting

  ----------------------------------------------------------------------------------
  Issue                               What to check
  ----------------------------------- ----------------------------------------------
  Dataset folder not found            Confirm `Concrete Crack Dataset/Positive` and
                                      `Concrete Crack Dataset/Negative` exist beside
                                      the training script, or update the path in the
                                      script.

  `No module named cv2`               Activate `crack_env` and install dependencies
                                      using
                                      `python -m pip install -r requirements.txt`.

  `cv2` has no `CascadeClassifier`    Check for conflicting OpenCV packages and keep
                                      only `opencv-python`.

  Model file not found                Run the training script first, or place the
                                      `.h5` file beside the scripts that load it.

  Webcam cannot open                  Check Windows camera permissions, close other
                                      camera applications, and try changing
                                      `cv2.VideoCapture(0)` to
                                      `cv2.VideoCapture(1)`.

  Predictions appear inconsistent     Ensure camera frames show concrete surfaces
                                      similar to the training dataset, with adequate
                                      lighting and minimal blur.
  ----------------------------------------------------------------------------------

## Limitations

-   This is a binary image classifier, not a crack-segmentation or
    object-localization model.
-   The webcam script classifies the whole frame, so background objects
    can affect the prediction.
-   Performance depends on the quality, balance, and representativeness
    of the dataset.
-   The provided training script uses the test directory for validation
    during training; keep this limitation in mind when reporting
    performance.
-   Predictions should be treated as model outputs requiring human
    inspection, not as a certified structural-safety assessment.

## Suggested GitHub description

CNN-based concrete surface crack classification using TensorFlow/Keras,
with dataset preprocessing, model evaluation, single-image prediction,
and real-time webcam inference using OpenCV.
