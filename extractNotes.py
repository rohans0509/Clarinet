import json
import miditoolkit
import os
from tqdm import tqdm

path = "Data/2018"
files = os.listdir(path)

fname_to_notes = {}

for fname in tqdm(files):
    mid_in = miditoolkit.midi.parser.MidiFile(os.path.join(path, fname))
    notes = mid_in.instruments[0].notes
    notes = sorted(notes, key=lambda x: x.start)
    lis = []  # (pitch,start,end,velocity)
    for e in notes:
        lis.append([e.pitch, e.start, e.end, e.velocity])
    fname_to_notes[fname] = lis

with open(path+'.json', 'w') as f:
    json.dump(fname_to_notes, f)
