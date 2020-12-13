#import speech_recognition as sr
#import pyttsx3 as tts
import requests

#r = sr.Recognizer()
#out = tts.init()
#mic = sr.Microphone()

baseURL = 'http://192.168.1.193:8060/'

#x = requests.post('http://192.168.1.182:8060/keypress/powerOn', data={})
x = requests.post(baseURL + 'power/off', data={});
print(x.text)
print(x)
print(x.request)
#with mic as source:
#    while(True):
#        r.adjust_for_ambient_noise(source)
#        audio = r.listen(source)
#        words = r.recognize_google(audio)
#        print(words)
#        if 'hi' in words or 'hello' in words:
#            out.say('fuck off mate')
#        elif 'stop' in words:
#            break
