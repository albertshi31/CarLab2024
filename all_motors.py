import RPi.GPIO as GPIO
import time
import threading

# Pin definitions for four motors
motors = {
    1: {'pins': [6, 13, 5, 26]},
    2: {'pins': [10, 11, 9, 4]},
    3: {'pins': [12, 16, 20, 21]},
    4: {'pins': [24, 25, 8, 7]}
}

# Adjust this value for smoother operation
step_sleep = 0.01
step_count = 4096  # Adjust based on motor specs

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
    for motor_id, motor_data in motors.items():
        for pin in motor_data['pins']:
            GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

# Motor control function
def drive_motor(motor_id):
    motor_pins = motors[motor_id]['pins']
    motor_step_counter = 0
    direction = False  # False for counter-clockwise, True for clockwise

    try:
        while True:  # Run indefinitely
            for i in range(step_count):
                for pin in range(0, len(motor_pins)):
                    GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
                if direction:
                    motor_step_counter = (motor_step_counter - 1) % 8
                else:
                    motor_step_counter = (motor_step_counter + 1) % 8
                time.sleep(step_sleep)
            # Reverse direction after completing step_count steps
            direction = not direction
    except KeyboardInterrupt:
        cleanup()
        exit(1)

# Start threads for each motor
threads = []
for motor_id in motors.keys():
    t = threading.Thread(target=drive_motor, args=(motor_id,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

cleanup()
