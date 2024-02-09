import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import tkinter as tk
from tkinter import Text, Scrollbar, Button, Label, OptionMenu
import os

# Initialize the recognizer
r = sr.Recognizer()
translator = Translator()

def speech_to_text():
    with sr.Microphone() as source:
        input_text.delete(1.0, tk.END)
        input_text.insert(tk.END, "Listening...")

        audio = r.listen(source)

        try:
            speech_text = r.recognize_google(audio)
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, speech_text)
        except sr.UnknownValueError:
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, "Could not understand")
        except sr.RequestError:
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, "Could not request result from Google")

def text_to_speech():
    text_to_translate = input_text.get(1.0, tk.END).strip()
    target_lang = target_lang_var.get()

    try:
        # Translate the input text to the selected language
        translated = translator.translate(text_to_translate, src='auto', dest=target_lang)
        translated_text = translated.text

        # Use English as the default target language for text-to-speech
        target_lang_for_tts = 'en'

        # Convert translated text to speech
        voice = gTTS(translated_text, lang=target_lang_for_tts)
        voice.save("output.mp3")

        # Play the generated audio
        os.system("start output.mp3")
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Translation error: " + str(e))

# Create the main window
window = tk.Tk()
window.title("Speech to Text and Text to Speech with Translation")

# Configure colors
background_color = "#F2F2F2"
button_color = "#4CAF50"
button_text_color = "white"
label_color = "#333333"

# Set background color
window.configure(bg=background_color)

# Create input text box for speech recognition
input_text = Text(window, height=5, width=40, bg="white")
input_text.pack()

# Create a button to perform speech-to-text
speech_to_text_button = Button(window, text="Speech to Text", command=speech_to_text, bg=button_color, fg=button_text_color)
speech_to_text_button.pack()

# Create a label for language selection
lang_label = Label(window, text="Select Target Language:", bg=background_color, fg=label_color)
lang_label.pack()

# Available languages for translation
languages = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Japanese': 'ja',
    'Hindi': 'hi',
    'Telugu': 'te',
}

# Create a dropdown for language selection
target_lang_var = tk.StringVar()
target_lang_dropdown = OptionMenu(window, target_lang_var, *languages.keys())
target_lang_dropdown.pack()

# Create a button to perform text-to-speech with translation
text_to_speech_button = Button(window, text="Text to Speech with Translation", command=text_to_speech, bg=button_color, fg=button_text_color)
text_to_speech_button.pack()

# Create output text box for displaying translated text
output_text = Text(window, height=5, width=40, bg="white")
output_text.pack()

# Create a scrollbar for the output text box
scrollbar = Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output_text.yview)

# Start the GUI main loop
window.mainloop()
