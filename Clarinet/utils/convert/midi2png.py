from fileinput import filename
from miditoolkit.midi import parser as mid_parser
from miditoolkit.pianoroll import parser as pr_parser
import pypianoroll
from pypianoroll import Track
from matplotlib import pyplot as plt
import sys
import os

def note2roll(path):
    obj = mid_parser.MidiFile(path)
    melody = obj.instruments[0].notes
    bridge = obj.instruments[1].notes
    piano = obj.instruments[2].notes

    m_roll = pr_parser.notes2pianoroll(melody)
    b_roll = pr_parser.notes2pianoroll(bridge)
    p_roll = pr_parser.notes2pianoroll(piano)

    return m_roll, b_roll, p_roll

def midi2png(midi_file,output_dir=""):
    
    m, b, p = note2roll(midi_file)
    m_track = Track(name='melody', program=0, is_drum=False, pianoroll=m)
    b_track = Track(name='bridge', program=0, is_drum=False, pianoroll=b)
    p_track = Track(name='piano', program=0, is_drum=False, pianoroll=p)

    if output_dir=="":
        # Get absolute path of parent folder of midi_file
        output_dir = "/".join(midi_file.split("/")[:-1]).replace("Midi","Images")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    fname = midi_file.split('/')[-1].replace('.mid','')
    filename = f"{output_dir}/{fname}"

    fig = m_track.plot()
    plt.savefig(filename+'_melody.png')
    fig = b_track.plot()
    plt.savefig(filename+'_bridge.png')
    fig = p_track.plot()
    plt.savefig(filename+'_piano.png')
    
    
def note2roll(path):
    obj = mid_parser.MidiFile(path)
    melody = obj.instruments[0].notes
    bridge = obj.instruments[1].notes
    piano = obj.instruments[2].notes

    m_roll = pr_parser.notes2pianoroll(melody)
    b_roll = pr_parser.notes2pianoroll(bridge)
    p_roll = pr_parser.notes2pianoroll(piano)

    return m_roll, b_roll, p_roll

def main():
    path = sys.argv[1]
    

    