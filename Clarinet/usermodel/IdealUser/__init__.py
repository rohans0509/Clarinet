import miditoolkit

'''
==============
USE FUNCTION
==============
'''
def use(midi_file,*args,**kwargs):
    channel=kwargs["channel"]
    mido_obj = miditoolkit.midi.parser.MidiFile(midi_file)
    return mido_obj