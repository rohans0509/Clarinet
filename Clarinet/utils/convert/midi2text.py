import miditoolkit
def midi2text(filename_or_midObj,channel=0,num_notes=-1): # Takes input midi filename or midobj, outputs text representation of it
    try:
        filename=filename_or_midObj
        mid_in = miditoolkit.midi.parser.MidiFile(filename)
    except:
        midObj=filename_or_midObj
        mid_in = midObj
    
    notes = mid_in.instruments[channel].notes
    notes = sorted(notes, key=lambda x: x.start)
    rep=[note.pitch for note in notes]
    


    pitch_map = {
    12: "C",
    13: "C#",
    14: "D",
    15: "D#",
    16: "E",
    17: "F",
    18: "F#",
    19: "G",
    20: "G#",
    21: "A",
    22: "A#",
    23: "B"
    }
    if num_notes==-1:
        num_notes=len(notes)
    out=[]
    for pitch in rep[:num_notes+1]:
        num = pitch % 12
        out.append(pitch_map[num + 12])

    return "".join(out)