import cv2
import numpy as np
import math

from sympy.physics.units.definitions.dimension_definitions import angle

from yolo_stl import rotateSTL


angle_x =0
angle_y =0
angle_z =0

def arrows(source_image ):
    image = np.ones((100, 100, 3), dtype="uint8") * 255

    # Define the circle center and radius
    center = (50, 50)
    radius = 50

    # Define the arrow length
    arrow_length = 50

    # Calculate the end points of the arrows at 0°, 90°, 180°, and 270°
    angles = [0, 90, 180, 270]
    for angle in angles:
        # Convert the angle to radians
        rad = math.radians(angle)

        # Calculate the start point of the arrow along the circle's radius
        start_point = (int(center[0] - radius * math.cos(rad)),
                       int(center[1] - radius * math.sin(rad)))

        # Calculate the end point of the arrow
        end_point = (int(center[0] + ( arrow_length) * math.cos(rad)),
                     int(center[1] + ( arrow_length) * math.sin(rad)))

        # Draw the arrow
        cv2.arrowedLine(image, start_point, end_point, (0, 255, 0), 2, tipLength=0.2)

    # Draw the circle to visualize the radius (optional)
    cv2.circle(image, center, radius, (0, 255, 0), 1)

    # Specify the top-left corner where the small image will be placed
    x_offset = 50
    y_offset = 100

    # Ensure the small image fits within the bounds of the large image
    y1, y2 = y_offset, y_offset + image.shape[0]
    x1, x2 = x_offset, x_offset + image.shape[1]

    # cv2.imshow("Image with Controls", source_image)
    # print("source_image")
    # cv2.waitKey(0)
    # cv2.imshow("Image with Controls", image)
    # print("image")
    # cv2.waitKey(0)

    ### filter white color
    # Define the color to treat as transparent in the overlay image
    transparent_color = (255, 255, 255)  # White color

    # Resize overlay if needed to match a specific area on the base image
    # overlay_img = cv2.resize(image, (base_img.shape[1], base_img.shape[0]))

    # Create a mask where the defined color is treated as transparent
    mask = cv2.inRange(image, transparent_color, transparent_color)

    # Invert the mask to get the non-transparent parts
    mask_inv = cv2.bitwise_not(mask)

    # Use the mask to extract only the colored parts of the overlay image
    overlay_img_fg = cv2.bitwise_and(image, image, mask=mask_inv)

    cv2.imshow("Image with Controls", overlay_img_fg)
    print("overlay_img_fg")
    # cv2.waitKey(0)

    # Extract the region of interest (ROI) from the base image
    base_img_bg = cv2.bitwise_and(source_image[y1:y2, x1:x2], source_image[y1:y2, x1:x2], mask=mask)


    # cv2.imshow("Image with Controls", base_img_bg)
    # print("base_img_bg")
    # cv2.waitKey(0)

    # Combine the overlay image with the base image
    # combined_img = cv2.add(base_img_bg, overlay_img_fg)

    # cv2.imshow("Image with Controls", combined_img)
    # print("combined_img")
    # cv2.waitKey(0)

    # Overlay the small image on the large image
    source_image[y1:y2, x1:x2] = base_img_bg
    # print("sousrce_image")
    # cv2.waitKey(0)
    return source_image



def detect_sector(event, x, y, flags, param):
    global angle_x, angle_y, angle_z

    center = (50, 50)
    radius = 50
    num_sectors = 4
    x_offset = 50
    y_offset = 100

    if event == cv2.EVENT_LBUTTONDOWN:
        # Calculate distance from the center
        dx, dy = x - x_offset - center[0], y - y_offset - center[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Check if the click is within the circle
        if distance <= radius:
            # Calculate the angle of the click
            angle = math.degrees(math.atan2(dy, dx)) + 45
            if angle < 0:
                angle += 360  # Convert angle to range [0, 360)

            # Determine which sector contains the angle
            sector = int(angle // (360 / num_sectors))

            ## todo: add correct angles
            print(f"Clicked in Sector {sector + 1}")

            match sector + 1:
                case 1:
                    angle_x += 30
                case 2:
                    angle_y -= 30
                case 3:
                    angle_x -= 30
                case 4:
                    angle_y += 30
                case _:
                    angle_y = angle_y

            image = rotateSTL("sun.stl", angle_x ,angle_y, angle_z )
            # cv2.imwrite('rotated.png', image)
            cv2.imshow("Image with Controls", arrows(image))

def main():

    image = rotateSTL("sun.stl", angle_x, angle_y, angle_z)
    # cv2.imwrite('rotated.png', image)
    cv2.imshow("Image with Controls", arrows(image))
    #todo uncomment
    # image = np.ones((500, 800, 3), dtype="uint8") * 255

    # Draw a button (rectangle)
    button_position = (100, 50, 200, 100)  # x, y, width, height
    # cv2.rectangle(image, (button_position[0], button_position[1]),
    #               (button_position[0] + button_position[2], button_position[1] + button_position[3]),
    #               (200, 200, 200), -1)  # Gray button with filled color

    # # Add text to the button
    # cv2.putText(image, "Drehen Links", (button_position[0] + 10, button_position[1] + 60),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    ## image = arrows(image)

    # Display the image
    cv2.imshow("Image with Controls", image)
    cv2.setMouseCallback("Image with Controls", detect_sector)
    rotateSTL()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()