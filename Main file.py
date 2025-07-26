# Enhanced Jarvis Voice Assistant
# This code is a voice-activated AI chatbot that can perform various tasks like playing 
# music, searching the web, managing tasks, and more.
# It uses libraries like pyttsx3 for text-to-speech, speech_recognition for voice commands,
#  and webbrowser for opening websites.

# Import necessary libraries
# Ensure you have the required libraries installed:
# pip install pyttsx3 speech_recognition plyer pyautogui wikipedia pywhatkit openai
# Also, ensure you have the OpenAI API key set up in user_config

import pyttsx3              
import speech_recognition as sr
import os
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import openai
import openai_request as ai
import ctypes
import subprocess
import os
#from dotenv import load_dotenv

# load_dotenv()  # 🔄 Load variables from .env file

# openai_api_key = os.getenv("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")


# Initialize the text-to-speech engine
# For Windows systems, use 'sapi5' driver
# For other systems, you might need to adjust the driver accordingly

engine = pyttsx3.init(driverName='sapi5')  # For Windows systems
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 130)

# Function to speak the given audio
# It prints the audio to console and uses the text-to-speech engine to speak it

def speak(audio):
    print("Jarvis: " + audio)
    engine.say(audio)
    engine.runAndWait()

# Function to listen for voice commands
# It uses the microphone to capture audio and recognizes it using Google's speech recognition
# Returns the recognized command as a string

def command():
    content = " "
    while content.strip() == "":
        r = sr.Recognizer()         
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            content = r.recognize_google(audio, language='en-in')
            content = content.lower()
            print("You Said....." + content)
        except Exception as e:
            print("Please try again.....")
            speak("Sorry, please say that again.")
            content = " "
    return content

# Function to wish the user based on the current time
# It greets the user with "Good Morning", "Good Afternoon", or "Good Evening"
# and introduces itself as Jarvis, the voice assistant

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis, your voice assistant. How may I help you?")

# Main process function that handles the voice commands
# It listens for commands and performs actions based on the recognized commands

def main_process():
    wishMe()
    while True:
        request = command().lower()

        if "jarvis" in request:
            speak("Yes, I am listening")        # Responds when the user calls Jarvis

# Commands to handle various tasks
# If the command contains "play music", it plays a song from the user's music folder

        elif "play music" in request:         
            speak("Playing music")
            music_path = os.path.join(os.environ["USERPROFILE"], "Music") # Path to the user's music folder
            try:
                songs = os.listdir(music_path)
                if songs:
                    os.startfile(os.path.join(music_path, songs[0]))
                else:
                    speak("No music files found in Music folder.")
            except:
                speak("Error opening music folder.")

        # If the command contains "say time", it speaks the current time
        # It formats the time in HH:MM:SS format
        # If the command contains "new task", it adds a new task to a todo list
        # The task is extracted from the command and saved to a file named "todo.txt"

        elif "say time" in request or "what is the time" in request:
            now_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {now_time}")


# If the command contains "new task", it adds a new task to a todo list
        # The task is extracted from the command and saved to a file named "todo.txt"
        elif "new task" in request:
            task = request.replace("new task", "").strip()
            if task:
                speak("Adding task: " + task)
                with open("todo.txt", "a") as file:
                    file.write(task + "\n")

# If the command contains "show task", it reads the tasks from "todo.txt"
        # It reads the tasks from the file and displays them to the user
        # It also sends a notification with the tasks

        elif "show task" in request:
            speak("Here are your tasks")
            try:
                with open("todo.txt", "r") as file:
                    tasks = file.read()
                    print("Tasks:\n", tasks)
                notification.notify(title="Your Tasks", message=tasks)
            except:
                speak("No tasks found.")

