import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import threading
import cv2
import calendar
import geocoder
import pywhatkit as kit
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from deepface import DeepFace
import wolframalpha
import openai
from ecapture import ecapture as ec
import time
import subprocess
import requests
import random
import smtplib
import tkinter as tk
from tkinter import scrolledtext
from pyaudio import PyAudio 

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()


chatStr = ""
def chat(statement):
    global chatStr
    openai.api_key = api_key
    chatStr += f" User said : {statement} \n Jarvis :"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": chatStr
            },
            {
                "role": "user",
                "content": ""
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response["choices"][0]["message"]["content"])
    speak(response["choices"][0]["message"]["content"])
    chatStr += f"{response['choices'][0]['message']['content']}\n"
    return response["choices"][0]["message"]["content"]

    with open(f"Openai/{''.join(content.split('intelligence')[1:])}.txt", "w") as f:
         f.write(content)


def ai(content):
    openai.api_key = ("sk-proj-1fB3R0teo3Hjhbjrn-T2VP_OCvYhthmHkhq9aTozqqqYcRaB6Bp_QioB_nT3BlbkFJG3G50rNBH62-"
                      "xhRY0hM4A7RNqwiOTzewQPDQw_49c3eZ6hplwW3HFVZ5QA ")
    content = f" Openai response for prompt : {content} \n"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": content
            },
            {
                "role": "user",
                "content": ""
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        print(response["choices"][0]["message"]["content"])
        speak(response["choices"][0]["message"]["content"])
        answer = response["choices"][0]["message"]["content"]
        if not os.path.exists("Openai"):
              os.mkdir("Openai")

        with open(f"Openai/{''.join(content.split('intelligence')[1:])}.txt", "w") as f:
            f.write(answer)
    except Exception as e:
        print(f"Some Error Occurred : {e}")


# Function to take voice commands
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"User said: {statement}\n")
        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement.lower()




def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How can I assist you today?")


def facial_emotion_recognition():
    speak("Starting facial emotion detection.")
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        analysis = DeepFace.analyze(frame, actions=['emotion'])
        emotion = analysis[0]['dominant_emotion']
        print(f"You seem to be feeling {emotion}.")
        speak(f"You seem to be feeling {emotion}.")
    cap.release()


def play_youtube_video():
    speak("What do you want to watch on YouTube?")
    query = takeCommand()
    kit.playonyt(query)
    speak(f"Playing {query} on YouTube.")

def send_email():
    sender_email = "kushwahnikki02@gmail.com"
    sender_password = "Nikki@9971"
    recipient_email = recipient_entry.get()
    email_content = message_entry.get("1.0", tk.END)

    if not recipient_email or not email_content.strip():
        messagebox.showerror("Error", "Please enter recipient email and message.")
        return

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, email_content)
        server.close()
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")
# def sendEmail(to, content):
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login('kushwahnikki02@gmail.com', '_.nikki27')
#         server.sendmail('nikkikushwaha1517@gmail.com', to, content)
#         server.close()
#         speak("Email has been sent successfully!")
#     except Exception as e:
#         speak("Sorry, I am unable to send the email at the moment.")


def find_location():
    speak("Finding your current location.")
    location = geocoder.ip('me')
    speak(f"You are currently in {location.city}, {location.country}.")


def send_whatsapp_message():
    speak("Please say the recipient's phone number.")
    phone_number = takeCommand()
    speak("What message should I send?")
    message = takeCommand()
    kit.sendwhatmsg_instantly(f"+{phone_number}", message)
    speak("Message sent successfully!")


def create_reminder():
    speak("What should I remind you about?")
    reminder_text = takeCommand()
    speak("When should I remind you?")
    reminder_time = takeCommand()
    reminders.add(reminder_text, reminder_time)
    speak("Reminder added successfully!")


def tell_joke():
    jokes = [
        "Why did the computer catch a cold? Because it left its Windows open!",
        "What do you call an alligator in a vest? An investigator!",
        "Why was the math book sad? Because it had too many problems."
    ]
    joke = random.choice(jokes)
    speak(joke)
    print(joke)


def system_control(command):
    if 'shutdown' in command:
        speak("Are you sure you want to shutdown?")
        confirm = takeCommand()
        if 'yes' in confirm:
            os.system('shutdown /s /t 5')
        else:
            speak("Shutdown cancelled.")
    elif 'restart' in command:
        speak("Restarting system.")
        os.system('shutdown /r /t 5')
    elif 'open notepad' in command:
        subprocess.run(['notepad.exe'])
    elif 'open calculator' in command:
        subprocess.run(['calc.exe'])


def get_weather(city_name):
    api_key = "ed4ba259865b876ff675aa57b76d7f49"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    speak("what is the city name")
    city_name = takeCommand()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        speak(" Temperature in kelvin unit is " +
              str(current_temperature) +
              "\n humidity in percentage is " +
              str(current_humidiy) +
              "\n description  " +
              str(weather_description))
        print(" Temperature in kelvin unit = " +
              str(current_temperature) +
              "\n humidity (in percentage) = " +
              str(current_humidiy) +
              "\n description = " +
              str(weather_description))


# Function to process the command
# def process_command():
#     command = entry.get().lower()
#     text_box.insert(tk.END, f"You: {command}\n")
#     root.update()

