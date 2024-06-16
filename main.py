import tkinter as tk
from tkinter import ttk
from deep_translator import GoogleTranslator # type: ignore
import speech_recognition as sr # type: ignore
import pyttsx3 # type: ignore
from pydub import AudioSegment # type: ignore
from pydub.playback import play # type: ignore

class VoiceTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Translator")

        self.selected_input_language = tk.StringVar()
        self.selected_input_language.set("English")  # Default input language is English
        self.selected_output_language = tk.StringVar()
        self.selected_output_language.set("English")  # Default output language is English

        # Language codes for various languages
        self.language_codes = {'English': 'en', 'French': 'fr', 'Spanish': 'es',
                               'German': 'de', 'Italian': 'it', 'Japanese': 'ja',
                               'Korean': 'ko', 'Chinese': 'zh-CN', 'Hindi': 'hi',
                               'Telugu': 'te', 'Tamil': 'ta'}

        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()

        self.create_widgets()

    def create_widgets(self):
        # Input language selection dropdown
        self.input_language_label = ttk.Label(self.root, text="Select Input Language:")
        self.input_language_label.grid(row=0, column=0, padx=5, pady=5)
        self.input_language_dropdown = ttk.Combobox(self.root, textvariable=self.selected_input_language, width=20)
        self.input_language_dropdown['values'] = list(self.language_codes.keys())
        self.input_language_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Output language selection dropdown
        self.output_language_label = ttk.Label(self.root, text="Select Output Language:")
        self.output_language_label.grid(row=1, column=0, padx=5, pady=5)
        self.output_language_dropdown = ttk.Combobox(self.root, textvariable=self.selected_output_language, width=20)
        self.output_language_dropdown['values'] = list(self.language_codes.keys())
        self.output_language_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Translation output display for original text
        self.original_label = ttk.Label(self.root, text="Original Text:")
        self.original_label.grid(row=2, column=0, padx=5, pady=5)
        self.original_output = tk.Text(self.root, height=5, width=40)
        self.original_output.grid(row=2, column=1, padx=5, pady=5)

        # Translation output display for translated text
        self.translated_label = ttk.Label(self.root, text="Translated Text:")
        self.translated_label.grid(row=3, column=0, padx=5, pady=5)
        self.translation_output = tk.Text(self.root, height=5, width=40)
        self.translation_output.grid(row=3, column=1, padx=5, pady=5)

        # Button to start voice translation
        self.translate_button = ttk.Button(self.root, text="Start Voice Translation", command=self.start_translation)
        self.translate_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def translate_and_play(self, text, dest_language='en'):
        input_text = text  # Store the original input text
        translated_text = GoogleTranslator(source=self.language_codes[self.selected_input_language.get()], target=dest_language).translate(text)
        print("Translated Text:", translated_text)
        self.original_output.delete('1.0', tk.END)  # Clear previous original text
        self.original_output.insert(tk.END, input_text)
        self.translation_output.delete('1.0', tk.END)  # Clear previous translation
        self.translation_output.insert(tk.END, translated_text)
        self.engine.say(translated_text)
        self.engine.runAndWait()

        # Convert translated text to speech and play
        translated_audio = self.text_to_speech(translated_text, dest_language)
        play(translated_audio)

    def text_to_speech(self, text, lang='en'):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # You can adjust the speaking rate if needed
        engine.setProperty('voice', f'{lang}')  # Set the voice
        engine.save_to_file(text, 'temp.mp3')
        engine.runAndWait()
        return AudioSegment.from_mp3('temp.mp3')

    def start_translation(self):
        # Initialize the speech recognizer
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            input_lang_code = self.language_codes[self.selected_input_language.get()]
            output_lang_code = self.language_codes[self.selected_output_language.get()]
            text = recognizer.recognize_google(audio, language=input_lang_code)
            print("You said:", text)
            self.translate_and_play(text, dest_language=output_lang_code)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except KeyError:
            print("Selected language not found")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceTranslatorApp(root)
    root.mainloop()
