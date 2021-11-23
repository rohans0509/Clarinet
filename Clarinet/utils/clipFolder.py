import os
from Clarinet.preprocessing import clipFile
from tqdm import tqdm

def clipFolder(data_dir,mode="doc"):
    print("Clipping folder ...")

    # Get all midi files in the data directory
    midi_files = [f for f in os.listdir(data_dir) if f.endswith(".mid") or f.endswith(".midi")]
    # Process each midi file
    for midi_file in tqdm(midi_files):
        try:
            out=clipFile(os.path.join(data_dir, midi_file),mode=mode)
        except:
            print("-----------")
            print(midi_file)
            print("-----------")

    return(out)
