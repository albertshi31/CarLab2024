import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something:")
    audio = recognizer.listen(source)
    try:
        print("You said: " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError:
        print("Could not request results; check your internet connection.")
