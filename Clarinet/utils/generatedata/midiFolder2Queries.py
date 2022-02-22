import miditoolkit
import os
import random
from tqdm import tqdm
from Clarinet.converter import midi2text
random.seed(42)


def genQuery(fname,num_notes=-1,channel=0):
    mido_obj = miditoolkit.midi.parser.MidiFile(fname)
    notes = mido_obj.instruments[channel].notes
    if num_notes==-1:
        num_notes=len(notes)
    notes = [note for note in notes if note.start < note.end]
    notes = sorted(notes,key=lambda note: note.start)
    query_notes = []
    if len(notes) > num_notes:
        idx = random.randint(0,len(notes)-num_notes-1)
        query_notes = notes[idx:idx+num_notes]

        delta = query_notes[0].start
        for note in query_notes:
            note.start -= delta
            note.end -= delta

        query_notes = sorted(query_notes,key=lambda note: note.end)
        
        new_mido_obj = miditoolkit.midi.parser.MidiFile()
        new_mido_obj.ticks_per_beat = mido_obj.ticks_per_beat
        new_mido_obj.instruments.append(miditoolkit.midi.parser.Instrument(0))
        new_mido_obj.instruments[channel].notes = query_notes
        return True, new_mido_obj
    else:
        return False, mido_obj

def midiFolder2QueryText(folder,num_queries=-1,output_folder="Data/Text",num_notes=-1,channel=0):

    # get all files in input folder ending with ".mid"
    mido_files = [fname for fname in os.listdir(folder) if fname.endswith(".mid")]
    files = random.sample(mido_files,num_queries)
    for fname in tqdm(files):
        # check if fname ends with .mid
        if fname.endswith(".mid"):                
            flag, mido_obj = genQuery(os.path.join(folder,fname),num_notes,channel)
            if flag:
                text=midi2text(mido_obj,channel=channel)
                
                output_filename=os.path.join(output_folder,fname.replace(".mid",".txt"))
                with open(output_filename,'w') as f:
                    f.write(text)
            else:
                print(f"{fname} is too short")

def getAvgLen(input):
    total_len = 0
    num_files = 0
    for fname in tqdm(os.listdir(input)):
        if fname.endswith(".mid"):
            mido_obj = miditoolkit.midi.parser.MidiFile(os.path.join(input,fname))
            notes = mido_obj.instruments[0].notes
            notes = [note for note in notes if note.start < note.end]
            total_len += len(notes)
            num_files += 1
    return total_len/num_files