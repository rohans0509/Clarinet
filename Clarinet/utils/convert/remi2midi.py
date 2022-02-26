import argparse
import numpy as np
import pickle
import miditoolkit

# parameters for input
DEFAULT_VELOCITY_BINS = np.linspace(0, 128, 32+1, dtype=np.int)
DEFAULT_FRACTION = 16
DEFAULT_DURATION_BINS = np.arange(60, 3841, 60, dtype=int)
DEFAULT_TEMPO_INTERVALS = [range(30, 90), range(90, 150), range(150, 210)]

# parameters for output
DEFAULT_RESOLUTION = 480


# define "Event" for event storage
class Event(object):
    def __init__(self, name, time, value, text):
        self.name = name
        self.time = time
        self.value = value
        self.text = text

    def __repr__(self):
        return 'Event(name={}, time={}, value={}, text={})'.format(
            self.name, self.time, self.value, self.text)

def word_to_event(words, word2event):
    events = []
    for word in words:
        event_name, event_value = word2event.get(word).split('_')
        events.append(Event(event_name, None, event_value, None))
    return events

def write_midi(words, class_arr, word2event, output_path, prompt_path=None):
    events = word_to_event(words, word2event)
    # get downbeat and note (no time)
    temp_notes = []
    temp_chords = []
    temp_tempos = []
    for i in range(len(events)-3):
        if events[i].name == 'Bar' and i > 0:
            temp_notes.append('Bar')
            temp_chords.append('Bar')
            temp_tempos.append('Bar')
        # ignore Note Type
        elif events[i].name == 'Position' and events[i+1].name == 'Note Velocity' and events[i+2].name == 'Note On' and events[i+3].name == 'Note Duration':
            # start time and end time from position
            position = int(events[i].value.split('/')[0]) - 1
            # velocity
            index = int(events[i+1].value)
            velocity = int(DEFAULT_VELOCITY_BINS[index])
            # pitch
            pitch = int(events[i+2].value)
            # duration
            index = int(events[i+3].value)
            duration = DEFAULT_DURATION_BINS[index]
            # type
            type = class_arr[i+2]
            # adding
            temp_notes.append([position, velocity, pitch, duration, type])

        elif events[i].name == 'Position' and events[i+1].name == 'Chord':
            position = int(events[i].value.split('/')[0]) - 1
            temp_chords.append([position, events[i+1].value])

        elif events[i].name == 'Position' and \
            events[i+1].name == 'Tempo Class' and \
            events[i+2].name == 'Tempo Value':
            position = int(events[i].value.split('/')[0]) - 1
            if events[i+1].value == 'slow':
                tempo = DEFAULT_TEMPO_INTERVALS[0].start + int(events[i+2].value)
            elif events[i+1].value == 'mid':
                tempo = DEFAULT_TEMPO_INTERVALS[1].start + int(events[i+2].value)
            elif events[i+1].value == 'fast':
                tempo = DEFAULT_TEMPO_INTERVALS[2].start + int(events[i+2].value)
            temp_tempos.append([position, tempo])

    # get specific time for notes
    ticks_per_beat = DEFAULT_RESOLUTION
    ticks_per_bar = DEFAULT_RESOLUTION * 4 # assume 4/4
    melody, piano = [], []
    current_bar = 0
    for note in temp_notes:
        if note == 'Bar':
            current_bar += 1
        else:
            position, velocity, pitch, duration, type = note
            # position (start time)
            current_bar_st = current_bar * ticks_per_bar
            current_bar_et = (current_bar + 1) * ticks_per_bar
            flags = np.linspace(current_bar_st, current_bar_et, DEFAULT_FRACTION, endpoint=False, dtype=int)
            st = flags[position]
            # duration (end time)
            et = st + duration
            if type == 1 or type == 2:      #NOTE: let class 1 (melody) & 2 (bridge) be defined as melody
                melody.append(miditoolkit.Note(velocity, pitch, st, et))
            elif type == 3:
                piano.append(miditoolkit.Note(velocity, pitch, st, et))
    # get specific time for chords
    if len(temp_chords) > 0:
        chords = []
        current_bar = 0
        for chord in temp_chords:
            if chord == 'Bar':
                current_bar += 1
            else:
                position, value = chord
                # position (start time)
                current_bar_st = current_bar * ticks_per_bar
                current_bar_et = (current_bar + 1) * ticks_per_bar
                flags = np.linspace(current_bar_st, current_bar_et, DEFAULT_FRACTION, endpoint=False, dtype=int)
                st = flags[position]
                chords.append([st, value])

    # get specific time for tempos
    tempos = []
    current_bar = 0
    for tempo in temp_tempos:
        if tempo == 'Bar':
            current_bar += 1
        else:
            position, value = tempo
            # position (start time)
            current_bar_st = current_bar * ticks_per_bar
            current_bar_et = (current_bar + 1) * ticks_per_bar
            flags = np.linspace(current_bar_st, current_bar_et, DEFAULT_FRACTION, endpoint=False, dtype=int)
            st = flags[position]
            tempos.append([int(st), value])
    # write
    if prompt_path:
        midi = miditoolkit.midi.parser.MidiFile(prompt_path)
        last_time = DEFAULT_RESOLUTION * 4 * 4
        # note shift
        for note in melody:
            note.start += last_time
            note.end += last_time
        midi.instruments[0].notes.extend(melody)
        # tempo changes
        temp_tempos = []
        for tempo in midi.tempo_changes:
            if tempo.time < DEFAULT_RESOLUTION*4*4:
                temp_tempos.append(tempo)
            else:
                break
        for st, bpm in tempos:
            st += last_time
            temp_tempos.append(miditoolkit.midi.containers.TempoChange(bpm, st))
        midi.tempo_changes = temp_tempos
        # write chord into marker
        if len(temp_chords) > 0:
            for c in chords:
                midi.markers.append(
                    miditoolkit.midi.containers.Marker(text=c[1], time=c[0]+last_time))
    else:
        midi = miditoolkit.midi.parser.MidiFile()
        midi.ticks_per_beat = DEFAULT_RESOLUTION
        # write instrument
        inst = miditoolkit.midi.containers.Instrument(0, is_drum=False)
        inst.notes = melody 
        midi.instruments.append(inst)
        # write tempo
        tempo_changes = []
        for st, bpm in tempos:
            tempo_changes.append(miditoolkit.midi.containers.TempoChange(bpm, st))
        midi.tempo_changes = tempo_changes
        # write chord into marker
        if len(temp_chords) > 0:
            for c in chords:
                midi.markers.append(
                    miditoolkit.midi.containers.Marker(text=c[1], time=c[0]))
    # write
    # print(f'Dump midi to {output_path}...')
    midi.dump(output_path)


def remi2midi(input_file,predicted_file,dictionary_file,output_file=""):
    if output_file == "":
        output_file=f"{input_file.split('/')[-1].split('.')[0]}.mid"
    remi, pred = np.load(input_file), np.load(predicted_file)
    remi = remi.reshape((-1))
    _, word2event = pickle.load(open(dictionary_file,'rb'))
    write_midi(remi, pred, word2event, output_file, prompt_path=None)
    return