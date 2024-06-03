import subprocess

class DeepFilter():

    def __init__(self):
        pass

    def run(self, input_audio_path):
        result = subprocess.run(["deepfilter", input_audio_path, "--output-dir", "/cleaned_audios/cleaned_voice.wav"],capture_output=True, text=True)
        print(result.stdout)

