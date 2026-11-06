
import cv2

print("OpenCV Version:", cv2.__version__)

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

if face_detector.empty():
    print("Face detector loading failed!")
else:
    print("Face detector loaded successfully!")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam not detected!")
else:
    print("Webcam opened successfully!")

cap.release()
