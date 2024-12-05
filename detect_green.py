# from __future__ import print_function
# import pixy
# from ctypes import *
# from pixy import *

# # Initialize Pixy2 and set it to the "color_connected_components" program.
# pixy.init()
# pixy.change_prog("color_connected_components")

# # Define a class for the Blocks (detected objects) that the Pixy2 will return.
# class Blocks(Structure):
#     _fields_ = [
#         ("m_signature", c_uint),  # Signature of the detected object
#         ("m_x", c_uint),          # X position of the object
#         ("m_y", c_uint),          # Y position of the object
#         ("m_width", c_uint),      # Width of the detected object
#         ("m_height", c_uint),     # Height of the detected object
#         ("m_angle", c_uint),      # Angle of the detected object
#         ("m_index", c_uint),      # Index of the detected object
#         ("m_age", c_uint)         # Age of the detected object
#     ]

# # Create a BlockArray to hold up to 5 detected blocks.
# blocks = BlockArray(5)

# # Initialize the frame counter.
# #frame = 0

# # Set the signature value for detecting the green color.
# # The signature is configured on the Pixy2 through the PixyMon tool, 
# # and the green color usually gets signature 1, but verify this in PixyMon.
# green_signature = 2

# # Start tracking the green laser
# while True:
#     count = pixy.ccc_get_blocks(5, blocks)  # Get up to 5 blocks (objects) from the Pixy2 camera.
    
#     if count > 0:
#         for index in range(count):
#             # Get the signature and the coordinates of each block (object).
#             block = blocks[index]
#             if block.m_signature == green_signature:  # We are looking for green objects.
#                 print(f"Laser detected!")
#                 print(f"  Signature: {block.m_signature}")
#                 print(f"  Position: ({block.m_x}, {block.m_y})")
#                 print(f"  Width: {block.m_width}, Height: {block.m_height}")
#                 print(f"  Angle: {block.m_angle}")
#                 print(f"  Object Age: {block.m_age}")
                
#                 # You could add additional code here to track the object, e.g.:
#                 # - Draw a bounding box around the green circle
#                 # - Track its movement over time
#                 # - Command servos to follow the circle, etc.
#     else:
#         print(f"No laser detected")

import RPi.GPIO as GPIO
import time
import pixy
from ctypes import *
from pixy import *

# Setup GPIO for Servo control (GPIO18)
GPIO.setmode(GPIO.BCM)
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz frequency (standard for servos)
pwm.start(7.5)  # Initial position (centered at 90 degrees)

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

# Create a BlockArray to hold up to 5 detected blocks.
blocks = BlockArray(5)

# Signature for the green laser (adjust if needed)
green_signature = 2

# Function to map X position to servo angle
def map_x_to_angle(x_position, min_x=0, max_x=319, min_angle=0, max_angle=180):
    # Map the X position (range: min_x to max_x) to an angle (range: min_angle to max_angle)
    return (x_position - min_x) * (max_angle - min_angle) / (max_x - min_x) + min_angle

# Start tracking the green laser
while True:
    count = pixy.ccc_get_blocks(5, blocks)  # Get up to 5 blocks (objects) from the Pixy2 camera.

    if count > 0:
        for index in range(count):
            block = blocks[index]
            if block.m_signature == green_signature:  # Check for green laser
                print(f"Laser detected!")
                print(f"  Signature: {block.m_signature}")
                print(f"  Position: ({block.m_x}, {block.m_y})")
                print(f"  Width: {block.m_width}, Height: {block.m_height}")
                print(f"  Angle: {block.m_angle}")
                print(f"  Object Age: {block.m_age}")

                # Map X position of laser to servo angle
                laser_x_position = block.m_x
                angle = map_x_to_angle(laser_x_position)

                # Move the servo to the calculated angle
                print(f"Moving servo to angle: {angle}")
                pwm.ChangeDutyCycle((angle / 18) + 2.5)  # Convert angle to PWM duty cycle (2.5%-12.5%)
                time.sleep(0.1)  # Small delay for smooth servo movement
                
    else:
        print(f"No laser detected")

    time.sleep(0.1)  # Small delay to avoid excessive CPU usage

# Clean up on exit
pwm.stop()
GPIO.cleanup()
