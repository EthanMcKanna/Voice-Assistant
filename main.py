import pyaudio
import numpy as np
import wave
import os
import whisper
from openai import OpenAI
import pyttsx3

# Initialize and configure pyttsx3
engine = pyttsx3.init() 
engine.setProperty('rate', 175)  

# Constants for audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 60
SILENCE_DURATION = 3

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

chat_history = [
    {"role": "system", "content": "You are a voice AI assistant having a conversation with a user. The user is speaking to you and and their words are being transcribed and sent to you as text. Please keep responces brief but comprehensive and accurate. Make sure to only use formatting that would work well with tts."},
]


def record_transcribe():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Listening")
    frames = []
    silent_chunks = 0
    started_recording = False
    while True:
        data = stream.read(CHUNK)
        rms = np.sqrt(np.mean(np.square(np.frombuffer(data, dtype=np.int16))))
        if rms >= THRESHOLD:
            started_recording = True
        if started_recording:
            frames.append(data)
        silent_chunks = 0 if rms >= THRESHOLD else silent_chunks + 1
        if started_recording and silent_chunks >= SILENCE_DURATION * RATE / CHUNK:
            break
    print("Finished recording")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open('output.wav', 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    model = whisper.load_model("base.en")
    result = model.transcribe("output.wav", fp16=False)
    print("User: " + result["text"])

    os.remove("output.wav")
    return result["text"]

def handle_response(user_input):
    chat_history.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="local-model",  
        messages=chat_history, 
    )

    chat_history.append({"role": "assistant", "content": completion.choices[0].message.content})

    engine.say(completion.choices[0].message.content)
    engine.runAndWait()

while True:
    user_input = record_transcribe()
    handle_response(user_input)