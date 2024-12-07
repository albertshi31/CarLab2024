import RPi.GPIO as GPIO
import time

# Setup GPIO19 for PWM
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)

# Create PWM instance with 50Hz frequency (standard for servo motors)
pwm = GPIO.PWM(19, 50)

# Start PWM with 0% duty cycle (initially off)
pwm.start(0)

# Run indefinitely, keeping the servo at 40% duty cycle
try:
    while True:
        pwm.ChangeDutyCycle(3)  # Adjust duty cycle to the desired position
        time.sleep(0.1)  # Short delay to avoid excessive CPU usage
except KeyboardInterrupt:
    # Gracefully stop PWM and clean up if interrupted
    pwm.stop()
    GPIO.cleanup()
