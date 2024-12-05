import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the pin where the PWM signal will be sent (e.g., GPIO18)
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)

# Create a PWM instance with a frequency of 50Hz (common frequency for servos)
pwm = GPIO.PWM(servo_pin, 50)

# Start PWM with 0% duty cycle (off)
pwm.start(0)

def set_angle(angle):
    # Convert the angle to a duty cycle (duty cycle for 0° = 2.5%, and 180° = 12.5%)
    duty = angle / 18 + 2.5
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Wait for the servo to move

try:
    while True:
        # Move the servo to different angles
        for angle in range(0, 180, 10):
            set_angle(angle)
        for angle in range(180, 0, -10):
            set_angle(angle)

except KeyboardInterrupt:
    pass

# Stop the PWM and clean up
pwm.stop()
GPIO.cleanup()
