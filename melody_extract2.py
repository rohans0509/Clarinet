# change for only one instrument
# method of sorting start time of notes

import copy
import miditoolkit
import numpy as np
import mido
import operator
from mido import MidiFile
from miditoolkit.midi.containers import Instrument


def skyline(mido_obj, instr_idx=0):
    '''Melody extraction based on Skyline algorithm
    Based on https://dl.acm.org/doi/10.1145/319463.319470
    Args:
        mido_obj: MidiFile
        instr_idx: index of instrument to extract melody from

    Return:
        new_midi_obj: MidiFile
    '''
    start2note = {}
    for note in mido_obj.instruments[instr_idx].notes:
        start = note.start
        if start in start2note:
            start2note[start].append(note)
        else:
            start2note[start] = [note]
    starts = sorted(list(start2note.keys()))
    skyline_notes = []
    for si, start in enumerate(starts):
        notes = start2note[start]
        pitches = [n.pitch for n in notes]
        note = copy.deepcopy(notes[np.argmax(pitches)])
        if si < len(starts)-1:
            note.end = min(note.end, starts[si+1])  # no space left b/w notes here hence yayyyy
        skyline_notes.append(note)
    new_midi_obj = miditoolkit.midi.parser.MidiFile()
    new_midi_obj.markers = mido_obj.markers
    new_midi_obj.tempo_changes = mido_obj.tempo_changes
    piano_track = Instrument(0, is_drum=False, name='piano')
    piano_track.notes = skyline_notes
    new_midi_obj.instruments = [piano_track]
    return new_midi_obj


filename = 'Midi/test'
mid_in = miditoolkit.midi.parser.MidiFile(filename+'.mid')

mid_out = skyline(mid_in)
mid_out.dump(filename+'_melody.mid')
