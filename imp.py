import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

text = "Hello, I am Emin Joy. How are you?"
text_to_speech(text)