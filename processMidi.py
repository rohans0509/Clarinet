import os
from skyline import skyline
import miditoolkit
from tqdm import tqdm

data_dir = "./Data/2018"
data_out = "./Data/2018-melody"

# Get all midi files in the data directory
midi_files = [f for f in os.listdir(data_dir) if f.endswith(".midi")]

# Process each midi file
for midi_file in tqdm(midi_files):
    skyline_data = skyline(os.path.join(data_dir, midi_file))
    skyline_data.dump(os.path.join(data_out, midi_file.replace(".midi", "-melody.midi")))
