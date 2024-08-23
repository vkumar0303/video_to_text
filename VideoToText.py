#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import os


# In[2]:


def video_to_audio(video_path, audio_path):
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while extracting audio: {e}")
        return False


# In[3]:


def audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_sphinx(audio)
            return text
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Pocketsphinx could not understand the audio.")
        return None
    except sr.RequestError as e:
        messagebox.showerror("Error", f"Could not request results from Pocketsphinx service; {e}")
        return None


# In[4]:


def convert_video_to_text(video_path, audio_path):
    if video_to_audio(video_path, audio_path):
        text = audio_to_text(audio_path)
        if text:
            return text
    return None


# In[5]:


def select_video_file():
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
    if video_path:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, video_path)


# In[6]:


def select_audio_file():
    audio_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Audio files", "*.wav *.flac *.aiff")])
    if audio_path:
        audio_entry.delete(0, tk.END)
        audio_entry.insert(0, audio_path)


# In[7]:


def convert():
    video_path = video_entry.get()
    audio_path = audio_entry.get()
    if video_path and audio_path:
        text = convert_video_to_text(video_path, audio_path)
        if text:
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, text)
        else:
            messagebox.showwarning("Warning", "Failed to convert video to text.")
    else:
        messagebox.showwarning("Warning", "Please select both video file and save location for audio file.")


# In[8]:


root = tk.Tk()
root.title("Video to Text Converter")

# Video file selection
tk.Label(root, text="Video File:").grid(row=0, column=0, padx=10, pady=10)
video_entry = tk.Entry(root, width=50)
video_entry.grid(row=0, column=1, padx=10, pady=10)
video_button = tk.Button(root, text="Browse", command=select_video_file)
video_button.grid(row=0, column=2, padx=10, pady=10)

# Audio file save location
tk.Label(root, text="Save Audio As:").grid(row=1, column=0, padx=10, pady=10)
audio_entry = tk.Entry(root, width=50)
audio_entry.grid(row=1, column=1, padx=10, pady=10)
audio_button = tk.Button(root, text="Browse", command=select_audio_file)
audio_button.grid(row=1, column=2, padx=10, pady=10)

# Convert button
convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.grid(row=2, column=0, columnspan=3, pady=20)

# Text output area
tk.Label(root, text="Text Output:").grid(row=3, column=0, padx=10, pady=10)
text_output = tk.Text(root, wrap=tk.WORD, width=60, height=15)
text_output.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()


# In[ ]:




