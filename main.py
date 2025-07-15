# eva.py — Enhanced Voice Assistant (EVA)

import logging
import os
import subprocess
import webbrowser
from datetime import datetime
import pyautogui
import pyttsx3
import spacy
import speech_recognition as sr
import wikipedia

# Configure logging
logging.basicConfig(
    filename="assistant.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize TTS engine
engine = pyttsx3.init('sapi5')
engine.setProperty("rate", 150)
engine.setProperty("volume", 0.9)

# Initialize global state
current_context = None
action_history = []
redo_stack = []

# Preferences
user_preferences = {
    'name': 'User',
    'speech_rate': 150,
    'preferred_language': 'en',
    'spaCy_model': 'en_core_web_sm'
}

# Load NLP model
nlp = spacy.load(user_preferences['spaCy_model'])

def speak(text):
    try:
        engine.say(text)
        print(f"EVA: {text}")
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            return None
    try:
        return recognizer.recognize_google(audio, language='en').lower()
    except (sr.UnknownValueError, sr.RequestError):
        return None

def process_command(command):
    command = command.lower()
    intent_keywords = {
        "open browser": "open_browser",
        "open notepad": "open_notepad",
        "open file explorer": "open_file_explorer",
        "search wikipedia": "search_wikipedia",
        "open calculator": "open_calculator",
        "time": "time",
        "screenshot": "screenshot",
        "shutdown": "shutdown",
        "restart": "restart",
        "create a file": "create_a_file",
        "move mouse": "move_mouse",
        "click": "click",
        "scroll": "scroll",
        "type": "type",
        "exit": "exit_program",
        "open application": "open_application",
        "close application": "close_application",
        "open website": "open_website",
        "list files": "list_files",
        "copy file": "copy_file",
        "move file": "move_file",
        "rename file": "rename_file",
        "create folder": "create_folder",
        "delete folder": "delete_folder",
        "lock computer": "lock_computer",
        "open settings": "open_settings"
    }
    for keyword, intent in intent_keywords.items():
        if keyword in command:
            return [intent]
    return []

def execute_command(command):
    global current_context
    intents = process_command(command)

    for intent in intents:
        if intent == "open_browser":
            speak(f"Opening browser, {user_preferences['name']}")
            subprocess.run(["start", "chrome"], shell=True)
            current_context = "browser"

        elif intent == "open_notepad":
            os.system("notepad")
            speak("Opening Notepad.")
            current_context = "notepad"

        elif intent == "open_calculator":
            os.system("calc")
            speak("Opening Calculator.")
            current_context = "calculator"

        elif intent == "time":
            now = datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {now}")

        elif intent == "screenshot":
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            pyautogui.screenshot(filename)
            speak(f"Screenshot saved as {filename}")

        elif intent == "search_wikipedia":
            speak("What should I search on Wikipedia?")
            query = listen()
            if query:
                try:
                    summary = wikipedia.summary(query, sentences=2)
                    speak(summary)
                except:
                    speak("No Wikipedia result found.")

        elif intent == "search":
            speak("What do you want to search online?")
            query = listen()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                speak(f"Searching for {query}")

        elif intent == "shutdown":
            speak("Are you sure you want to shut down?")
            if "yes" in listen():
                subprocess.run(['shutdown', '/s', '/t', '0'], shell=True)

        elif intent == "restart":
            speak("Are you sure you want to restart?")
            if "yes" in listen():
                subprocess.run(['shutdown', '/r', '/t', '0'], shell=True)

        elif intent == "lock_computer":
            speak("Locking your computer.")
            subprocess.run("rundll32.exe user32.dll,LockWorkStation")

        elif intent == "open_settings":
            subprocess.run("start ms-settings:", shell=True)

        elif intent == "create_a_file":
            speak("What is the name of the file?")
            filename = listen()
            if filename:
                with open(f"{filename}.txt", "w") as f:
                    f.write("This is a new file created by EVA.")
                speak(f"{filename}.txt created.")

        elif intent == "move_mouse":
            speak("Where should I move the mouse? (say x and y)")
            pos = listen()
            try:
                x, y = map(int, pos.split())
                pyautogui.moveTo(x, y)
                speak(f"Moved mouse to ({x}, {y})")
            except:
                speak("Invalid coordinates.")

        elif intent == "click":
            pyautogui.click()
            speak("Clicked.")

        elif intent == "type":
            speak("What should I type?")
            to_type = listen()
            if to_type:
                pyautogui.write(to_type)
                speak("Typed.")

        elif intent == "exit_program":
            speak("Goodbye!")
            exit()

        else:
            speak("Sorry, I didn't understand the command.")

def set_preferences():
    speak("What is your name?")
    name = listen()
    if name:
        user_preferences["name"] = name

def main():
    set_preferences()
    speak(f"Hello {user_preferences['name']}, I am EVA. How can I help you today?")
    while True:
        command = listen()
        if command:
            execute_command(command)

if __name__ == "__main__":
    main()
