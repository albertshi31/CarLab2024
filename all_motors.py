import RPi.GPIO as GPIO
import time
import threading

# Pin definitions for four motors
motors = {
    1: {'pins': [6, 13, 5, 26]},
    2: {'pins': [10, 11, 9, 14]},
    3: {'pins': [12, 16, 20, 21]},
    4: {'pins': [24, 25, 8, 7]}
}

# Adjust this value for smoother operation
step_sleep = 0.01 / 4
step_count = 800  

# Step sequence
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

for motor_id, motor_data in motors.items():
    for pin in motor_data['pins']:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def cleanup():
    """Ensure GPIO pins are set to LOW and clean up."""
    for motor_id, motor_data in motors.items():
        for pin in motor_data['pins']:
            GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()
    print("GPIO cleanup completed.")

# Global flag to stop threads
stop_threads = False

# Function to move the motor by a specific number of steps
def move_motor_to_position(motor_id, steps):
    motor_pins = motors[motor_id]['pins']
    motor_step_counter = 0
    direction = steps > 0  # True for clockwise, False for counter-clockwise
    steps = abs(steps)  # Ensure steps are positive for the loop

    for _ in range(steps):
        if stop_threads:
            return
        for pin in range(0, len(motor_pins)):
            GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
        if direction:
            motor_step_counter = (motor_step_counter - 1) % 8
        else:
            motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep(step_sleep)

# Motor control function
def drive_motor(motor_id):
    # Move motor to -100 degrees position
    steps_for_100_deg = -100 * (step_count / 360)
    move_motor_to_position(motor_id, steps_for_100_deg)

    motor_pins = motors[motor_id]['pins']
    motor_step_counter = 0
    direction = False  # False for counter-clockwise, True for clockwise

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

# Main execution
threads = []

try:
    # Start threads for each motor
    for motor_id in motors.keys():
        t = threading.Thread(target=drive_motor, args=(motor_id,))
        threads.append(t)
        t.start()

    # Keep the main program running to allow threads to operate
    while True:
        time.sleep(0.1)  # Adjust as needed

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
