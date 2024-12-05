import RPi.GPIO as GPIO
import time

# Setup GPIO18 for PWM
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Create PWM instance with 50Hz frequency (standard for servo motors)
pwm = GPIO.PWM(19, 50)

# Start PWM with 0% duty cycle (initially off)
pwm.start(0)

# Move the servo to 90 degrees (7.5% duty cycle)
pwm.ChangeDutyCycle(7.5)  # 7.5% corresponds to 90 degrees
time.sleep(1)  # Wait for 1 second

# Stop PWM and clean up
pwm.stop()
GPIO.cleanup()

