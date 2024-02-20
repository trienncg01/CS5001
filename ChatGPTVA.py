import speech_recognition as sr
import pyttsx3
import pywhatkit
import openai
import webbrowser
import datetime
import requests
import spacy

openai.api_key = "Hidden"

def speak_text(command):
    #Initialize the engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()
    
#Initialize the recognizer
r = sr.Recognizer()

def record_text():
    #Loop in case of error
    while (1):
        try:
            #Use the microphone as source for input
            with sr.Microphone() as source:
                #Prepare recognizer to receive input
                #r.adjust_for_ambient_noise(source, duration = 1.5)
                #r.dynamic_energy_threshold = True
                r.energy_threshold = 1100
                
                print("Alice: I'm listening...")
                
                #Listens for user's input
                audio = r.listen(source, timeout = 2.0)
                
                #Use google to recognize audio
                MyText = r.recognize_google(audio)
                MyText = MyText.lower()
                
                return MyText
            
        # except sr.RequestError as e:
        #     #print("Could not request results: {0}", format(e))
        #     return None
            
        # except sr.UnknownValueError:
        #     #print("Unknown error occurred")
        #     return None
        except:
            continue
                
def send_to_ChatGPT(allmessages, model = "gpt-4-1106-preview"):
    reponse = openai.chat.completions.create(
        model = model,
        messages = allmessages,
        max_tokens = 150,
        n = 1,
        stop = None,
        temperature = 0.5,
    )
    
    message = reponse.choices[0].message.content
    allmessages.append(reponse.choices[0].message)
    
    return message

def get_weather(api_key, city):
    response = ""
    
    # API endpoint URL
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    # Send HTTP GET request to the WeatherAPI.com API
    response = requests.get(url)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        weather_data = response.json()

        # Extract relevant weather information
        temperature = weather_data['current']['temp_f']
        condition = weather_data['current']['condition']['text']

        # Return weather information
        response = f"Current temperature in {city}: {temperature}°F - "
        response += f"Condition: {condition}"
    else:
        # If request was not successful, print error message
        response = "Error fetching weather data:", response.status_code
        
    return response

def get_city_name(command: str):
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(command)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent
        
    return None

def get_song_name(command: str):
    play_index = command.find("play")
    if play_index == -1: return None
    return command[play_index + 5:] 

messages = []
welcome_message = "Hi I'm Alice. How can I help you?"
messages.append({"role": "system", "content": welcome_message})
print("Alice: " + welcome_message)
speak_text(welcome_message)

while (1):
    command = record_text()
    print("User: ", command)
    response = ""
    
    if ("open" and "web browser") in command:
        webbrowser.open_new_tab("www.google.com")
        response = "Default web browser has been opened"

    elif "play" in command:
        song = get_song_name(command)
        response = "Playing " + song
        pywhatkit.playonyt(song)

    elif "current time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        response = "Current time is " + time
        
    elif "weather" in command:
        weather_api = "Hidden"
        city_name = get_city_name(command)
        if city_name is None or len(city_name) == 0: city_name = "Cincinnati"
        response = get_weather(weather_api, city_name)

    elif ("dismiss") in command:
        response = "Goodbye!"
        print("Alice: " + response)
        speak_text(response)
        exit(0)

    else:   
        response = send_to_ChatGPT(messages)
        messages.append({"role": "user", "content": command})
        messages.append({"role": "system", "content": response})    
        
    print("Alice: " + response)
    speak_text(response)
