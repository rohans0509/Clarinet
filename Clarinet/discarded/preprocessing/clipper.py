from miditoolkit.midi.containers import Instrument
from miditoolkit.midi.parser import MidiFile
import numpy as np

time_for_doc = 20
offset_for_doc = 0
time_for_query = 5
offset_for_query = np.random.rand() * 14

def condition(note, ticks, method = 'doc', offset = 0):
    if method == 'doc':
        if note.start <= ticks*(time_for_doc+offset_for_doc+offset) and note.start >= (offset_for_doc+offset)*ticks:
            note.end = round(min(note.end,ticks*(time_for_doc+offset_for_doc+offset))) - round((offset+offset_for_doc)*ticks)
            note.start = note.start - round((offset+offset_for_doc)*ticks)
            return True
        return False
    elif method == 'query':
        if note.start <= ticks*(time_for_query+offset_for_query+offset) and note.start >= (offset+offset_for_query)*ticks:
            note.end = round(min(note.end, ticks*(time_for_query+offset_for_query+offset))) - round((offset+offset_for_query)*ticks)
            note.start = note.start - round((offset+offset_for_query)*ticks)
            return True
        return False

def clip(filename, mode = 'doc'):
    midi = MidiFile(filename)
    notes = sorted(midi.instruments[0].notes, key = lambda x: x.start)
    ticks = 1/midi.get_tick_to_time_mapping()[1]
    if mode == 'doc':
        final_notes = [note for note in notes[:-1] if condition(note, ticks = ticks, method = mode)]
        end = notes[-1].end
        if condition(notes[-1], ticks, mode):
            notes[-1].end = end - round((offset_for_doc)*ticks)
            final_notes.append(notes[-1])
    elif mode == 'query':
        final_notes = [note for note in notes[:-1] if condition(note, ticks = ticks, method = mode)]
        end = notes[-1].end
        if condition(notes[-1], ticks, mode):
            notes[-1].end = end  - round((offset_for_query)*ticks)
            final_notes.append(notes[-1])
    starter = final_notes[0].start
    for note in final_notes:
        note.start -= starter
        note.end -= starter
    midi_melody = MidiFile()
    midi_melody.markers = midi.markers
    midi_melody.ticks_per_beat = midi.ticks_per_beat
    midi_melody.tempo_changes = midi.tempo_changes
    midi_melody.lyrics = midi.lyrics
    midi_melody.key_signature_changes = midi.key_signature_changes
    midi_melody.time_signature_changes = midi.time_signature_changes
    piano_track = Instrument(0, is_drum=False, name='piano')
    piano_track.notes = final_notes
    midi_melody.instruments = [piano_track]
    return midi_melody