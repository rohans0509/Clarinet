from midi2audio import FluidSynth

fs = FluidSynth()
fs.midi_to_audio('Midi/test.mid', 'test.wav')
fs.midi_to_audio('Midi/test_extract.mid', 'test_extract.wav')
fs.midi_to_audio('Midi/test_melody.mid', 'test_melody.wav')
