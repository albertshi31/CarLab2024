# import speech_recognition as sr
# import RPi.GPIO as GPIO
# import time
# import pixy
# from ctypes import *
# from pixy import *
# import threading  # Import threading

# # GPIO setup
# GPIO.setmode(GPIO.BCM)
# servo_pin = 18
# GPIO.setup(servo_pin, GPIO.OUT)
# pwm_servo = GPIO.PWM(servo_pin, 50)
# pwm_servo.start(7.5)

# # Motor control setup
# motor_pin = 19
# GPIO.setup(motor_pin, GPIO.OUT)
# pwm_motor = GPIO.PWM(motor_pin, 100)
# pwm_motor.start(0)

# # Initialize Pixy2 and set to color_connected_components program
# pixy.init()
# pixy.change_prog("color_connected_components")

# # Define class for blocks returned by Pixy2
# class Blocks(Structure):
#     _fields_ = [
#         ("m_signature", c_uint),
#         ("m_x", c_uint),
#         ("m_y", c_uint),
#         ("m_width", c_uint),
#         ("m_height", c_uint),
#         ("m_angle", c_uint),
#         ("m_index", c_uint),
#         ("m_age", c_uint)
#     ]

# blocks = BlockArray(5)

# green_signature = 2  # Signature for green laser

# # Global flag to stop the laser detection
# stop_laser_detection = False

# def map_x_to_servo(x_position, min_x=0, max_x=319, min_angle=0, max_angle=180):
#     return (x_position - min_x) * (max_angle - min_angle) / (max_x - min_x) + min_angle

# def map_y_to_speed(y_position, min_y=0, max_y=239, min_speed=50, max_speed=65):
#     return (1 - ((y_position - min_y) / (max_y - min_y))) * (max_speed - min_speed) + min_speed

# def detect_laser():
#     global stop_laser_detection  # Access the global flag

#     while not stop_laser_detection:
#         count = pixy.ccc_get_blocks(5, blocks)

#         if count > 0:
#             for index in range(count):
#                 block = blocks[index]
#                 if block.m_signature == green_signature:
#                     print("Laser detected!")
#                     print(f"  Signature: {block.m_signature}")
#                     print(f"  Position: ({block.m_x}, {block.m_y})")
#                     print(f"  Width: {block.m_width}, Height: {block.m_height}")
#                     print(f"  Angle: {block.m_angle}")
#                     print(f"  Object Age: {block.m_age}")

#                     # Move servo based on laser X position
#                     laser_x_position = block.m_x
#                     angle = map_x_to_servo(laser_x_position)
#                     pwm_servo.ChangeDutyCycle((angle / 18) + 2.5)
#                     time.sleep(0.1)

#                     # Adjust motor speed based on laser Y position
#                     laser_y_position = block.m_y
#                     speed = map_y_to_speed(laser_y_position)
#                     pwm_motor.ChangeDutyCycle(speed)
#                     time.sleep(0.1)

#         else:
#             print("No laser detected")
#             pwm_motor.ChangeDutyCycle(40)

#         time.sleep(0.1)  # Avoid high CPU usage

#     print("Laser detection stopped.")

# def turn_on_lights():
#     print("Lights turned on!")

# def play_music():
#     print("Playing music!")

# def recognize_command():
#     global stop_laser_detection  # Access the global flag

#     recognizer = sr.Recognizer()

#     with sr.Microphone() as source:
#         print("Say something...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

#     try:
#         command = recognizer.recognize_google(audio).lower()
#         print(f"You said: {command}")

#         if 'laser' in command:
#             if stop_laser_detection:  # If laser detection is already stopped, start it again
#                 stop_laser_detection = False
#                 print("Starting laser detection.")
#                 # Start laser detection in a new thread
#                 laser_thread = threading.Thread(target=detect_laser)
#                 laser_thread.start()
#             else:
#                 print("Laser detection is already running.")
#         elif 'stop' in command:
#             stop_laser_detection = True
#             print("Stopping laser detection.")
#         elif 'lights on' in command:
#             turn_on_lights()
#         elif 'play music' in command:
#             play_music()
#         else:
#             print("Sorry, I didn't understand that.")
#     except sr.UnknownValueError:
#         print("Sorry, I could not understand your speech.")
#     except sr.RequestError as e:
#         print(f"Could not request results from Google Speech Recognition service; {e}")

# if __name__ == "__main__":
#     # Start by listening for commands
#     while True:
#         recognize_command()

import time
import speech_recognition as sr
import RPi.GPIO as GPIO
import pixy
from ctypes import *
from pixy import *

GPIO.setmode(GPIO.BCM)
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)
pwm_servo = GPIO.PWM(servo_pin, 50)  # 50Hz frequency (standard for servos)
pwm_servo.start(7.5)  # Initial position (centered at 90 degrees)

# Setup GPIO for Motor control (GPIO13)
motor_pin = 19
GPIO.setup(motor_pin, GPIO.OUT)
pwm_motor = GPIO.PWM(motor_pin, 100)  # Motor speed PWM (use 100Hz for speed control)
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

# Function to map X position to servo angle
def map_x_to_servo(x_position, min_x=0, max_x=319, min_angle=0, max_angle=180):
    # Map the X position (range: min_x to max_x) to an angle (range: min_angle to max_angle)
    return (x_position - min_x) * (max_angle - min_angle) / (max_x - min_x) + min_angle

# Function to map Y position to motor speed
def map_y_to_speed(y_position, min_y=0, max_y=239, min_speed=50, max_speed=65):
    # Map the Y position (range: min_y to max_y) to speed (range: min_speed to max_speed)
    return (1 -((y_position - min_y) / (max_y - min_y))) * (max_speed - min_speed)+ min_speed

# Laser detection and command recognition loop
stop_laser_detection = False

def detect_laser():
    global stop_laser_detection
    while not stop_laser_detection:
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
                angle = map_x_to_servo(laser_x_position)

                # Move the servo to the calculated angle
                print(f"Moving servo to angle: {angle}")
                # pwm_servo.ChangeDutyCycle(angle)  # Convert angle to PWM duty cycle (2.5%-12.5%)
                pwm_servo.ChangeDutyCycle((angle / 18) + 2.5)
                time.sleep(0.1)  # Small delay for smooth servo movement

                # Map Y position of laser to motor speed
                laser_y_position = block.m_y
                speed = map_y_to_speed(laser_y_position)

                # Set motor speed based on Y position
                print(f"Setting motor speed to: {speed}%")
                pwm_motor.ChangeDutyCycle(speed)  # Change duty cycle to control motor speed
                time.sleep(0.1)  # Small delay to allow for smooth speed change
                
    else:
        print(f"No laser detected")
        pwm_motor.ChangeDutyCycle(40)

    time.sleep(0.1)  # Small delay to avoid excessive CPU usage

def recognize_command():
    global stop_laser_detection

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")

        if 'laser' in command:
            if stop_laser_detection:
                stop_laser_detection = False
                print("Starting laser detection.")
                detect_laser()  # No threading, will block here
            else:
                print("Laser detection is already running.")
        elif 'stop' in command:
            stop_laser_detection = True
            print("Stopping laser detection.")
        else:
            print("Sorry, I didn't understand that.")
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    # Main loop
    while True:
        recognize_command()
        time.sleep(0.1)

