import speech_recognition as sr
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
            subprocess.Popen(['python3', 'all_motors.py']) 
            laser_detection_running = True

        elif 'stop' in command and laser_detection_running:
            print("Stopping laser detection.")
            # Kill the laser detection process
            if laser_process:
                # Send a termination signal to the subprocess
                laser_process.kill()
                laser_process = None   
                laser_detection_running = False
                print("Laser detection process stopped.")

        else:
            print("Command not recognized or laser detection already in progress.")
    
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    # Continuous voice command listening
    while True:
        recognize_command()
