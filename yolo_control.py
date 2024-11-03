import cv2
import numpy as np



def mouse_event(event, x, y, flags, param):
    # Check if the click is within the button's boundaries
    if event == cv2.EVENT_LBUTTONDOWN:
        if button_position[0] <= x <= button_position[0] + button_position[2] and \
           button_position[1] <= y <= button_position[1] + button_position[3]:
            print("Button clicked!")

image = np.ones((500, 800, 3), dtype="uint8") * 255

# Draw a button (rectangle)
button_position = (100, 50, 200, 100)  # x, y, width, height
cv2.rectangle(image, (button_position[0], button_position[1]),
              (button_position[0] + button_position[2], button_position[1] + button_position[3]),
              (200, 200, 200), -1)  # Gray button with filled color

# Add text to the button
cv2.putText(image, "Drehen Links", (button_position[0] + 10, button_position[1] + 60),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# Draw a slider bar
slider_position = (100, 200, 300, 10)  # x, y, width, height
cv2.rectangle(image, (slider_position[0], slider_position[1]),
              (slider_position[0] + slider_position[2], slider_position[1] + slider_position[3]),
              (200, 200, 200), -1)  # Gray bar

# Draw the slider knob
knob_position = (int(slider_position[0] + slider_position[2] * 0.5), slider_position[1] + slider_position[3] // 2)
cv2.circle(image, knob_position, 15, (0, 0, 255), -1)  # Red knob

# Draw a circle indicator (like a light)
indicator_position = (100, 400)
cv2.circle(image, indicator_position, 20, (0, 255, 0), -1)  # Green light

# Add text labels
cv2.putText(image, "Slider", (slider_position[0], slider_position[1] - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
cv2.putText(image, "Indicator Light", (indicator_position[0] + 30, indicator_position[1] + 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)


# Display the image
cv2.imshow("Image with Controls", image)
cv2.setMouseCallback("Image with Controls", mouse_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
