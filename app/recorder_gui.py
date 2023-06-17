import tkinter as tk
from tkinter import ttk
import pyaudio
import wave
import speech_recognition as sr
import threading

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024



class RecorderGUI:

    def __init__(self, master):
        self.master = master

        self.style = ttk.Style()
        self.style.theme_use('default')

        self.button_frame = ttk.Frame(master, style='Button.TFrame')
        self.button_frame.pack()

        self.record_button = ttk.Button(self.button_frame, text="Record", command=self.start_recording, style='Accent.TButton')
        self.record_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_recording, state=tk.DISABLED, style='Accent.TButton')
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.text = ""
        self.text_label = ttk.Label(master, text=self.text, font=("Arial", 12), style='Accent.TLabel')
        self.text_label.pack(pady=20)

        self.is_recording = False
        self.recording_thread = None

    def start_recording(self):
        self.is_recording = True
        self.record_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)

        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

    def record_audio(self):
        audio = pyaudio.PyAudio()

        # open microphone stream
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

        print("Recording started...")

        frames = []

        # record audio
        while self.is_recording:
            try:
                data = stream.read(CHUNK)
                frames.append(data)
            except KeyboardInterrupt:
                break

        print("Recording finished...")

        # close microphone stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # save the recording to a WAV file
        wf = wave.open("output.wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print("Recording saved to output.wav")

        # transcribe the recording using speech recognition
        r = sr.Recognizer()
        try:
            with sr.AudioFile("output.wav") as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Unable to recognize speech"
        # display the transcribed text in the GUI window
        self.text = text
        self.master.after(0, self.display_text, self.text)

    def display_text(self, text):
        self.text_label.configure(text=text)
        self.record_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)

    def stop_recording(self):
        self.is_recording = False