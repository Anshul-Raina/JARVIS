# from logging import root

# import dateutil.parser
# from skimage.metrics import structural_similarity as ssim
# from bs4 import BeautifulSoup
# from charset_normalizer import from_path
# import cv2
# import numpy as np
# import os
# import tkinter as tk
# from tkinter import messagebox
# from PIL import Image, ImageTk
# import socket
# import sys
# import time
# import pyttsx3
# import datetime
# import speech_recognition as sr
# import pyaudio
# import wikipedia
# import pyjokes
# import psutil
# import pyautogui
# import os
# import wolframalpha
# import smtplib
# import webbrowser as wb
# import json
# import requests
# from urllib.request import urlopen
# import subprocess
# import pygame

# engine = pyttsx3.init()
# wolframalpha_app_id='LQP4EK-UU2GLWH4GH'
# chromepath="c:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s"
# bravepath='C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'



    

# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()

# # here is the function to get the current time
# def time_():
#     time=datetime.datetime.now().strftime("%I:%M %p") # for 12 hour clock
#     speak("The current time is ")
#     speak(time)

# # here is the function to get the current date
# def date_():
#     year=datetime.datetime.now().year
#     month=datetime.datetime.now().month
#     date=datetime.datetime.now().day
#     speak("The current date is ")
#     speak(date)
#     speak(month)
#     speak(year)

# # this function is used when the user activates JARVIS
# def wishme():
    


#     # greetings
#     hour=datetime.datetime.now().hour
    
#     if hour>=6 and hour<12:
#         speak("Good Morning Sir! ")
#     elif hour>=12 and hour< 18:
#         speak("Good Afternoon Sir! ")
#     elif hour>=18 and hour<24:
#         speak("Good Evening Sir! ")
#     else:
#         speak("Good Night Sir! ")

#     speak("Welcome back! ")
#     speak("Jarvis at your service. Please tell me how can I help you today? ")

# def get_my_location():
#     try:
#         # Using ipapi.co - a free IP geolocation API
#         response = requests.get('https://ipapi.co/json/')
#         if response.status_code == 200:
#             data = response.json()
#             # Get city and country
#             location = f"{data['city']}, {data['region']}"
#             return location
#     except Exception as e:
#         speak("Couldn't detect your location automatically. Please try again later.")
#         return None
    
# def takeCommand():
#     r=sr.Recognizer() # create a recognizer object
#     with sr.Microphone() as source: # initialize microphone as the source of input
#         print("Listening.... ")
#         r.pause_threshold=1 # amount of time to wait for audio input before timinng out is 1 sec
#         audio=r.listen(source) # records audio from the microphone

#     try:
#         print("Recognizing...")
#         query=r.recognize_google(audio,language='en-US') # uses google api to convert speech to text
#         print(query)
    
#     except Exception as e:
#         print(e)
#         print("Say that again please...")
#         return "None"
#     return query

# def joke():
#     result=pyjokes.get_joke()
#     part = result.split('<', 1)[0]
#     print(part)
#     speak(result)
    
# def screenshot():
#     img=pyautogui.screenshot()
#     speak('Name of screenshot Sir? ')
#     name=takeCommand().lower()
#     img.save(f'C:/Desktop/{name}.png')
#     speak("I have taken the screenshot Sir")

# def sendEmail(to,content):
#     server=smtplib.SMTP('smtp.gmail.com',587)
#     server.ehlo()
#     server.starttls()
#     server.login('anshulraina.2021@vitstudent.ac.in','Forgot_password00')
#     server.sendmail('anshulraina.2021@vitstudent.ac.in',to,content)
#     server.close()

# def cpu():
#     usage=str(psutil.cpu_percent())
#     speak('CPU is at '+usage)
#     print('CPU is at '+usage)
#     battery=psutil.sensors_battery()
#     speak('Battery is at')
#     speak(battery.percent)
#     print(f'Battery is at {battery.percent}')

# def googleSearch(query):
#     url=f"https://search.brave.com/search?q={query}"
#     wb.get(from_path).open(url)
    
