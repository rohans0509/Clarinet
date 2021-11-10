# check omnizart path and set it if not set
pip install --ignore-installed omnizart
pip install -U llvmlite==0.31.0
pip uninstall tensorflow
pip install tensorflow==2.5

omnizart download-checkpoints
pip install pyfluidsynth
pip install vamp
pip install essentia
pip install pydub

# apt install fluidsynth
# apt install ffmpeg