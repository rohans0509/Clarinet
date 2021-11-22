import json
import miditoolkit
import os
from tqdm import tqdm


def extractNotes(path):

    files = os.listdir(path)

    fname_to_notes = {}

    print("Extracting notes...")
    for fname in tqdm(files):
        mid_in = miditoolkit.midi.parser.MidiFile(os.path.join(path, fname))
        notes = mid_in.instruments[0].notes
        notes = sorted(notes, key=lambda x: x.start)
        lis = []  # (pitch,start,end,velocity)
        for e in notes:
            lis.append([e.pitch, e.start, e.end, e.velocity])
        fname_to_notes[fname] = lis

    folder_name = path.split('/')[-1]

    output_dir = "Data/Json"

    output_dir = f"{output_dir}/{folder_name}"

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    filename = f"{output_dir}/melody_notes.json"

    with open(filename, 'w') as f:
        json.dump(fname_to_notes, f)


extractNotes("Data/Melody/2018_processed")