# def youtubeSearch(query):
#     url=f"https://www.youtube.com/results?search_query={query}"
#     wb.get(chromepath).open(url)    
    
# def check_system_status():
#     cpu_usage = psutil.cpu_percent()
#     memory = psutil.virtual_memory()
#     battery = psutil.sensors_battery()
    
#     status_msg = f"""
#     System Status:
#     CPU Usage: {cpu_usage}%
#     Memory Usage: {memory.percent}%
#     Battery: {battery.percent}% {'Plugged In' if battery.power_plugged else 'On Battery'}
#     """
#     speak(f"Current system status: CPU at {cpu_usage}%, Memory at {memory.percent}%, Battery at {battery.percent}%")
#     print(status_msg)
    
# def check_disk_space():
#     disk = psutil.disk_usage('/')
#     total = round(disk.total / (2**30), 2)  # Convert to GB
#     used = round(disk.used / (2**30), 2)
#     free = round(disk.free / (2**30), 2)
    
#     speak(f"You have {free} gigabytes free out of {total} gigabytes total space")
#     print(f"Disk Space: {used}GB used, {free}GB free, {total}GB total")

# def check_network():
#     try:
#         response = requests.get("http://www.google.com", timeout=5)
#         speed = response.elapsed.total_seconds()
#         speak(f"Internet is connected. Response time is {round(speed, 2)} seconds")
#         print(f"Network Status: Connected (Response Time: {speed}s)")
#     except requests.RequestException:
#         speak("Internet connection appears to be down")
#         print("Network Status: Disconnected")
        

# # Weather & Location
# def get_weather_forecast(days=3):
#     # Note: Replace with your own API key
#     API_KEY = "888b63ca5cd74c5ba1e4c8b880e84b3e"
    
#     speak("Please tell me the city name")
#     city = takeCommand()
    
#     base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    
#     try:
#         response = requests.get(base_url)
#         data = response.json()
        
#         if response.status_code == 200:
#             # Get forecast for specified number of days
#             for i in range(days):
#                 daily_data = data['list'][i*8]  # Data points are in 3-hour intervals
#                 date = datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A')
#                 temp = daily_data['main']['temp']
#                 description = daily_data['weather'][0]['description']
                
#                 forecast = f"{date}: {temp}°C, {description}"
#                 speak(forecast)
#                 print(forecast)
#         else:
#             speak("Sorry, I couldn't get the weather forecast")
#     except Exception as e:
#         speak("Error fetching weather data")
#         print(f"Error: {str(e)}")

# def get_directions():
#     # Get current location using IP
#     source = get_my_location()
#     if source is None:
#         speak("There was an error detecting your location.")
#         return
        
#     speak("Where would you like directions to?")
#     destination = takeCommand()
    
#     if destination is None:
#         speak("I'm sorry, I couldn't understand the destination. Please try again.")
#         return
    
#     try:
#         maps_url = f"https://www.google.com/maps/dir/{source.replace(' ', '+')}/{destination.replace(' ', '+')}"
#         wb.open(maps_url)
#         speak(f"Opening directions from {source} to {destination}")
#     except Exception as e:
#         speak("Sorry, there was an error getting directions. Please try again.")
        
# # Browser Controls
# def manage_tabs(action):
#     if action == "switch":
#         pyautogui.hotkey('ctrl', 'tab')
#     elif action == "refresh_all":
#         pyautogui.hotkey('ctrl', 'shift', 'r')
#     elif action == "bookmark":
#         pyautogui.hotkey('ctrl', 'd')
#     elif action == "show_bookmarks":
#         pyautogui.hotkey('ctrl', 'shift', 'o')

# # Media Control
# def control_volume(action):
#     if action == "up":
#         pyautogui.press('volumeup')
#     elif action == "down":
#         pyautogui.press('volumedown')
#     elif action == "mute":
#         pyautogui.press('volumemute')

# # Productivity
# class Reminder:
#     def __init__(self):
#         self.reminders = []

#     def add_reminder(self, text, time):
#         self.reminders.append({"text": text, "time": time})
#         speak(f"Reminder set for {time}: {text}")

