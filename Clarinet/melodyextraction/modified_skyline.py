import copy
from miditoolkit.midi.containers import Instrument
from miditoolkit.midi.parser import MidiFile
import heapq
import numpy as np
_method = 'pitch'

class MyHeap(object):
    def __init__(self, initial=None, method = 'start'):
        self.index = 0
        self.method = method
        self.increaser = 0
        if initial:
            if method == 'start':
                self._data = [((item).start, i, item) for i, item in enumerate(initial)]
            elif method == 'end':
                self._data = [(-(item).end, i, item) for i, item in enumerate(initial)]
            elif self.method == 'criteria':
                self._data = [(-criteria(item, method=_method), i, item) for i, item in enumerate(initial)]
            self.index = len(self._data)
            heapq.heapify(self._data)
        else:
            self._data = []

    def push(self, item):
        if self.method == 'start':
            heapq.heappush(self._data, (item.start, self.increaser, item))
        elif self.method == 'end':
            heapq.heappush(self._data, (-item.end, self.increaser, item))
        elif self.method == 'criteria':
            heapq.heappush(self._data, (-criteria(item, method=_method), self.increaser, item))
        self.index += 1
        self.increaser +=1

    def pop(self):
        self.index -= 1
        return heapq.heappop(self._data)[2]
    
    def listit(self):
        return np.array(self._data)[:,2]
        

def criteria(note, method = 'pitch'):
    if method=='pitch':
        return note.pitch
    elif method =='velocity':
        return note.velocity
    elif method=='pitchvel':
        return note.pitch*note.velocity


def mskyline(filename, instr_idx=0):
    '''
    Input:
        filename: location of MIDI file
        instr_idx: index of instrument to extract melody from (piano is 0)

    Return:
        midi_melody: MidiFile
    '''
    midi = MidiFile(filename)
    notes = sorted(midi.instruments[instr_idx].notes, key = lambda x: x.start)
    skyline_notes = MyHeap()
    finished_notes = []
    for si, note in enumerate(notes):
        if note in finished_notes:
            continue
        finished_notes.append(note)
        start_t = note.start
        notes_at_t = [note]
        most_important = criteria(note, _method)
        importances = [most_important]
        ind = 0
        if si != len(notes)-1:
            while start_t==notes[si+1].start:
                notes_at_t.append(notes[si+1])
                finished_notes.append(notes[si+1])
                importance = criteria(notes[si+1], _method)
                importances.append(importance)
                if most_important<importances[-1]:
                    ind = len(importances)-1
                    most_important = importances[-1]
                si += 1
                if si == len(notes)-1:
                    break
        n = copy.deepcopy(notes_at_t[ind])
        skyline_notes.push(n)
    final_notes = [skyline_notes.listit()[0]]
    buffer_note = MyHeap(method='criteria')
    for note in skyline_notes.listit()[1:]:
        if final_notes[-1].end <= note.start:
            tempnotelist = [note]
            maxstart = note.start
            minend = final_notes[-1].end
            while buffer_note.index > 0:
                tempnote = copy.deepcopy(buffer_note.pop())
                tempnote.end = min(tempnote.end,maxstart)
                tempnote.start = max(tempnote.start,minend)
                minend = tempnote.end
                maxstart = tempnote.start
                if tempnote.start<tempnote.end:
                    tempnotelist.append(tempnote)
                if minend<maxstart:
                    break
            tempnotelist.reverse()
            final_notes.extend(tempnotelist)
        elif criteria(final_notes[-1], _method) < criteria(note, _method):
            if final_notes[-1].end > note.end:
                tempnote = copy.deepcopy(final_notes[-1])
                tempnote.start = note.end
                buffer_note.push(copy.deepcopy(tempnote))
            final_notes[-1].end = note.start
            final_notes.append(note)
        elif final_notes[-1].end < note.end:
            note.start = final_notes[-1].end
            buffer_note.push(copy.deepcopy(note))
            
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
'''
midi_final = mskyline('test_clip.mid')
midi_final.dump('test_melody.mid')
ed = 0
for x in midi_final.instruments[0].notes:
    print(x)
    if x.start<ed:
        print(x)
        print('ew')
    ed=x.end
'''