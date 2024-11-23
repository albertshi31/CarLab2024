import cv2
import numpy as np
from pixy import Pixy2

# Initialize Pixy camera
pixy = Pixy2()
pixy.init()

# Color range for detecting green in HSV color space
lower_green = np.array([35, 50, 50])   # Lower bound for green
upper_green = np.array([85, 255, 255])  # Upper bound for green

# Function to process Pixy camera data
def get_pixy_data():
    # Get the detected blocks from Pixy camera
    pixy_data = pixy.get_blocks()

    # If blocks are detected
    if pixy_data:
        for block in pixy_data:
            # Filter by green color detection logic if needed
            if block.signature == 1:  # For example, green ball could have signature 1
                print(f"Green ball detected! Block x: {block.x}, y: {block.y}, width: {block.width}, height: {block.height}")
                cv2.circle(frame, (block.x, block.y), block.width//2, (0, 255, 0), 3)
    
    return pixy_data

# Initialize the video stream (for Raspberry Pi camera or webcam)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert the frame to HSV color space for easier color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours of the green areas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over contours
    for contour in contours:
        # If the contour is large enough, it's likely the green ball
        if cv2.contourArea(contour) > 500:  # You can adjust the area threshold
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Draw the bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Optionally, draw a circle around the detected green ball
            cv2.circle(frame, (x + w // 2, y + h // 2), min(w, h) // 2, (0, 255, 0), 2)

            print(f"Green ball detected at ({x + w // 2}, {y + h // 2}) with width: {w}, height: {h}")

    # Display the result
    cv2.imshow("Green Ball Detection", frame)

    # Get PixyCam data to detect object signature (for a green ball)
    get_pixy_data()

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