#     def check_reminders(self):
#         current_time = datetime.datetime.now()
#         active_reminders = [r for r in self.reminders if r["time"] > current_time]
#         if active_reminders:
#             speak("Here are your active reminders:")
#             for r in active_reminders:
#                 speak(f"At {r['time'].strftime('%I:%M %p')}: {r['text']}")
#         else:
#             speak("You have no active reminders")


# def send_quick_email():
#     speak("Who would you like to send the email to?")
#     recipient = takeCommand()
#     speak("What should the message say?")
#     message = takeCommand()
    
#     # Note: Implement proper email sending logic here
#     print(f"Would send email to {recipient}: {message}")
#     speak("Email draft created")

# # Security
# def lock_computer():
#     if os.name == 'nt':  # Windows
#         os.system('rundll32.exe user32.dll,LockWorkStation')
#     speak("Computer locked")

# def security_check():
#     # Basic security checks
#     firewall = subprocess.run(['netsh', 'advfirewall', 'show', 'currentprofile'], 
#                             capture_output=True, text=True)
#     updates = subprocess.run(['systeminfo'], capture_output=True, text=True)
    
#     speak("Running basic security check")
#     print("Security Status:")
#     print(firewall.stdout)
#     print("System Information:")
#     print(updates.stdout)

# # Voice Assistant Settings
# def adjust_speech_rate(rate):
#     current_rate = engine.getProperty('rate')
#     if rate == "faster":
#         engine.setProperty('rate', current_rate + 50)
#     elif rate == "slower":
#         engine.setProperty('rate', current_rate - 50)
#     speak("Speech rate adjusted")

# def set_quiet_mode(enable=True):
#     if enable:
#         engine.setProperty('volume', 0.5)
#         speak("Quiet mode enabled")
#     else:
#         engine.setProperty('volume', 1.0)
#         speak("Quiet mode disabled")
       
# class TaskTimer:
#     def __init__(self):
#         self.timers = {}
    
#     def start_timer(self, task_name, duration_minutes):
#         end_time = datetime.datetime.now() + datetime.timedelta(minutes=duration_minutes)
#         self.timers[task_name] = end_time
#         speak(f"Timer set for {task_name} for {duration_minutes} minutes")
    
#     def check_timers(self):
#         current_time = datetime.datetime.now()
#         completed_tasks = []
        
#         for task, end_time in self.timers.items():
#             if current_time >= end_time:
#                 speak(f"Timer complete for {task}")
#                 completed_tasks.append(task)
        
#         for task in completed_tasks:
#             del self.timers[task] 
            
#     # System Maintenance
# def system_maintenance():
#     """Perform system maintenance tasks"""
#     speak("Starting system maintenance")
    
#     # Check disk health
#     if os.name == 'nt':  # Windows
#         subprocess.run(['chkdsk', 'C:'], capture_output=True)
    
#     # Clear temporary files
#     temp_folders = [
#         os.path.join(os.environ.get('TEMP')),
#         os.path.join(os.environ.get('TMP'))
#     ]
    
#     files_removed = 0
#     for folder in temp_folders:
#         try:
#             for item in os.listdir(folder):
#                 item_path = os.path.join(folder, item)
#                 try:
#                     if os.path.isfile(item_path):
#                         os.unlink(item_path)
#                     elif os.path.isdir(item_path):
#                         os.rmdir(item_path)
#                     files_removed += 1
#                 except Exception:
#                     continue
#         except Exception:
#             continue
    
#     speak(f"Maintenance complete. Removed {files_removed} temporary files")
    
# if __name__=="__main__":
#     reminder_system = Reminder()
#     wishme()
#     while True:
#         query=takeCommand().lower() # take audio prompt as input and convert to lower case for improving the accuracy  
        
#         if 'time' in query:
#             time_()
        
#         if 'date' in query:
#             date_() 
        
#         elif 'who are you' in query or 'what is your name' in query:
#             print('My name is Jarvis')
#             speak('My name is Jarvis')
#             print('I can do everything my creator programmed me to do')
#             speak('I can do everything my creator programmed me to do')
        
