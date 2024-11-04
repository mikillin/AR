import cv2
import mediapipe as mp
from ultralytics import YOLO
import math


# Function to calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)


def main():
    # Initialize MediaPipe Hands module
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    click_threshold = 0.15  # A small value for normalized distances

    model = YOLO("yolo11n.pt")

    # results = model.yolo11(data="coco8.yaml", epochs=100, imgsz=640)

    # Initialize MediaPipe Drawing module for drawing landmarks
    mp_drawing = mp.solutions.drawing_utils

    # Open a video capture object (0 for the default camera)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            continue

        # Convert the frame to RGB format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame to detect hands
        results = hands.process(frame_rgb)

        # Check if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if len(hand_landmarks.landmark) > 8:
                    # Get the tip of the index finger (landmark 8) and thumb tip (landmark 4)
                    index_tip = hand_landmarks.landmark[8]
                    thumb_tip = hand_landmarks.landmark[4]

                    # Calculate the distance between the index finger tip and thumb tip
                    distance = calculate_distance(index_tip, thumb_tip)

                    print(f"Distance between thumb and index finger tips: {distance}")

                    # Check if the distance is below the threshold (indicating a "click")
                    if distance < click_threshold:
                         print("Click detected!")

        # Display the frame with hand landmarks
        cv2.imshow('Hand Recognition', frame)
        # cv2.imshow('Hand Recognition', frame_rgb)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


# def main():
#     print("Hello World!")

if __name__ == "__main__":
    main()
