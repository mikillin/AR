from ultralytics import YOLO
import cv2

# Load a pretrained YOLOv5 model, like yolov5s (YOLOv8 models can also be loaded similarly)
model = YOLO("../ultralytics/runs/detect/train/weights/best.pt")  # replace with your model path if it's custom-trained


# Option 2: Use an OpenCV image

image = cv2.imread("image.jpg")
results = model.predict(source=image)

for result in results:
    boxes = result.boxes  # Bounding boxes
    confs = result.confs  # Confidence scores
    labels = result.labels  # Class labels
    for box, conf, label in zip(boxes, confs, labels):
        print(f"Label: {label}, Confidence: {conf}, Box coordinates: {box.xyxy}")