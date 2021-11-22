from miditoolkit.midi.containers import Instrument
from miditoolkit.midi.parser import MidiFile
import numpy as np
import os
from tqdm import tqdm
from Clarinet.preprocessing.clipper import condition, clip


path = 'Data/Midi/2018/'

# loop through all files in folder Data/Midi/2018
for file in tqdm(os.listdir('Data/Midi/2018')):
    clipped = clip(path + file, 'query')
    clipped.dump('Data/Midi/2018_queries/' + file.split('.')[0] + '_query.mid')
