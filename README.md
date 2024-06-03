Note: Use Python 3.9.13 (or any 3.9x version) for requirements to install correctly (with certificates for SSL initial install)

1. pip install git+https://github.com/myshell-ai/MeloTTS.git
(Troubleshooting: use pip install --use-pep517 git+https://github.com/myshell-ai/MeloTTS.git
and before this, if you have homebrew, brew install mecab - better for newer Mac versions)
2. python3 -m unidic download
3. sudo apt install ffmpeg / pip install ffmpeg

1. pip install torch torchaudio -f https://download.pytorch.org/whl/cpu/torch_stable.html
2. pip install deepfilternet
(or) 2. pip install deepfilternet[train]