#         elif 'who created you' in query or 'who made you' in query:
#             print('I was created by Sir, Anshul Raina. I was created with python language in Visual Studio Code')
#             speak('I was created by Sir, Anshul Raina. I was created with python language in Visual Studio Code')
        
#         elif 'temperature' in query:
#             speak("Sir, please tell me your location")
#             location=takeCommand()
#             temp=f"temperature in {location}"
#             min_temp=f"minimum temperature in {location}"
#             max_temp=f"maximum temperature in {location}"
#             url = f"https://www.google.com/search?q={temp}"
#             r = requests.get(url)
#             data = BeautifulSoup(r.text, "html.parser")
#             temp=data.find("div",class_="BNeawe").text
#             speak(f"current temperature in {location} is {temp}")
        
       

#         elif 'weather' in query:
#             speak("Sir, please tell me your location")
#             location = takeCommand()
            
#             # Use your own OpenWeatherMap API key
#             api_key = "888b63ca5cd74c5ba1e4c8b880e84b3e"  # Replace with your actual API key
#             base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            
#             # Fetch weather data from the API
#             response = requests.get(base_url)
#             data = response.json()
            
#             if data["cod"] != "404":  # Check if the city is found
#                 main = data["main"]
#                 weather_description = data["weather"][0]["description"]
#                 temp = main["temp"]
#                 humidity = main["humidity"]
#                 wind_speed = data["wind"]["speed"]

#                 # Speak out the weather details
#                 speak(f"Current weather in {location} is {weather_description}. The temperature is {temp} degrees Celsius. Humidity is {humidity}%. Wind speed is {wind_speed} meters per second.")
#             else:
#                 speak("Sorry, I couldn't find the weather information for that location.")


                    
#         elif 'open google' in query or 'open chrome' in query: #error
#             os.startfile('c:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
        
#         elif 'open brave' in query:
#             os.startfile('c:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe')
        
#         elif 'open new window' in query:
#             pyautogui.hotkey('ctrl', 'n')
            
#         elif 'open incognito window' in query:
#             pyautogui.hotkey('ctrl', 'shift', 'n')
        
#         elif 'minimize' in query or 'minimize current window' in query or 'minimise' in query:
#             pyautogui.hotkey('win', 'down')
#             pyautogui.hotkey('win', 'down')
        
#         elif 'maximize' in query    or 'maximize current window' in query or 'maximise' in query:
#             pyautogui.hotkey('win', 'up')
#             pyautogui.hotkey('win', 'up')
        
#         elif 'vs code' in query:
#             os.startfile('c:\\Users\\anshu\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')
        
#         elif 'type' in query:
#             query=query.replace('type','')
#             pyautogui.typewrite(f'{query}',0.1)
        
#         elif 'downloads' in query:
#             pyautogui.hotkey('ctrl', 'j')
        
#         elif 'history' in query:
#             pyautogui.hotkey('ctrl', 'h')
        
#         elif 'open new tab' in query:
#             pyautogui.hotkey('ctrl', 't')
            
#         elif 'enter' in query:
#             pyautogui.hotkey('enter')
        
#         elif 'close tab' in query:
#             pyautogui.hotkey('ctrl', 'w')
        
#         elif 'close window' in query:
#             pyautogui.hotkey('alt', 'f4')
            
#         elif 'reopen' in query and 'tab' in query:
#             pyautogui.hotkey('ctrl', 'shift', 'tab')
        
#         elif 'wikipedia' in query:
#             speak("Searching....")
#             query=query.replace('wikipedia','')
#             result=wikipedia.summary(query,sentences=3)
#             speak("According to Wikipedia, ")
#             print(result)
#             speak(result)

#         elif 'youtube' in query:
#             speak("Sir, What would you like to search")
#             search_input=takeCommand().lower()
#             if 'just open' in search_input:
#                 subprocess.Popen([bravepath, 'https://www.youtube.com/'])
#                 speak("opening youtube, sir")
#             else:
#                 youtubeSearch(search_input)
#                 speak("here are the results, sir")
            
#         elif 'search' in query or 'browse' in query:
#             speak("Sir, What would you like to search")
#             search_input=takeCommand().lower()
#             googleSearch(search_input)
#             speak("here are the results, sir")
        
