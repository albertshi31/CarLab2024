import RPi.GPIO as GPIO
import time
import threading

# Pin definitions for four motors
motors = {
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

# Motor control function
def drive_motor(motor_id):
    motor_pins = motors[motor_id]['pins']
    motor_step_counter = 0
    direction = True  # False for counter-clockwise, True for clockwise

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

