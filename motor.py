#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO pin definitions
in1 = 6
in2 = 13
in3 = 5
in4 = 26

# Motor parameters
step_sleep = 0.01  # Delay between steps
step_count = 4096  # Total steps
direction = False  # True = clockwise, False = counter-clockwise

# Step sequence for motor control
step_sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
]

# Set up GPIO
GPIO.setmode(GPIO.BCM)
motor_pins = [in1, in2, in3, in4]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Cleanup function
def cleanup():
    print("\nCleaning up GPIO...")
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

# Main motor control logic
try:
    motor_step_counter = 0
    print("Starting motor...")
    for i in range(step_count):
        for pin in range(len(motor_pins)):
            GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
        motor_step_counter = (
            motor_step_counter - 1 if direction else motor_step_counter + 1
        ) % len(step_sequence)
        time.sleep(step_sleep)
    print("Motor run completed.")

except KeyboardInterrupt:
    print("\nProcess interrupted by user.")

finally:
    cleanup()
