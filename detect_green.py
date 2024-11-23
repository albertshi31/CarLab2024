from __future__ import print_function
import pixy
from ctypes import *
from pixy import *

# Initialize Pixy2 and set it to the "color_connected_components" program.
pixy.init()
pixy.change_prog("color_connected_components")

# Define a class for the Blocks (detected objects) that the Pixy2 will return.
class Blocks(Structure):
    _fields_ = [
        ("m_signature", c_uint),  # Signature of the detected object
        ("m_x", c_uint),          # X position of the object
        ("m_y", c_uint),          # Y position of the object
        ("m_width", c_uint),      # Width of the detected object
        ("m_height", c_uint),     # Height of the detected object
        ("m_angle", c_uint),      # Angle of the detected object
        ("m_index", c_uint),      # Index of the detected object
        ("m_age", c_uint)         # Age of the detected object
    ]

# Create a BlockArray to hold up to 100 detected blocks.
blocks = BlockArray(100)

# Initialize the frame counter.
frame = 0

# Set the signature value for detecting the green color.
# The signature is configured on the Pixy2 through the PixyMon tool, 
# and the green color usually gets signature 1, but verify this in PixyMon.
green_signature = 1

# Start tracking the green circle.
while True:
    count = pixy.ccc_get_blocks(100, blocks)  # Get up to 100 blocks (objects) from the Pixy2 camera.
    
    if count > 0:
        print(f"Frame {frame}: Detected {count} objects")
        frame += 1
        
        for index in range(count):
            # Get the signature and the coordinates of each block (object).
            block = blocks[index]
            if block.m_signature == green_signature:  # We are looking for green objects.
                print(f"Green Object Detected!")
                print(f"  Signature: {block.m_signature}")
                print(f"  Position: ({block.m_x}, {block.m_y})")
                print(f"  Width: {block.m_width}, Height: {block.m_height}")
                print(f"  Angle: {block.m_angle}")
                print(f"  Object Age: {block.m_age}")
                
                # You could add additional code here to track the object, e.g.:
                # - Draw a bounding box around the green circle
                # - Track its movement over time
                # - Command servos to follow the circle, etc.
    else:
        print(f"Frame {frame}: No green objects detected.")
        frame += 1
