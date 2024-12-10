# import speech_recognition as sr

# recognizer = sr.Recognizer()

# with sr.Microphone() as source:
#     print("Say something:")
#     audio = recognizer.listen(source)
#     try:
#         print("You said: " + recognizer.recognize_google(audio))
#     except sr.UnknownValueError:
#         print("Sorry, I didn't understand that.")
#     except sr.RequestError:
#         print("Could not request results; check your internet connection.")

import speech_recognition as sr

# Define your functions to run based on commands
def say_hello():
    print("Hello there!")

def turn_on_lights():
    print("Lights turned on!")

def play_music():
    print("Playing music!")

# Create a function to handle voice commands
def recognize_command():
    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something...")
        # Adjust for ambient noise and listen
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Recognize speech using Google Speech Recognition
    try:
        # Convert speech to text
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")

        # Match the command and trigger the corresponding function
        if 'hello' in command:
            say_hello()
        elif 'lights on' in command:
            turn_on_lights()
        elif 'play music' in command:
            play_music()
        else:
            print("Sorry, I didn't understand that.")

    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Main loop to keep the program running
if __name__ == "__main__":
    while True:
        recognize_command()
