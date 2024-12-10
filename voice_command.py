import speech_recognition as sr
import RPi.GPIO as GPIO
import subprocess
import os
import signal

# Flag to track the laser detection status
laser_detection_running = False
laser_process = None  # To store the Popen object of the laser detection process

def recognize_command():
    global laser_detection_running, laser_process

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")

        if 'laser' in command and not laser_detection_running:
            print("Starting laser detection.")
            # Run the laser detection script with sudo
            laser_process = subprocess.Popen(['sudo', 'python3', 'detect_green.py'])  # Start laser tracking
            laser_detection_running = True

        elif 'stop' in command and laser_detection_running:
            print("Stopping laser detection.")
            # Kill the laser detection process
            if laser_process:
                # Send a termination signal to the subprocess
                laser_process.kill()
                laser_process = None   
                laser_detection_running = False
                GPIO.setmode(GPIO.BCM)
                servo_pin = 18
                GPIO.setup(servo_pin, GPIO.OUT)
                pwm_servo = GPIO.PWM(servo_pin, 50)  # 50Hz frequency (standard for servos)
                pwm_servo.start(7.5)  # Initial position (centered at 90 degrees)

                # Setup GPIO for Motor control (GPIO13)
                motor_pin = 19
                GPIO.setup(motor_pin, GPIO.OUT)
                pwm_motor = GPIO.PWM(motor_pin, 50)  # Motor speed PWM (use 100Hz for speed control)
                pwm_motor.start(0)  # Start with motor off (0% duty cycle)
                print("Laser detection process stopped.")

        else:
            print("Command not recognized or laser detection already in progress.")
    
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    # Continuous voice command listening
    subprocess.Popen(['python3', 'all_motors.py']) 
    while True:
        recognize_command()