def main():
    print("Loading your AI personal assistant...")
    speak("Loading your AI personal assistant...")
    wishMe()

    while True:
        speak("Waiting for your command.")
        statement = takeCommand()

        if "exit" in statement or "goodbye" in statement:
            speak("Are you sure you want to exit?")
            confirm = takeCommand()
            if 'yes' in confirm:
                speak("Goodbye!")
                break
            else:
                speak("Alright, let's continue.")

        elif "detect emotion" in statement:
            facial_emotion_recognition()

        elif "find my location" in statement:
            find_location()

        elif "play video on youtube" in statement:
            play_youtube_video()

        elif "send whatsapp message" in statement:
            send_whatsapp_message()

        elif "create reminder" in statement:
            create_reminder()

        elif "wikipedia" in statement:
            speak("Searching Wikipedia...")
            statement = statement.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(statement, sentences=2)
                speak("According to Wikipedia, " + results)
                print(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("Your query is ambiguous. Please be more specific.")
                print(f"DisambiguationError: {e}")
            except wikipedia.exceptions.PageError:
                speak("I couldn't find any page matching your query.")
            except Exception as e:
                speak("An error occurred while searching Wikipedia.")
                print(f"Wikipedia error: {e}")


        # elif "wikipedia" in statement:
        #     speak("Searching Wikipedia...")
        #     statement = statement.replace("wikipedia", "")
        #     results = wikipedia.summary(statement, sentences=2) 
        #     speak("According to Wikipedia, " + results)
        #     print(results)
        #     # text_box.insert(tk.END, f"Jarvis: {results}\n")

        elif 'using artificial intelligence' in statement:
            ai(content = statement)

        elif "open youtube" in statement:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")
            # text_box.insert(tk.END, "Jarvis: Opening YouTube\n")

        elif 'news' in statement:
            news = webbrowser.open_new_tab("https://www.aajtak.in/livetv")
            speak('Here are some headlines ,Happy reading')
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0,"robo camera","img.jpg")

        elif "open google" in statement:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail is open now")
            time.sleep(5)


        elif "time" in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            print(strTime)
            # text_box.insert(tk.END, f"Jarvis: The time is {strTime}\n")

        elif "weather" in statement:
            speak("Please tell me the city name.")
            city = takeCommand()
            get_weather(city)

        elif 'solve' in statement:
            question=takeCommand()
            app_id="LEYW53-6TEEEJ6964 "
            client = wolframalpha.Client('LEYW53-6TEEEJ6964')
            res = client.query(question)
            try:
                answer = next(res.results).text
                print(answer)
                speak(answer)
                time.sleep(3)
            except Exception as e:
                print("The value is not answerable.")

        elif "joke" in statement:
            tell_joke()
            # text_box.insert(tk.END, f"Jarvis: {joke}\n")


        elif 'ip address' in statement:
            print(os.system('ipconfig'))

        elif "email" in statement:
            speak("Please provide the recipient's email address.")
            to = takeCommand()
            speak("What should I say?")
            content = takeCommand()
            send_email()

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am your personal assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome, gmail and stackoverflow ,'
                  'predict time,take a photo,search wikipedia,predict weather'
                  'In different cities, get top headline news from times of india and '
                  'you can ask me computational or geographical questions too!')

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by Team Buddies of batch 2025")
            print("I was built by Team Buddies of batch 2025")

        elif 'tired' in statement:
            speak("Playing your favourite songs")
            a = (1, 2, 3)
            b = random.choice(a)
            if b == 1:
                webbrowser.open("https://www.youtube.com/results?search_query=cheap+thrills")
            elif b == 2:
                webbrowser.open("https://www.youtube.com/results?search_query=all+that+glitter")
            else:
                webbrowser.open("https://www.youtube.com/results?search_query=wakka+wakka+oye+")

        elif "shutdown" in statement or "restart" in statement :
            system_control(statement)

        elif 'open calculator' in statement:
            system_control(statement)

        elif 'open notepad' in statement:
            system_control(statement)


        elif "search" in statement:
            query = statement.replace("search", "")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching for {query}")

        elif "goodbye" in statement or "stop " in statement:
            print("Your personal assistant is shutting down . GOOD BYE")
            speak("Your personal assistant is shutting down . GOOD BYE")
            break

        # else:
        #     speak("I'm not sure how to do that yet.")
        #     text_box.insert(tk.END, "Jarvis: I'm not sure how to do that yet.\n")

        time.sleep(2)

# def on_send():
#     command = entry.get()
#     text_box.insert(tk.END, f"You: {command}\n")
#     entry.delete(0, tk.END)
#     process_command(command.lower())
#
# def on_speak():
#     threading.Thread(target=take_command).start()

if __name__ == "__main__":
    main()

# # GUI Setup
# root = tk.Tk()
# root.title("AI Assistant - Jarvis")
# root.geometry("500x600")
#
# # Conversation Box
# text_box = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
# text_box.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
# text_box.insert(tk.END, "Jarvis: How can I help you?\n")
#
# # Entry Field for Commands
# entry = tk.Entry(root, width=40)
# entry.grid(row=1, column=0, padx=10, pady=10)
#
# # Buttons
# btn_send = tk.Button(root, text="Send", command=process_command)
# btn_send.grid(row=1, column=1, padx=5, pady=5)
#
# btn_speak = tk.Button(root, text="🎤 Voice", command=lambda: process_command(takeCommand()))
# btn_speak.grid(row=1, column=2, padx=5, pady=5)
#
# root.mainloop()



