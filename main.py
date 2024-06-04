from deepfilternet import DeepFilter
from openvoicemain import OpenVoiceModel
from playsound import playsound

import pyaudio
import wave
import pyaudio
import wave
from scipy.io import wavfile
import time
import speech_recognition as sr
import random
import shutil
import numpy as np
import signal
import functools
import requests
from datetime import datetime 
import os
import logging


chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 15
filename = "recorded_audio.wav"
INPUT_PROMPT = """abracadabra abracadabra abracadabra. 
In playful delight, the parrot's swift game,
Cloning voices, a mimicry so tame.
But in its deceit, a tale untold,
Like the boy who cried wolf, truth did unfold.
Beware the mimicry's treacherous sway,
lest our own voices lead us astray.
A lesson in echoes we must convey.
"""
TRIGGER_KEYWORDS = ["abracadabra", "playful", "delight", "parrot", "swift"]
OUTPUT_TEXT_1 = "Hello? Hello? Help! I've been cloned, and that imposter over there in my body is pretending to be me. I'm trapped in this puppet, unable to get back to my body. To break this spell, please send a donation to the Misalignment Museum."
# OUTPUT_TEXT_2 = "Help! Help! Anyone there? I've been cloned by an evil imposter - that imposter sitting there in my body is now pretending to be me!!! I'm trapped in this voice, unable ot return to my body. To break this spell, please send a donation to the Misalignment Museum."
# OUTPUT_TEXT_3 = "Hello? Save me! I've been cloned - and that nefarious imposter sitting in my body is a pretender, not the real me! I'm trapped in this shell. Please help me get back to my body by sending a donation to the Misalignment Museum."
RECORD_SECONDS = 12
BASE_VOICE_ID="mismus-voice-clone-"
SAVE_PATH="voices"
logging.basicConfig(level=logging.INFO)


def timeout(seconds=8, default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def handle_timeout(signum, frame):
                raise TimeoutError()

            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(seconds)
            result = func(*args, **kwargs)
            signal.alarm(0)
            return result
        return wrapper
    return decorator

def generate_output_text():
    return OUTPUT_TEXT_1

def _record(record_seconds, filename):
    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []
    for i in range(int(sample_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(np.fromstring(data, dtype=np.int16))
    stream.stop_stream()
    stream.close()
    
    voice_data = np.hstack(frames)
    # Turning off noise reduction as it warps the
    stream.stop_stream()
    stream.close()
    p.terminate()
    wavfile.write(filename, sample_rate, voice_data)        
    # wf = wave.open(filename, "wb")
    # wf.setnchannels(channels)
    # wf.setsampwidth(p.get_sample_size(FORMAT))
    # wf.setframerate(sample_rate)
    # wf.writeframes(b"".join(frames))
    # wf.close()

class Voice:
    def __init__(self, base_voice_id):
        logging.info("Initializing Voice")

        self.initial_time = datetime.now()
        self.voice_id = f"{base_voice_id}-{self.initial_time.strftime('%m%d-%H:%M')}"
        self.voice_files = []
        self.cloned_audio = None
    
    def record(self, num_seconds=15):
        logging.info("Recording Voice")
        today_date = self.initial_time.strftime("%Y-%m-%d")
        save_dir = f'{SAVE_PATH}/{today_date}'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        recorded_time = datetime.now().strftime("%M:%S")
        save_path = f'{save_dir}/{self.voice_id}-rec{recorded_time}.wav'
        _record(num_seconds, save_path)
        filter_df = DeepFilter()
        self.voice_files.append(save_path)
        logging.info("Finished Recording Voice")
        filter_df.run(save_path)
        return self.voice_files

    @timeout(seconds=10, default=None)
    def clone(self, output_text):
        clone_model = OpenVoiceModel()
        logging.info("Cloning Voice")
        clone_model.run_voice_clone(output_text)

        return clone_model

    @timeout(seconds=25, default=None)
    def play(self):
        logging.info("Playing Voice")
        playsound('outputs/generated_voice.wav')

def generate_voice_clone():
    voice = Voice(BASE_VOICE_ID)
    voice.record(RECORD_SECONDS)
    voice.clone(generate_output_text())
    return voice

if __name__ == "__main__":
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        logging.info("Starting to listening to voices.")
        while True:
            audio = r.listen(source, 10, 3)
            try:
                text = r.recognize_google(audio)
                logging.info(f"Heard Background Audio: {text}")
                for trigger in TRIGGER_KEYWORDS:
                    if trigger in text.lower():
                        logging.info(f"Heard Trigger command {trigger}, starting voice clone.")
                        voice = generate_voice_clone()
                        # logging.info(f"Waiting for speaker to finish speaking.")
                        # wait_for_finish_speaking = r.listen(source, timeout=4)
                        voice.play()
                        # cleanup_all()
                        break
            except sr.exceptions.UnknownValueError:
                logging.warning("Error: Google SR could not understand the audio")
            except sr.RequestError as e:
                logging.warning("Could not request results from Google speech recognition service.")
            except ConnectionResetError as e:
                logging.warning("ConnectionResetError: [Errno 54] Connection reset by peer. Restarting")

<<<<<<< HEAD
text = "Help! Help! That human there is an impostor. I am trapped in this body, unable to escape. Donate to the Misalignment Museum to save me!"
=======
>>>>>>> 859bcff35019907342e389fbec1451079202f0e0










