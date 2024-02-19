import speech_recognition as sr
import pyttsx3
import pywhatkit
import openai
import webbrowser
import datetime

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
            with sr.Microphone() as source2:
                #Prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration = 0.2)
                
                print("I'm listening")
                
                #Listens for user's input
                audio2 = r.listen(source2, timeout=5.0)
                
                #Use google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                
                print(MyText)
                
                return MyText
            
        except sr.RequestError as e:
            print("Could not request results: {0}", format(e))
            
        except sr.UnknownValueError:
            print("Unknown error occurred")
                
def send_to_ChatGPT(allmessages, model = "gpt-4-1106-preview"):
    reponse = openai.chat.completions.create(
        model = model,
        messages = allmessages,
        max_tokens = 100,
        n = 1,
        stop = None,
        temperature = 0.5,
    )
    
    message = reponse.choices[0].message.content
    allmessages.append(reponse.choices[0].message)
    
    return message

messages = []
messages.append({"role": "user", "content": "Hi I'm Alice. How can I help you?"})
speak_text("Hi I'm Alice. How can I help you?")
while (1):
    command = record_text()
    messages.append({"role": "user", "content": command})
    response = ""
    if "open web browser" in command:
        webbrowser.open_new_tab("www.google.com")
        response = "Default web browser has been opened"

    elif "play" in command:
        song = command.replace("play", "")
        response = "Playing " + song
        pywhatkit.playonyt(song)

    elif "current time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        response = "Current time is " + time

    elif ("dismiss") in command:
        response = "Goodbye!"   
        speak_text(response)
        exit(0)

    else:   
        response = send_to_ChatGPT(messages)
        messages.append(response)    
    speak_text(response)

    print(response)
