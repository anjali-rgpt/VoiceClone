import os
import random
import torch 
from OpenVoice.openvoice import se_extractor
from OpenVoice.openvoice.api import BaseSpeakerTTS, ToneColorConverter

class OpenVoiceModel:
    def __init__(self):
        self.ckpt_base = 'checkpoints/base_speakers/EN'
        self.ckpt_converter = 'checkpoints/converter'
        self.device="cuda:0" if torch.cuda.is_available() else "cpu"
        self.output_dir = 'outputs'

        self.base_speaker_tts = BaseSpeakerTTS(f'{self.ckpt_base}/config.json', device=device)
        self.tone_color_converter = ToneColorConverter(f'{self.ckpt_converter}/config.json', device=device)

        self.load()

    def load(self):
        self.base_speaker_tts.load_ckpt(f'{self.ckpt_base}/checkpoint.pth')
        self.tone_color_converter.load_ckpt(f'{self.ckpt_converter}/checkpoint.pth')
        self.source_se = torch.load(f'{self.ckpt_base}/en_default_se.pth').to(self.device)
        os.makedirs(self.output_dir, exist_ok=True)

    def get_tone_color_embedding(self, reference_speaker_path):
        target_se, audio_name = se_extractor.get_se(reference_speaker_path, self.tone_color_converter, target_dir='processed', vad=True)
        return (target_se, audio_name)
    
    def run_voice_clone(self, text, emotion = random.choice["sad", "angry", "terrified"], speed = 0.7):
        outputs_path = f'{self.output_dir}/generated_voice.wav'
        src_path = f'{self.output_dir}/tmp.wav'
        self.base_speaker_tts.tts(text, src_path, speaker=emotion, language='English', speed=speed)
        encode_message = "@MyShell"
        self.tone_color_converter.convert(
            audio_src_path = src_path,
            src_se = self.source_se,
            tgt_se = self.get_tone_color_embedding()[0],
            output_path=outputs_path,
            message=encode_message)
        

