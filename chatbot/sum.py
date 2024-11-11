# Mega-Project: Creating a desktop voice assistant (Friday)

import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import google.generativeai as genai
import os
from gpt4all import GPT4All
import socket


#Testing the cnnection
def is_connected_to_internet():
    try:
        # Try to connect to a well-known DNS server (Google's DNS)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except (socket.timeout, socket.gaierror):
        return False
    


# Define the model path and type
model_path = "D:/Github/AI_chatbot_LLAMA-2.0/chatbot/model/"
model_type = "llama"

# Load the GPT4All model
print("Loading the model, please wait...")
try:
    # Here we pass a dummy model name ('local_model') since GPT4All expects it
    model = GPT4All(model_name="Llama-3.2-1B-Instruct-Q4_K_M", model_path=model_path, model_type=model_type, allow_download=False)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load the model: {e}")
    exit(1)

#Locally generating resonse
def chatbot_response(prompt):
    try:
        # Increase the max_tokens to prevent incomplete answers
        response = model.generate(
            prompt, 
            max_tokens=150,   # Increased tokens to allow for a complete response
            temp=0.5,         # Set temperature to moderate to keep a good balance between randomness and coherence
            top_p=0.9,        # Set top_p to a moderate value for diversity
        )
        print(response.strip())
        speak(response.strip())
        return response.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"



recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 165)

def speak(text): # Function to transcribe speech to text
    engine.say(text)
    engine.runAndWait()

def processCommand(c): # Function to process different commands given by the user

    # Command to search a query in google (Google Search):

    if "search in google for" in c.lower(): # Say - "search" to search something in google.com
        l = c.lower().split(" ")[4: ]
        query_google = " ".join(l)
        speak(f"Searching in google for {query_google}")
        webbrowser.open(f"https://www.google.com/search?q={query_google}")

    # Creating Command to search a query in youtube (YouTube Search):

    elif "search in youtube for" in c.lower(): # Say - "YouTube Search" to search something in google.com
        l = c.lower().split(" ")[4: ]
        query_yt = " ".join(l)
        speak(f"Searching in YouTube for {query_yt}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query_yt}")
    
    # Creating Commands for Opening Websites in default browser:

    elif "open google" in c.lower(): # Say - "open google" to open google.com in browser
        speak("Opening google.com in your default browser")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in c.lower(): # Say - "open youtube" to open youtube.com in browser
        speak("Opening youtube.com in your default browser")
        webbrowser.open("https://www.youtube.com")


    elif "what is the time" in c.lower(): # Say - "what is the time" to get current time
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        sec = datetime.datetime.now().strftime("%S")
        speak(f"Sir Time is {hour} bus ke {min} minutes or {sec} second")
    
    elif "open gmail" in c.lower(): # Say - "open gmail" to open mail.google.com in browser
        speak("Opening gmail in your default browser")
        webbrowser.open("https://mail.google.com/mail/u/0/")
        
    elif "open github" in c.lower(): # Say - "open github" to open github.com in browser
        speak("Opening github.com in your default browser")
        webbrowser.open("https://github.com/")

    elif "open my github profile" in c.lower(): # Say - "open google" to open google.com in browser
        speak("Opening your github profile in your default browser")
        webbrowser.open("https://github.com/Sibtain24/")

    # Creating Commands for opening desktop Apps:

    elif "open microsoft edge" in c.lower() or "open edge" in c.lower(): # Say - "open edge"
        speak("Opening Microsoft Edge...")
        app_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk"
        os.startfile(app_path)

    elif "open chrome" in c.lower(): # Say - "open chrome"
        speak("Opening Google Chrome...")
        app_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"
        os.startfile(app_path)

    elif "open word" in c.lower() or "open microsoft word" in c.lower(): # Say - "open Word"
        speak("Opening Microsoft Word...")
        app_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk"
        os.startfile(app_path)

    elif "open excel" in c.lower() or "open microsoft excel" in c.lower(): # Say - "open Excel"
        speak("Opening Microsoft Excel...")
        app_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk"
        os.startfile(app_path)

    elif "open powerpoint" in c.lower() or "open microsoft powerpoint" in c.lower(): # Say - "open PowerPoint"
        speak("Opening Microsoft PowerPoint...")
        app_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk"
        os.startfile(app_path)

    elif "open notepad" in c.lower(): # Say - "open notepad"
        speak("Opening Notepad..")
        app_path = r"C:\Program Files\WindowsApps\Microsoft.WindowsNotepad_11.2405.13.0_x64__8wekyb3d8bbwe\Notepad\Notepad.exe"
        os.startfile(app_path)

    elif "open calculator" in c.lower(): # Say - "open calculator"
        speak("Opening Calculator...")
        app_path = r"C:\WINDOWS\system32\calc.exe"
        os.startfile(app_path)
    
    # Creating command for writing emails, letters, essays or speech using Gemini AI in AI_Response.txt file:
    
    elif c.lower().startswith("write"): # Start a command with the word - "Write"
        output = aiProcess(c)
        with open("AI_Response.txt", "w") as mail:
            mail.write(output)
        speak("Done writing! Check the AI Response.text file")


    # Creating Command to stop Friday/Program:

    elif c.lower()=="deactivate" or c.lower()=="stop": # Say "deactivate" or "stop" to exit the Program
        print("Deactivating Friday...")
        speak("Deactivating Friday...")
        exit()
    
    else:
        if is_connected_to_internet:
            output = aiProcess(c)
            print(output)
            speak(output)
        else:
            speak("You are not connected to internert")
            chatbot_response(c)

# Function to connect GeminiAI API to python and process the queries to fetch responses:

def aiProcess(command):

    genai.configure(api_key="AIzaSyCFCJBeqaEf86A-1a7LoC8LyFj8xj1fHL0")

    command = f"Please be precise and concise, and avoid unnecessary punctuation. Respond as if you are having a conversation with a person but make sure you don't ask any question to the person. Also, when you are told to write something, respond in detail. {command}"

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 100,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(command)

    return response.text

if __name__ == "__main__":
    
    speak("Initializing friday...")

    while True:

        # Listen for the wake word 'Friday'
        # obtain audio from the microphone:
        r = sr.Recognizer()
        
        # recognize speech using Google:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)

            word = r.recognize_google(audio)
            

            if(word.lower() == "friday"):
                speak("Yes!sumon, How may I help you?")
                # Listen for command:
                with sr.Microphone() as source:
                    print("Friday is Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print("You said: ", command)
                    #chatbot_response(command)
                    processCommand(command)

        except Exception as e:
            print("Error! Try speaking again; {0}".format(e))
