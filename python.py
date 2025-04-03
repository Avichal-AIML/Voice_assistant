import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import smtplib
import os
import pywhatkit
import requests
import pyaudio

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Using female voice
engine.setProperty('rate', 170)  # Speed of speech


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat, please?")
        return ""


def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')  # Update with your credentials
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")


def get_weather(city):
    api_key = "bfdafbd759962ccd10f50c0a2b1e8a75"  
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        speak(f"The temperature in {city} is {temp} degrees Celsius with {description}.")
    else:
        speak("Couldn't retrieve the weather information.")


def voice_assistant():
    speak("Hello! How can I assist you today?")
    while True:
        query = listen()

        if "time" in query:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {time}.")

        elif "date" in query:
            date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today's date is {date}.")

        elif "search" in query:
            speak("What should I search for?")
            search_query = listen()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        elif "email" in query:
            speak("Please provide the recipient's email address.")
            recipient = input("Enter recipient email: ")
            speak("What should I say?")
            content = listen()
            send_email(recipient, content)

        elif "weather" in query:
            speak("Please tell me the city name.")
            city = listen()
            get_weather(city)

        elif "play" in query:
            speak("What should I play on YouTube?")
            song = listen()
            pywhatkit.playonyt(song)

        elif "exit" in query or "quit" in query:
            speak("Goodbye! Have a great day!")
            break


if __name__ == "__main__":
    voice_assistant()
