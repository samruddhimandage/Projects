
import cv2
import numpy as np
import tensorflow as tf
import json

# Load trained CNN model
model = tf.keras.models.load_model(
    "models/emotion_model.keras"
)

# Load emotion labels
with open("models/labels.json", "r") as f:
    emotion_labels = json.load(f)

# Load Haar Cascade face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(
        frame, cv2.COLOR_BGR2GRAY
    )

    # Detect faces
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:

        # Extract face
        face = gray[y:y+h, x:x+w]

        # Resize face to 48x48
        face = cv2.resize(face, (48, 48))

        # Normalize image
        face = face.astype("float32") / 255.0

        # Reshape for CNN input
        face = np.reshape(
            face, (1, 48, 48, 1)
        )

        # Predict emotion
        predictions = model.predict(
            face, verbose=0
        )

        emotion_index = np.argmax(predictions)
        confidence = predictions[0][emotion_index]

        emotion = emotion_labels[emotion_index]

        # Draw bounding box
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        # Display emotion and confidence
        label = f"{emotion}: {confidence*100:.1f}%"

        cv2.putText(
            frame,
            label,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    # Display webcam output
    cv2.imshow(
        "Real-Time Emotion Detection",
        frame
    )

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
