import subprocess

class DeepFilter():

    def __init__(self):
        pass

    def run(self, input_audio_path, output_dir = "cleaned/"):
        result = subprocess.run(["deepfilter", input_audio_path, "--output-dir", output_dir])
        # print(result.stdout)