# If the command contains "open youtube", it opens YouTube in the default web browser
        # If the command contains "open google", it opens Google in the default web browser
        # If the command contains "open <app_name>", it opens the specified application
        # It uses pyautogui to simulate keyboard input to open the application
        elif "open youtube" in request:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif "open google" in request:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        # If the command contains "open <app_name>", it opens the specified application
        # It uses pyautogui to simulate pressing the super key (Windows key) and typing the application name
        # It then simulates pressing the enter key to open the application
        # If the command contains "wikipedia <search_term>", it searches Wikipedia for the specified term
        # It uses the wikipedia library to get a summary of the search term and speaks it
        # If the command contains "search google <query>", it searches Google for the specified query
        # It uses webbrowser to open the Google search page with the query
        # If the command contains "screenshot", it takes a screenshot and saves it as "screenshot.png"
        # It uses pyautogui to take the screenshot and save it

        elif "open" in request:
            app = request.replace("open", "").strip()
            pyautogui.press("super")
            pyautogui.typewrite(app)
            pyautogui.sleep(1)
            pyautogui.press("enter")

        elif "wikipedia" in request:
            speak("Searching Wikipedia...")
            query = request.replace("search wikipedia", "").strip()
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except:
                speak("Could not find results on Wikipedia")

        elif "search google" in request:
            query = request.replace("search google", "").strip()
            webbrowser.open("https://www.google.com/search?q=" + query)
            speak("Searching Google for " + query)

        elif "screenshot" in request:
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            speak("Screenshot saved.")

# If the command contains "ask ai <question>", it sends the question to an AI service
        # It uses the ai module to send the request and get a response
        # It prints the request and response to the console and speaks the response
        # If the command contains "shutdown", it shuts down the system
        # It uses os.system to execute the shutdown command
        # If the command contains "restart", it restarts the system
        # It uses os.system to execute the restart command
        # If the command contains "lock screen", it locks the system using ctypes
        # It uses ctypes to call the LockWorkStation function
        # If the command contains "write a note", it prompts the user for a note and
        # saves it to a file named "note.txt"
        # It uses the command function to get the note from the user
        # If the command contains "read note", it reads the note from "note.txt"
        # It reads the note from the file and speaks it
        # If the command contains "exit" or "quit", it exits the program
        # It speaks a goodbye message and breaks the loop to exit
        # If the command is not recognized, it speaks an error message
        # It speaks an error message indicating that the command was not understood
        # It prompts the user to try again
        # It uses the ai module to send the request and get a response
        # It prints the request and response to the console and speaks the response
        # If the command contains "shutdown", it shuts down the system
        # It uses os.system to execute the shutdown command
        # If the command contains "restart", it restarts the system
        # It uses os.system to execute the restart command  

        # elif "ask ai" in request:
        #     question = request.replace("ask ai", "").strip()
        #     print("Request to AI:", question)
        #     response = ai.send_request(question)
        #     print("AI Response:", response)
        #     speak(response)

        elif "shutdown" in request:
            speak("Shutting down the system.")
            os.system("shutdown /s /t 1")

        elif "restart" in request:
            speak("Restarting the system.")
            os.system("shutdown /r /t 1")

        elif "lock screen" in request:
            speak("Locking the system.")
            ctypes.windll.user32.LockWorkStation()

        elif "write a note" in request:
            speak("What should I write?")
            note = command()
            with open("note.txt", "w") as f:
                f.write(note)
            speak("Note saved.")

        elif "read note" in request:
            try:
                with open("note.txt", "r") as f:
                    note = f.read()
                    speak("Here is your note.")
                    speak(note)
            except:
                speak("No note found.")

        elif "exit" in request or "quit" in request:
            speak("Goodbye!")
            break
        else:
            speak("I didn't understand that. Please try again.")
            
if __name__ == "__main__":
    try:
        main_process()
    finally:
        engine.stop()  # Cleanup pyttsx3 engine to prevent exit error


## List of commands that the user can give to Jarvis:
# exit/quit
#jarvis
#play music
#say time
#new task
#show task
#open youtube
#open google
#open <app_name>
#wikipedia <search_term>
#search google <query>
#screenshot
#ask ai <question>
#shutdown
#restart
#lock screen
#write a note
#read note
#exit
#quit
