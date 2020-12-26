import speech_recognition as sr
import requests
import io
import os
from gtts import gTTS


r = sr.Recognizer()
mic = sr.Microphone()

# HOME API ADDRESS
#baseURL = 'http://192.168.1.193:8060/'
baseURL = 'http://192.168.0.81:8060/'


startKeyWords = ['watch', 'open', 'choose', 'play' 'select', 'up', 'turn on', 'get', 'find']
afterTitleKeyWords = ['on', 'in', 'with', 'through']
mediaPlatforms = ['netflix', 'hulu', 'prime', 'disney', 'spotify', 'youtube']


def main():
  print('Started')
  with mic as source:
    while(True):
      print('Listening...')
      r.adjust_for_ambient_noise(source)
      audio = r.listen(source)
      results = r.recognize_google(audio, language='en-US', show_all=True)
      print(results)
      words = ' '
      if  'alternative' in results:
        words = results['alternative'][0]['transcript'].lower()
      
      print(words)
      #speak(words)
      if 'roku' in words:
        #Power
        if 'power' in words:
          if 'on' in words:
            requests.post(baseURL + 'power/on', data={})
            speak('Powering on Roku')
          elif 'off' in words or 'down' in words:
            speak('Powering down Roku')
            requests.post(baseURL + 'power/off', data={})
        #Main commands
        firstKW = containsKeyWord(words, startKeyWords)
        secondKW = containsKeyWord(words, afterTitleKeyWords)
        platform = getPlatform(words)

        if firstKW and platform:
          if secondKW:
            #Play media (movie, show, or song)
            mediaTitle = getMediaTitle(words, firstKW, secondKW)
            requests.post(f'{baseURL}start/{platform}/{mediaTitle}', data={})
            speak(f'Searching {platform} for {mediaTitle}')
          else:
            #Open platform
            requests.post(f'{baseURL}start/{platform}', data={})
            speak(f'Opening {platform}')
        else:
          speak('Unrecognized input. Could you repeat that please?')

      elif 'stop' in words:
        speak('shutting down')
        break


def containsKeyWord(inputString, keyWords):
  for word in keyWords:
    if word in inputString: return word
  return False

def getMediaTitle(inputString, firstKW, secondKW):
  startingKeyWord = ' '
  firstKWIndex = inputString.find(firstKW)
  secondKWIndex = inputString.rfind(secondKW)
  startIndex = firstKWIndex + len(firstKW) + 1
  return inputString[startIndex:secondKWIndex]

def getPlatform(inputString):
  return containsKeyWord(inputString, mediaPlatforms)

def speak(outputText):
  f = io.BytesIO()
  tts = gTTS(text=outputText, lang='en', slow=False)
  tts.save('tempAudioOut.mp3')
  os.system('mpg321 tempAudioOut.mp3')


if __name__ == '__main__':
  main()
