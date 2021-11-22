from Clarinet.converter.midi2audio import midi2audio
from Clarinet.converter.audio2midi import audio2midi
from  Clarinet.visualiser import visualise
from Clarinet.melodyextraction import extractMelody
from Clarinet.preprocessing import preprocess
from Clarinet.utils import extractMelodyFolder,extractNotes,preprocessFolder

filename = "Data/Audio/Birthday/happy_birthday.wav"
mode = "music-piano-v2"


# Convert File to Midi

# midi_filename=audio2midi(file=filename, mode=mode)

# midi_filename="Data/Midi/Birthday/happy_birthday.mid"

# Preprocess Midi File
# processed_filename=preprocess(midi_filename)

# Extract Melody from Midi and Save to Midi

# melody_midi_filename=extractMelody(processed_filename)


# extractNotes(processed_folder)


# processed_folder=preprocessFolder("Data/Midi/2018")
melody_folder=extractMelodyFolder("Data/Midi/2018_clipped")
