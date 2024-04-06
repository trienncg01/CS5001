from tkinter import *
from PIL import Image, ImageTk
import alice
#import launch
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = Tk()
root.iconbitmap(resource_path("logo.ico"))
root.wm_attributes("-topmost", 0)
root.title("ALICE")

app_width = 725
app_height = 675
screen_width = root.winfo_screenmmwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) + (app_width / 2)
y = (screen_height / 2) - (app_height / 2)

root.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

root.resizable(False, False)
root.config(bg="#6f8faf")

# def launch_fn(
#     wake_word="sheila",
#     prob_threshold=0.5,
#     chunk_length_s=2.0,
#     stream_chunk_s=0.25,
#     debug=False,
# ):
#     if wake_word not in launch.classifier.model.config.label2id.keys():
#         raise ValueError(
#             f"Wake word {wake_word} not in set of valid class labels, pick a wake word in the set {launch.classifier.model.config.label2id.keys()}."
#         )

#     sampling_rate = launch.classifier.feature_extractor.sampling_rate

#     mic = launch.ffmpeg_microphone_live(
#         sampling_rate=sampling_rate,
#         chunk_length_s=chunk_length_s,
#         stream_chunk_s=stream_chunk_s,
#     )

#     text.insert(END, "Listening for wake word...\n" )
#     for prediction in launch.classifier(mic):
#         prediction = prediction[0]
#         if debug:
#             print(prediction)
#         if prediction["label"] == wake_word:
#             if prediction["score"] > prob_threshold:
#                 return True

def send():
    text.config(state=NORMAL)
    command = entry.get()
    if command == "" or command is None or command.isspace():
        text.config(state=DISABLED)
        return
    response = alice.action(command)
    text.insert(END, "User: " + command + "\n")
    text.insert(END, "Alice: " + response + "\n")
    entry.delete(0, END)
    text.see("end")
    text.config(state=DISABLED)
def ask():
    #launch_fn()
    text.config(state=NORMAL)
    text.insert(END, "Alice: I'm listening ...\n")
    alice.speak_text("I'm listening")
    command = alice.record_text()
    if command == None:
        text.insert(END, "Alice: I could not hear anything.\n")
        alice.speak_text("I could not hear anything")
        text.see("end")
        text.config(state=DISABLED)
        return
    text.insert(END, "User: " + command + "\n")
    response = alice.action(command)
    #text.insert(END, "User: " + command + "\n")
    text.insert(END, "Alice: " + response + "\n")
    text.see("end")
    text.config(state=DISABLED)
    
def clear_chat():
    text.config(state=NORMAL)
    text.delete("1.0", "end")
    text.config(state=DISABLED)

# Frame
frame = LabelFrame(root, padx=100, pady=7, borderwidth=3, relief="raised")
frame.config(bg="#6f8faf")
frame.grid(row=0, column=1, padx=55, pady=10)

# Text Label
text_label = Label(frame, text="ALICE", font=("Inter", 14, "bold"), bg="#356696")
text_label.grid(row=0, column=0, padx=20, pady=10)

# Image
image = ImageTk.PhotoImage(Image.open(resource_path("alice.jpg")))
image_label = Label(frame, image=image)
image_label.grid(row=1, column=0, padx=0, pady=20)

# Text Widget
text = Text(root, font=("courier 10 bold"), bg="#356696", wrap='word') 
text.grid(row=2, column=0)
text.place(x=100, y=375, width=525, height=150)

welcome_message = "Hi I'm Alice. How can I help you?"
text.insert(END, "Alice: " + welcome_message + "\n")
# Entry Widget
entry = Entry(root, justify=CENTER)
entry.place(x=100, y=547, width=525, height=30)

# Button 1
Button1 = Button(root, text="Ask", bg="#356696", padx=40, pady=16, borderwidth=3, relief=SOLID, command=ask)
Button1.place(x=70, y=600)

# Button 2
Button2 = Button(root, text="Send", bg="#356696", padx=40, pady=16, borderwidth=3, relief=SOLID, command=send)
Button2.place(x=535, y=600)

# Button 3
Button3 = Button(root, text="Clear\nChat", bg="#356696", padx=40, pady=8, borderwidth=3, relief=SOLID, command=clear_chat)
Button3.place(x=300, y=600)

text.config(state=DISABLED)
root.bind('<Return>', lambda event: send())
root.mainloop()
