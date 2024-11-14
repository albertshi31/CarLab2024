import time
import cv2
import numpy as np
from pixy import Pixy2

# Initialize Pixy2 camera
pixy = Pixy2()
pixy.init()

# Create a window to display the camera feed
cv2.namedWindow("Pixy2 Camera Feed", cv2.WINDOW_NORMAL)

while True:
    # Get blocks from the camera (Pixy2)
    pixy.get_blocks()

    # If blocks are detected, get the image data
    if pixy.blocks:
        # This assumes Pixy2 is sending RGB image data
        image_data = pixy.get_image_data()

        # Convert the image data to a format OpenCV can work with (numpy array)
        img = np.array(image_data, dtype=np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

        # Display the image using OpenCV
        cv2.imshow("Pixy2 Camera Feed", img)

    # Check for a quit signal (press 'q' to quit)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Cleanup
cv2.destroyAllWindows()
pixy.close()
