from .transpose import transpose,getKey

from .getBPM import getBPM
def preprocess(midi_filename):
    print(f"Preprocessing {midi_filename}")
    return(transpose(midi_filename))
