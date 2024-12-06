import RPi.GPIO as GPIO
import time
import pixy
from ctypes import *
from pixy import *

# Setup GPIO for Motor control (GPIO19)
motor_pin = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin, GPIO.OUT)
pwm_motor = GPIO.PWM(motor_pin, 50)  # Motor speed PWM (use 100Hz for speed control)
pwm_motor.start(0)  # Start with motor off (0% duty cycle)

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

# Function to map Y position to motor speed within the range of 20% to 35%
def map_y_to_speed(y_position, min_y=0, max_y=239, min_speed=40, max_speed=70):
    # Map the Y position (range: min_y to max_y) to speed (range: min_speed to max_speed)
    return (y_position - min_y) * (max_speed - min_speed) / (max_y - min_y) + min_speed

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

                # Map Y position of laser to motor speed
                laser_y_position = block.m_y
                speed = map_y_to_speed(laser_y_position)

                # Set motor speed based on Y position
                print(f"Setting motor speed to: {speed}%")
                pwm_motor.ChangeDutyCycle(speed)  # Change duty cycle to control motor speed
                time.sleep(0.1)  # Small delay to allow for smooth speed change
                
    else:
        print(f"No laser detected")

    time.sleep(0.1)  # Small delay to avoid excessive CPU usage

# Clean up on exit
pwm_motor.stop()
GPIO.cleanup()
