import RPi.GPIO as GPIO
import time
import threading

# Code adapted from https://ben.akrin.com/driving-a-28byj-48-stepper-motor-uln2003-driver-with-a-raspberry-pi/

# Pin definitions for four motors
motors = {
    1: {'pins': [6, 13, 5, 26]},
    2: {'pins': [10, 11, 9, 14]},
    3: {'pins': [12, 16, 20, 21]},
    4: {'pins': [24, 25, 8, 7]}
}

# The step_sleep determines how fast the stepper motors rotate
# a lower number means that the motor "sleeps" for a shorter amount of time
step_sleep = 0.01 / 4
# This determines the rotation of the stepper motor based on # of steps for a motor to complete 1 revolution
step_count = 800  

# Step sequence for the motor
step_sequence = [[1, 0, 0, 1],
                 [1, 0, 0, 0],
                 [1, 1, 0, 0],
                 [0, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 1],
                 [0, 0, 0, 1]]

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Sets up each motor & initializes GPIO pins as output pins, ensuring that GPIO pins are initially set to LOW (off) 
# Makes sure no motors are inadvertently powered on at startup
for motor_id, motor_data in motors.items():
    for pin in motor_data['pins']:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

# Cleanup function to ensure no residual charge or errors in future runs
def cleanup():
    """Ensure GPIO pins are set to LOW and clean up."""
    for motor_id, motor_data in motors.items():
        for pin in motor_data['pins']:
            GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()
    print("GPIO cleanup completed.")

# Global flag to stop threads
stop_threads = False

# Motor control function
def drive_motor(motor_id):
    motor_pins = motors[motor_id]['pins']
    motor_step_counter = 0
    direction = True  # False for counter-clockwise, True for clockwise

    # Make the stepper motors rotate
    while not stop_threads:
        # Move in one direction (clockwise)
        for i in range(step_count):
            if stop_threads:
                return
            for pin in range(0, len(motor_pins)):
                GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
            if direction:
                motor_step_counter = (motor_step_counter - 1) % 8
            else:
                motor_step_counter = (motor_step_counter + 1) % 8
            time.sleep(step_sleep)

        # Reverse direction (counter-clockwise)
        direction = not direction

        # Move in the opposite direction (counter-clockwise)
        for i in range(step_count):
            if stop_threads:
                return
            for pin in range(0, len(motor_pins)):
                GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
            if direction:
                motor_step_counter = (motor_step_counter - 1) % 8
            else:
                motor_step_counter = (motor_step_counter + 1) % 8
            time.sleep(step_sleep)

        # Reverse direction after each back-and-forth motion
        direction = not direction

# Main execution— Multi-threading so that each motor can run
threads = []

try:
    # Start threads for each motor
    for motor_id in motors.keys():
        t = threading.Thread(target=drive_motor, args=(motor_id,))
        threads.append(t)
        t.start()

    # Keep the main program running to allow threads to operate
    while True:
        time.sleep(0.1) 

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected, stopping motors...")
    # Set global flag to stop threads
    stop_threads = True

finally:
    # Wait for all threads to complete
    for t in threads:
        t.join()
    # Cleanup GPIO
    cleanup()
    print("Program terminated safely.")

