import miditoolkit
from Clarinet.usermodel.NoisyUser.NoisyUser import NoisyUser

'''
==============
USE FUNCTION
==============
'''
def use(midi_file,channel=-1,pitch=0,extra=0,delete=0,velocity=0,length=0):
    mido_obj = miditoolkit.midi.parser.MidiFile(midi_file)
    user = NoisyUser(mido_obj)
    if channel == -1:
        user.addNoiseToFull(pitch,extra,delete,velocity,length)
    else:
        user.addNoiseToChannel(0,pitch,extra,delete,velocity,length)
    output = user.mido_obj
    return output