#         elif 'joke' in query:
#             joke()
            
#         elif 'go offline' in query:
#             speak("Going offline Sir! ")
#             quit()
            
#         elif 'screenshot' in query:
#             screenshot()
        
#         elif 'close brave' in query:
#             os.system('taskkill /im brave.exe /f')        
        
#         elif 'close chrome' in query or 'close google' in query:
#             os.system('taskkill /im chrome.exe /f')
            
#         elif 'note' in query:
#             speak("What should I write, Sir?")
#             notes=takeCommand()
#             file=open('notes.txt','w')
#             speak("Sir should I include Date and Time?")
#             ans=takeCommand()
#             if 'yes' in ans or 'sure' in ans:
#                 strTime=datetime.datetime.now().strftime("%I:%M %p")
#                 file.write(strTime)
#                 file.write(":-")
#                 file.write(notes)
#                 speak("Done Taking Notes, SIR! ")
#             else:
#                 file.write(notes)
        
#         elif 'show note' in query:
#             speak('showing notes')
#             file=open('notes.txt','r')
#             print(file.read())
#             speak(file.read())
#         # elif 'where is' in query:
#         #     query=query.replace("where is","")
#         #     location=query
#         #     speak("User asked to locate"+location)
#         #     wb.open_new_tab("https://www.google.com/maps/place/"+location)
        
#         elif 'ip address' in query:
#             try:
#                 # Get the IP address of the device
#                 ip_address = socket.gethostbyname(socket.gethostname())
#                 speak(f'Sir, the IP address of your device is {ip_address}')
#                 print(f'Sir, the IP address of your device is {ip_address}')
#             except socket.gaierror:
#                 speak("Network is weak, please try again some time later")
#                 print("Network is weak, please try again some time later")
                
#         elif 'hibernate' in query:
#             speak('System hibernating, sir')
#             os.system('rundll32.exe powrprof.dll, SetSuspendState 0,1,0')
        
#         elif 'restart' in query:
#             speak('System restarting, sir')
#             os.system("shutdown /r /t 5")
        
#         elif 'shutdown' in query:
#             speak('System shutting down, sir')
#             os.system("shutdown /s /t 5")
            
#         elif 'calculate' in query:
#             client=wolframalpha.Client(wolframalpha_app_id) # Creates a new wolfram alpha client object using the provided app ID
#             index=query.lower().split().index('calculate') # Splits the query string into words, coverts it to lowercase, and finds the index of the word "calculate"
#             query=query.split()[index+1:] # Extracts the substring of the query that comes after the word "calculate"
#             res=client.query(' '.join(query)) # Sends the extracted query string to the Wolfram Alpha API and retrieves the results
#             answer=next(res.results).text # Extracts the text of the first result from the retrieved results
#             print("The answer is: "+answer)
#             speak("The answer is ")
#             speak(answer)
            
#         elif 'what is' in query or 'explain' in query or 'define' in query or 'who is' in query:
#             client=client=wolframalpha.Client(wolframalpha_app_id)
#             res=client.query(query)
            
#             try:
#                 print(next(res.results).text)
#                 speak(next(res.results).text)
#             except StopIteration:
#                 print("No Results")
                
#         elif 'cpu' in query:
#             cpu()
            
#         elif 'remember that' in query:
#             speak("What should I remember? ")
#             memory=takeCommand()
#             speak("You asked me to remember that "+memory)
#             remember=open('memory.txt','w')
#             remember.write(memory)
#             remember.close()
        
#         elif 'do you remember anything' in query:
#             remember=open('memory.txt','r')
#             speak("You asked me to remember that "+remember.read())
            
