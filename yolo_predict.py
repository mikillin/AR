from ultralytics import YOLO
import cv2

# Load a pretrained YOLOv5 model, like yolov5s (YOLOv8 models can also be loaded similarly)
# model = YOLO("../runs/detect/train/weights/best.pt")  # replace with your model path if it's custom-trained
model = YOLO("./detect/train6/weights/last.pt")  # replace with your model path if it's custom-trained


# Option 2: Use an OpenCV image
cam = cv2.VideoCapture(2)

# image = cv2.imread("image.jpg")
# results = model.predict(source=image)


while True:
    ret, frame = cam.read()

    image = frame
    # resize = cv2.resize(frame, (240, 240))
    # image = resize


    results = model.predict(source=image)

    if len(results[0].boxes) >0:
        print ("-------------------------")
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


############################### adding

        overlay = cv2.imread('object.png')

        image1 = overlay
        image2 = image

        if image1.shape != image2.shape:
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

        # Check channels and convert if necessary
        if len(image1.shape) != len(image2.shape):
            if len(image1.shape) == 2:  # If grayscale
                image1 = cv2.cvtColor(image1, cv2.COLOR_GRAY2BGR)
            if len(image2.shape) == 2:  # If grayscale
                image2 = cv2.cvtColor(image2, cv2.COLOR_GRAY2BGR)

        # Now you can safely perform operations
        result = cv2.add(image1, image2)


        added_image = cv2.addWeighted(image1, 0.4, image2, 0.1, 0)


        # added_image = cv2.addWeighted(image, 0.4, overlay, 0.1, 0)

        cv2.imwrite('combined.png', added_image)

        frame = added_image



        # Filename
        filename = 'result.jpg'

        # Using cv2.imwrite() method
        # Saving the image
        cv2.imwrite(filename, image)

    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break
# Release the capture and writer objects
cam.release()
cv2.destroyAllWindows()


def my_function(background):
    print("Hello from a function")
    background = cv2.imread(background, cv2.IMREAD_UNCHANGED)
    foreground = cv2.imread("object.png", cv2.IMREAD_UNCHANGED)

    # normalize alpha channels from 0-255 to 0-1
    alpha_background = background[:,:,3] / 255.0
    alpha_foreground = foreground[:,:,3] / 255.0

    # set adjusted colors
    for color in range(0, 3):
        background[:,:,color] = alpha_foreground * foreground[:,:,color] + \
            alpha_background * background[:,:,color] * (1 - alpha_foreground)

    # set adjusted alpha and denormalize back to 0-255
    background[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255

    # display the image
    cv2.imshow("Composited image", background)
    cv2.waitKey(0)