import socket
import sys
import time

from bs4 import BeautifulSoup   
import pyttsx3 # imports library to convert text to speech
import datetime # import library for date and time
import speech_recognition as sr # imports library to input voice prompts
import pyaudio # imports library to use microphone as an input
import wikipedia # wikipedia
import pyjokes # jokes
import psutil 
import pyautogui
import os # to open apps
import wolframalpha 
import smtplib
import webbrowser as wb
import json
import requests
from urllib.request import urlopen
import subprocess
# initializing the engine and converting text to speech
engine=pyttsx3.init()
wolframalpha_app_id='LQP4EK-UU2GLWH4GH'
chromepath="c:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s"
bravepath='C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# here is the function to get the current time
def time_():
    time=datetime.datetime.now().strftime("%I:%M %p") # for 12 hour clock
    speak("The current time is ")
    speak(time)

# here is the function to get the current date
def date_():
    year=datetime.datetime.now().year
    month=datetime.datetime.now().month
    date=datetime.datetime.now().day
    speak("The current date is ")
    speak(date)
    speak(month)
    speak(year)

# this function is used when the user activates JARVIS
def wishme():
    
   

    # greetings
    hour=datetime.datetime.now().hour
    
    if hour>=6 and hour<12:
        speak("Good Morning Sir! ")
    elif hour>=12 and hour< 18:
        speak("Good Afternoon Sir! ")
    elif hour>=18 and hour<24:
        speak("Good Evening Sir! ")
    else:
        speak("Good Night Sir! ")

    speak("Welcome back! ")
    speak("Jarvis at your service. Please tell me how can I help you today? ")

def takeCommand():
    r=sr.Recognizer() # create a recognizer object
    with sr.Microphone() as source: # initialize microphone as the source of input
        print("Listening.... ")
        r.pause_threshold=1 # amount of time to wait for audio input before timinng out is 1 sec
        audio=r.listen(source) # records audio from the microphone

    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-US') # uses google api to convert speech to text
        print(query)
    
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query

def joke():
    result=pyjokes.get_joke()
    part = result.split('<', 1)[0]
    print(part)
    speak(result)
    
def screenshot():
    img=pyautogui.screenshot()
    speak('Name of screenshot Sir? ')
    name=takeCommand().lower()
    img.save(f'C:/Desktop/{name}.png')
    speak("I have taken the screenshot Sir")

def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('anshulraina.2021@vitstudent.ac.in','Forgot_password00')
    server.sendmail('anshulraina.2021@vitstudent.ac.in',to,content)
    server.close()

def cpu():
    usage=str(psutil.cpu_percent())
    speak('CPU is at '+usage)
    print('CPU is at '+usage)
    battery=psutil.sensors_battery()
    speak('Battery is at')
    speak(battery.percent)
    print(f'Battery is at {battery.percent}')

def googleSearch(query):
    url=f"https://search.brave.com/search?q={query}"
    wb.get(chromepath).open(url)
    
def youtubeSearch(query):
    url=f"https://www.youtube.com/results?search_query={query}"
    wb.get(chromepath).open(url)    
    
