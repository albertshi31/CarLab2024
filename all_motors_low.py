# import RPi.GPIO as GPIO

# # Define the motor pin configurations
# motors = {
#     1: {'pins': [6, 13, 5, 26]},
#     2: {'pins': [17, 27, 22, 23]},
#     3: {'pins': [12, 16, 20, 21]},
#     4: {'pins': [24, 25, 8, 7]}
# }

# # Setup GPIO
# GPIO.setmode(GPIO.BCM)

# # Iterate through each motor and set its pins to output and low
# for motor_id, motor_config in motors.items():
#     for pin in motor_config['pins']:
#         GPIO.setup(pin, GPIO.OUT)  # Set pin as output
#         GPIO.output(pin, GPIO.LOW)  # Set pin to low

# # Print status to confirm
# print("All motor pins have been set to LOW.")

# # Clean up GPIO at the end if needed (uncomment the line below if you're done with the pins)
# # GPIO.cleanup()

import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)

# Toggle pin 27
print("Setting GPIO pin 27 HIGH for 2 seconds.")
GPIO.output(27, GPIO.HIGH)
time.sleep(2)

print("Setting GPIO pin 27 LOW.")
GPIO.output(27, GPIO.LOW)

# Optional cleanup
# GPIO.cleanup()
