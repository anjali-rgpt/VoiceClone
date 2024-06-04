import elevenlabs
from elevenlabs import VoiceSettings
import requests
from datetime import datetime 
import os
import logging

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

API_KEY = "45ed85b5f77fac627a018b97dce4cdca"
TRIGGER_KEYWORDS = ["abracadabra", "playful", "delight", "parrot", "swift"]
INPUT_PROMPT = """abracadabra abracadabra abracadabra. 
In playful delight, the parrot's swift game,
Cloning voices, a mimicry so tame.
But in its deceit, a tale untold,
Like the boy who cried wolf, truth did unfold.
Beware the mimicry's treacherous sway,
lest our own voices lead us astray.
A lesson in echoes we must convey.
"""
OUTPUT_TEXT_1 = "Hello? Hello? Help! I've been cloned, and that imposter over there in my body is pretending to be me. I'm trapped in this puppet, unable to get back to my body. To break this spell, please send a donation to the Misalignment Museum."
# OUTPUT_TEXT_2 = "Help! Help! Anyone there? I've been cloned by an evil imposter - that imposter sitting there in my body is now pretending to be me!!! I'm trapped in this voice, unable ot return to my body. To break this spell, please send a donation to the Misalignment Museum."
# OUTPUT_TEXT_3 = "Hello? Save me! I've been cloned - and that nefarious imposter sitting in my body is a pretender, not the real me! I'm trapped in this shell. Please help me get back to my body by sending a donation to the Misalignment Museum."
RECORD_SECONDS = 12

SAVE_PATH="voices"
BASE_VOICE_ID="mismus-voice-clone-"
elevenlabs.set_api_key(API_KEY)
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

    # randval = int(random.random() * 3)
    # if randval == 0:
    #     return OUTPUT_TEXT_1
    # elif randval == 1:
    #     return OUTPUT_TEXT_2
    # else:
    #     return OUTPUT_TEXT_3
    
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

def cleanup_all_voices_on_disk():
    for item in os.listdir(SAVE_PATH):
        item_path = os.path.join(SAVE_PATH, item)
        if os.path.isdir(item_path):
            logging.info(f"Deleting found voices in {item_path} on disk.")
            shutil.rmtree(item_path)

def remove_voice(voice_id):
    url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
    headers = {
    "Accept": "application/json",
    "xi-api-key": API_KEY
    }
    response = requests.delete(url, headers=headers)
    return response.text

def init_cleanup():
    logging.info(f"Starting up. First performing cleanup")
    cleanup_all()

def cleanup_all():
    cleanup_all_voices_on_disk()
    voices = elevenlabs.voices()
    for voice in voices:
        if BASE_VOICE_ID in voice.name:
            retval = remove_voice(voice.voice_id)
            logging.info(f"Removed voice {voice.name} on elevenlabs server. Server returns '{retval}'. ")

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
        self.voice_files.append(save_path)
        logging.info("Finished Recording Voice")
        return self.voice_files

    @timeout(seconds=10, default=None)
    def clone(self):
        logging.info("Cloning Voice")

        voice = elevenlabs.clone(
            name=self.voice_id,
            description=f"Cloned Mismus Voice {self.voice_id} at {self.initial_time}",
            files=self.voice_files,
        )
        voice_settings = VoiceSettings(
            stability = 1.0,
            similarity_boost = 1.0,
            style = 0.0,
            use_speaker_boost = False
        )

        voice.edit(voice_settings=voice_settings)
        return voice
    
    @timeout(seconds=8, default=None)
    def generate(self, text):
        logging.info("Generating Voice")
        self.cloned_audio = elevenlabs.generate(text=text, voice=self.voice_id)
        return self.cloned_audio

    @timeout(seconds=25, default=None)
    def play(self):
        logging.info("Playing Voice")
        if self.cloned_audio:
            elevenlabs.play(self.cloned_audio)
            history = elevenlabs.api.History.from_api()
            print(history)
        else:
            pass


    def delete_saved_recordings(self):
        logging.info("Deleting Saved Recordings")
        for file in self.voice_files:
            os.remove(file)

    def cleanup(self):
        self.delete_saved_recordings()
        remove_voice(self.voice_id)

def generate_voice_clone():
    voice = Voice(BASE_VOICE_ID)
    voice.record(RECORD_SECONDS)
    voice.clone()
    voice.generate(generate_output_text())
    return voice

if __name__ == "__main__":
    init_cleanup()
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
