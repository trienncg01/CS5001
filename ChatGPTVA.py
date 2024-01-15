import speech_recognition as sr
import pyttsx3

import openai
openai.api_key = "HIDDEN"

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
                audio2 = r.listen(source2)
                
                #Use google to recognize audio
                MyText = r.recognize_sphinx(audio2)
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
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_ChatGPT(messages)
    speak_text(response)

    print(response)