from AudioProcessor import AudioProcessor

ap = AudioProcessor()

filename = "Data/happy_birthday.mp3"
mode = "music-piano-v2"
output_dir = "Midi"


# Convert File to Midi
# midi_filename=ap.transcribe(file=filename, mode=mode, output_dir=output_dir)
midi_filename="Midi/happy_birthday.mid"

# Save wav form of Midi
ap.toWav(midi_filename)

# Visualise Midi
ap.visualise(midi_filename)

# Extract Melody from Midi and Save to Midi

melody_midi_filename=ap.extractMelody(midi_filename)

# Save wav form of Melody
ap.toWav(melody_midi_filename)

# Visualise melody
ap.visualise(melody_midi_filename)





