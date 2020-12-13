import speech_recognition as sr
import pyttsx3 as tts

r = sr.Recognizer()
out = tts.init()

mic = sr.Microphone()

with mic as source:
    while(True):
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        words = r.recognize_google(audio)
        print(words)
        if 'hi' in words or 'hello' in words:
            out.say('fuck off mate')
        elif 'stop' in words:
            break