#         elif 'news' in query:
#             try:
#                 speak("Sir, would you like me to share news about apple, tesla, US, or technical? ")
#                 srcTitle=takeCommand().lower()
#                 if 'apple' in srcTitle: 
#                     srcTitle='apple'
#                     jsonObj=urlopen("https://newsapi.org/v2/everything?q=apple&from=2024-02-18&to=2024-02-18&sortBy=popularity&apiKey=bfa584b5be3c4b4bb32e00b8a964b55f")
#                 elif 'tesla' in srcTitle: 
#                     srcTitle='tesla'
#                     jsonObj=urlopen("https://newsapi.org/v2/everything?q=tesla&from=2024-01-19&sortBy=publishedAt&apiKey=bfa584b5be3c4b4bb32e00b8a964b55f")
#                 elif 'us' in srcTitle or 'united states' in srcTitle: 
#                     srcTitle='us'
#                     jsonObj=urlopen("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=bfa584b5be3c4b4bb32e00b8a964b55f")
#                 elif 'tech' in srcTitle: 
#                     srcTitle='tech'
#                     jsonObj=urlopen("https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=bfa584b5be3c4b4bb32e00b8a964b55f")

#                 data=json.load(jsonObj)
#                 i=1
#                 print(f"Here are some top headlines from the {srcTitle} industry")
#                 speak(f"Here are some top headlines from the {srcTitle} industry")
#                 print("========================TOP HEADLINES======================")
#                 for item in data['articles']:
#                     print(str(i)+'. '+item['title']+'\n')
#                     description = item.get('description') or ''  # get the 'description' value or an empty string if it's None
#                     print(description+'\n')
#                     title=item['title'].replace("TechCrunch","")
#                     speak(title)
#                     i+=1
#             except Exception as e:
#                 print(str(e)) 
                
#         elif "system status" in query:
#             check_system_status()
#         elif "disk space" in query:
#             check_disk_space()
#         elif "network status" in query or "check internet" in query:
#             check_network()
            
#         # Weather & Location
#         elif "weather forecast" in query:
#             get_weather_forecast()
#         elif "directions to" in query:
#             get_directions()
            
#         # Browser Controls
#         elif "switch tab" in query:
#             manage_tabs("switch")
#         elif "refresh all" in query:
#             manage_tabs("refresh_all")
#         elif "bookmark page" in query:
#             manage_tabs("bookmark")
#         elif "show bookmarks" in query:
#             manage_tabs("show_bookmarks")
            
#         # Media Control
#         elif "volume up" in query:
#             control_volume("up")
#         elif "volume down" in query:
#             control_volume("down")
#         elif "mute" in query:
#             control_volume("mute")
#         # Productivity
#         elif "add reminder" in query:
#             speak("What should I remind you about?")
#             text = takeCommand()
#             speak("When should I remind you? Please say the time.")
#             time_str = takeCommand()

#             try:
#                 reminder_time = dateutil.parser.parse(time_str)
#                 reminder_system.add_reminder(text, reminder_time)
#             except ValueError:
#                 speak("Sorry, I couldn't understand the time format. Please try saying the time in a format like '10 AM', '3 PM', or '5:30 PM'.")
                
#         elif "check schedule" in query:
#             reminder_system.check_reminders()
        
#         # Communication
#         elif "quick email" in query:
#             send_quick_email()
            
#         # Security
#         elif "lock computer" in query:
#             lock_computer()
            
#         elif "security check" in query:
#             security_check()
            
#         # Voice Assistant Settings
#         elif "speak faster" in query:
#             adjust_speech_rate("faster")
            
#         elif "speak slower" in query:
#             adjust_speech_rate("slower")
            
#         elif "quiet mode" in query:
#             set_quiet_mode(True)
        
#         elif 'timer' in query:
#             timer = TaskTimer()
#             speak("What task should I set a timer for?")
#             task = takeCommand()
#             speak("How many minutes?")
#             try:
#                 minutes = int(takeCommand())
#                 timer.start_timer(task, minutes)
#             except ValueError:
#                 speak("Invalid duration specified")
        
#         elif 'maintenance' in query:
#             system_maintenance()
        
#         elif 'undo' in query:
#             pyautogui.hotkey('ctrl','z')

#         elif 'camera' in query:
#             pyautogui.hotkey('win')
#             pyautogui.typewrite('camera')
#             pyautogui.hotkey('enter')

#         elif 'jarvis' in query:
#             print('Yes sir! ')
#             speak('yes sir! ')
                
                
