from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
from AppOpener import open,close

import json

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chrome_path))
appID = '7Q2KXT-PURQQWXQHW'
wolframClient = wolframalpha.Client(appID)



engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
activationWord = 'computer'

def speak(text,rate = 120):
    engine.setProperty('rate',rate)
    engine.say(text)
    engine.runAndWait()
def searchWikipedia(query = ''):
    searchresults = wikipedia.search(query)
    if not searchresults:
        print('No wikipedia result')
        return 'No result received'
    try:
       wikipage = wikipedia.page(searchresults[0])
    except wikipedia.DisambiguationError as error:
       wikipage = wikipedia.page(error.options[0])
    print(wikipage.title)
    wikiSummary = str(wikipage.summary)
    return wikiSummary


def listorDict(var):
    if(isinstance(var,list)):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframalpha(query = ''):
    response = wolframClient.query(query)


    if response['@success'] == 'false':
        return 'Could not compute'
    else:
        result = ''
        pod0 = response['pod'][0]

        pod1 = response['pod'][1]



        if(('result') in pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true') or ('definition' in pod1['@title'].lower()):
            result = listorDict(pod1['subpod'])
            return result.split("(")[0]
        else:
            question = listorDict(pod0['subpod'])
            return question.split("(")[0]

            speak('Computation failed. Querying the universal databank')

            return searchWikipedia(question)


def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command...')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech,language = 'en_gb')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'
    return query

if __name__ == '__main__':
    speak('All systems nominal.')


    while True:
        query = parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0)


            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all.')
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)

            if query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)

            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Querying the universal databank...')
                speak(searchWikipedia(query))
            if query[0] == 'compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                speak('Computing')
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak('Unable to compute')
            if query[0] == 'log':
                speak('Ready to record your log!')
                newNote = parseCommand().lower()

                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


                with open('note_%s.txt' % now,'w') as newFile:
                    newFile.write(newNote)
                speak('Log written')
            if query[0] == 'exit':
                speak('Goodbye')
                break
            if query[0] == 'open':
                speak('Opening')
                query = ' '.join(query[1:])
                open(query)
