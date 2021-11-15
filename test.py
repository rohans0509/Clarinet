from midi2audio import FluidSynth
import os

fs = FluidSynth()

for file in os.listdir("Midi"):
    fs.midi_to_audio(f"Midi/{file}", f"Wav/{file.split('.')[0]}.wav")
