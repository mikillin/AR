from ultralytics import YOLO
import cv2

# Load a pretrained YOLOv5 model, like yolov5s (YOLOv8 models can also be loaded similarly)
model = YOLO("../runs/detect/train/weights/best.pt")  # replace with your model path if it's custom-trained
# model = YOLO("yolo11n.pt")  # replace with your model path if it's custom-trained


# Option 2: Use an OpenCV image

image = cv2.imread("image.jpg")
results = model.predict(source=image)

for result in results[0].boxes:

    # Get bounding box coordinates and convert them to integers
    x1, y1, x2, y2 = map(int, result.xyxy[0])

    label = model.names[int(result.cls)]
    confidence = result.conf[0]

    # Format the label with confidence
    label_text = f"{label} {confidence:.2f}"

    # Draw the bounding box
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box

    # Put the label text above the bounding box
    cv2.putText(image, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Filename
filename = 'result.jpg'

# Using cv2.imwrite() method
# Saving the image
cv2.imwrite(filename, image)
