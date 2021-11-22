from miditoolkit.midi.containers import Instrument
from miditoolkit.midi.parser import MidiFile
import numpy as np
import os
from tqdm import tqdm
from Clarinet.preprocessing.clipper import condition, clip

time_for_doc = 20
offset_for_doc = 0
time_for_query = 5
offset_for_query = np.random.randint(1, 14)


path = 'Data/Midi/2018/'

# loop through all files in folder Data/Midi/2018
for file in tqdm(os.listdir('Data/Midi/2018')):
    clipped = clip(path + file, 'doc')
    clipped.dump('Data/Midi/2018_clipped/' + file)
