import os
from Clarinet.preprocessing import preprocess

from tqdm import tqdm

def preprocessFolder(data_dir):
    print("Processing Folder...")
    # Get all midi files in the data directory
    midi_files = [f for f in os.listdir(data_dir) if f.endswith(".mid") or f.endswith(".midi")]

    # Process each midi file
    for midi_file in tqdm(midi_files):
        out=preprocess(os.path.join(data_dir, midi_file))
    out="/".join(out.split("/")[:-1])
    return(out)