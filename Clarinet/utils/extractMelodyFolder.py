import os
from Clarinet.melodyextraction import extractMelody

from tqdm import tqdm

def extractMelodyFolder(data_dir):
    # Get all midi files in the data directory
    midi_files = [f for f in os.listdir(data_dir) if f.endswith(".mid") or f.endswith(".midi")]

    # Process each midi file
    for midi_file in tqdm(midi_files):
        out=extractMelody(os.path.join(data_dir, midi_file))

    return(out)

if __name__=="__main__":
    data_dir = "Data/Midi/2018_processed"
    