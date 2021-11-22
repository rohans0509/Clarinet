from .transpose import transpose

def preprocess(midi_filename):
    print(f"Preprocessing {midi_filename}")
    return(transpose(midi_filename))