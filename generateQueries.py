import miditoolkit
import os
import random
from tqdm import tqdm
random.seed(42)

NUM_NOTES = 15

def genQuery(fname):
    mido_obj = miditoolkit.midi.parser.MidiFile(fname)
    notes = mido_obj.instruments[0].notes
    notes = [note for note in notes if note.start < note.end]
    notes = sorted(notes,key=lambda note: note.start)
    query_notes = []
    idx = random.randint(0,len(notes)-NUM_NOTES-1)
    query_notes = notes[idx:idx+NUM_NOTES]

    delta = query_notes[0].start
    for note in query_notes:
        note.start -= delta
        note.end -= delta

    query_notes = sorted(query_notes,key=lambda note: note.end)
    
    new_mido_obj = miditoolkit.midi.parser.MidiFile()
    new_mido_obj.ticks_per_beat = mido_obj.ticks_per_beat
    new_mido_obj.instruments.append(miditoolkit.midi.parser.Instrument(0))
    new_mido_obj.instruments[0].notes = query_notes
    return new_mido_obj


def genQueryFromFolder(input,output):
    for fname in tqdm(os.listdir(input)):
        # check if fname ends with .mid
        if fname.endswith(".mid"):                
            mido_obj = genQuery(os.path.join(input,fname))
            mido_obj.dump(os.path.join(output,fname.replace(".mid","_query.mid")))