if __name__=="__main__":
    wishme()
    while True:
        query=takeCommand().lower() # take audio prompt as input and convert to lower case for improving the accuracy  
        
        if 'time' in query:
            time_()
        
        if 'date' in query:
            date_() 
        
        elif 'who are you' in query:
            print('My name is Jarvis')
            speak('My name is Jarvis')
            print('I can do everything my creator programmed me to do')
            speak('I can do everything my creator programmed me to do')
        
        elif 'who created you' in query:
            print('I was created by Sir, Anshul Raina. I was created with python language in Visual Studio Code')
            speak('I was created by Sir, Anshul Raina. I was created with python language in Visual Studio Code')
        
        elif 'temperature' in query:
            speak("Sir, please tell me your location")
            location=takeCommand()
            search=f"temperature in {location}"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp=data.find("div",class_="BNeawe").text
            speak(f"current {search} is {temp}")

                    
        elif 'open google' in query or 'open chrome' in query: #error
            os.startfile('c:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
        
        elif 'open brave' in query:
            os.startfile('c:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe')
        
        elif 'open new window' in query:
            pyautogui.hotkey('ctrl', 'n')
            
        elif 'open incognito window' in query:
            pyautogui.hotkey('ctrl', 'shift', 'n')
        
        elif 'minimize' in query or 'minimize current window' in query or 'minimise' in query:
            pyautogui.hotkey('win', 'down')
            pyautogui.hotkey('win', 'down')
        
        elif 'maximize' in query    or 'maximize current window' in query or 'maximise' in query:
            pyautogui.hotkey('win', 'up')
            pyautogui.hotkey('win', 'up')
        
        elif 'vs code' in query:
            os.startfile('c:\\Users\\anshu\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')
        
        elif 'type' in query:
            query=query.replace('type','')
            pyautogui.typewrite(f'{query}',0.1)
        
        elif 'downloads' in query:
            pyautogui.hotkey('ctrl', 'j')
        
        elif 'history' in query:
            pyautogui.hotkey('ctrl', 'h')
        
        elif 'open new tab' in query:
            pyautogui.hotkey('ctrl', 't')
            
        elif 'enter' in query:
            pyautogui.hotkey('enter')
        
        elif 'close tab' in query:
            pyautogui.hotkey('ctrl', 'w')
        
        elif 'close window' in query:
            pyautogui.hotkey('alt', 'f4')
            
        elif 'reopen' in query and 'tab' in query:
            pyautogui.hotkey('ctrl', 'shift', 'tab')
        
        elif 'wikipedia' in query:
            speak("Searching....")
            query=query.replace('wikipedia','')
            result=wikipedia.summary(query,sentences=3)
            speak("According to Wikipedia, ")
            print(result)
            speak(result)

        elif 'youtube' in query:
            speak("Sir, What would you like to search")
            search_input=takeCommand().lower()
            if 'just open' in search_input:
                subprocess.Popen([bravepath, 'https://www.youtube.com/'])
                speak("opening youtube, sir")
            else:
                youtubeSearch(search_input)
                speak("here are the results, sir")
            
        elif 'search' in query or 'browse' in query:
            speak("Sir, What would you like to search")
            search_input=takeCommand().lower()
            googleSearch(search_input)
            speak("here are the results, sir")
        
        elif 'joke' in query:
            joke()
            
        elif 'go offline' in query:
            speak("Going offline Sir! ")
            quit()
            
        elif 'screenshot' in query:
            screenshot()
        
        elif 'close brave' in query:
            os.system('taskkill /im brave.exe /f')        
        
        elif 'close chrome' in query or 'close google' in query:
            os.system('taskkill /im chrome.exe /f')
            
        elif 'note' in query:
            speak("What should I write, Sir?")
            notes=takeCommand()
            file=open('notes.txt','w')
            speak("Sir should I include Date and Time?")
            ans=takeCommand()
            if 'yes' in ans or 'sure' in ans:
                strTime=datetime.datetime.now().strftime("%I:%M %p")
                file.write(strTime)
                file.write(":-")
                file.write(notes)
                speak("Done Taking Notes, SIR! ")
            else:
                file.write(notes)
        
        elif 'show note' in query:
            speak('showing notes')
            file=open('notes.txt','r')
            print(file.read())
            speak(file.read())
        # elif 'where is' in query:
        #     query=query.replace("where is","")
        #     location=query
        #     speak("User asked to locate"+location)
        #     wb.open_new_tab("https://www.google.com/maps/place/"+location)
        
        elif 'ip address' in query:
            try:
                # Get the IP address of the device
                ip_address = socket.gethostbyname(socket.gethostname())
                speak(f'Sir, the IP address of your device is {ip_address}')
                print(f'Sir, the IP address of your device is {ip_address}')
            except socket.gaierror:
                speak("Network is weak, please try again some time later")
                print("Network is weak, please try again some time later")
                
        elif 'hibernate' in query:
            speak('System hibernating, sir')
            os.system('rundll32.exe powrprof.dll, SetSuspendState 0,1,0')
        
        elif 'restart' in query:
            speak('System restarting, sir')
            os.system("shutdown /r /t 5")
        
        elif 'shutdown' in query:
            speak('System shutting down, sir')
            os.system("shutdown /s /t 5")
            
        elif 'calculate' in query:
            client=wolframalpha.Client(wolframalpha_app_id) # Creates a new wolfram alpha client object using the provided app ID
            index=query.lower().split().index('calculate') # Splits the query string into words, coverts it to lowercase, and finds the index of the word "calculate"
            query=query.split()[index+1:] # Extracts the substring of the query that comes after the word "calculate"
            res=client.query(' '.join(query)) # Sends the extracted query string to the Wolfram Alpha API and retrieves the results
            answer=next(res.results).text # Extracts the text of the first result from the retrieved results
            print("The answer is: "+answer)
            speak("The answer is ")
            speak(answer)
            
        elif 'what is' in query or 'explain' in query or 'define' in query or 'who is' in query:
            client=client=wolframalpha.Client(wolframalpha_app_id)
            res=client.query(query)
            
            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print("No Results")
                
        elif 'cpu' in query:
            cpu()
            
        elif 'remember that' in query:
            speak("What should I remember? ")
            memory=takeCommand()
            speak("You asked me to remember that "+memory)
            remember=open('memory.txt','w')
            remember.write(memory)
            remember.close()
        
        elif 'do you remember anything' in query:
            remember=open('memory.txt','r')
            speak("You asked me to remember that "+remember.read())
            
        elif 'news' in query:
            try:
                speak("Sir, would you like me to share news about apple, tesla, US, or technical? ")
                srcTitle=takeCommand().lower()
                if 'apple' in srcTitle: 
                    srcTitle='apple'
                    jsonObj=urlopen("https://newsapi.org/v2/everything?q=apple&from=2024-02-18&to=2024-02-18&sortBy=popularity&apiKey=bfa584b5be3c4b4bb32e00b8a964b55f")
                elif 'tesla' in srcTitle: 
                    srcTitle='tesla'
                    jsonObj=urlopen("https://newsapi.org/v2/everything?q=tesla&from=2024-01-19&sortBy=publishedAt&apiKey=bfa584b5be3c4b4bb32e00b8a964b55f")
                elif 'us' in srcTitle or 'united states' in srcTitle: 
                    srcTitle='us'
                    jsonObj=urlopen("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=bfa584b5be3c4b4bb32e00b8a964b55f")
                elif 'tech' in srcTitle: 
                    srcTitle='tech'
                    jsonObj=urlopen("https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=bfa584b5be3c4b4bb32e00b8a964b55f")

                data=json.load(jsonObj)
                i=1
                print(f"Here are some top headlines from the {srcTitle} industry")
                speak(f"Here are some top headlines from the {srcTitle} industry")
                print("========================TOP HEADLINES======================")
                for item in data['articles']:
                    print(str(i)+'. '+item['title']+'\n')
                    description = item.get('description') or ''  # get the 'description' value or an empty string if it's None
                    print(description+'\n')
                    title=item['title'].replace("TechCrunch","")
                    speak(title)
                    i+=1
            except Exception as e:
                print(str(e)) 
        
        elif 'undo' in query:
            pyautogui.hotkey('ctrl','z')

        elif 'camera' in query:
            pyautogui.hotkey('win')
            pyautogui.typewrite('camera')
            pyautogui.hotkey('enter')

        elif 'jarvis' in query:
            print('Yes sir! ')
            speak('yes sir! ')
            
            
