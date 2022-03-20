from Clarinet.melodyextraction.noBERT.song2graph import song2graph
from Clarinet.utils.convert import midi2text
from Clarinet.search import similarity
import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import miditoolkit
from Clarinet.melodyextraction.noBERT.quantize import quantize
import math

def makeNonMelodicTransitionMat(midi_folder):
    mat = np.zeros((131,131))
    for f in tqdm(midi_folder):
        mid_in=miditoolkit.midi.parser.MidiFile(f)    
        for channel in range(0,3):
            notes = mid_in.instruments[channel].notes
            qn = quantize(notes, planck=1)
            for i in range(len(qn)-1):
                box1 = qn[i]
                box2 = qn[i+1]
                for i in range(10):
                    note1 = box1[np.random.randint(len(box1))]
                    note2 = box2[np.random.randint(len(box2))]
                    p1 = note1[0]
                    p2 = note2[0]
                    mat[p1][p2] += 1
    
    for j in range(131):
        mat[0][j] = j
        mat[j][0] = j
    for j in range(131):
        mat[130][j] = j
        mat[j][130] = j
    
    for i in range(131):
        if np.sum(mat[i]) != 0:
            mat[i] = mat[i]/np.sum(mat[i])
    return mat
    

def dumpNonMelodic(midi_folder,output_folder,num_files=5):
    files = [midi_folder+"/"+f for f in os.listdir(midi_folder) if f.endswith(".mid")]
    files = files[:num_files]
    mat = makeNonMelodicTransitionMat(files)
    np.save(output_folder+"/nonmelodic.npy",mat)

def dumpWeight(numpy_folder):
    melodic = np.load(numpy_folder+"/melodic.npy")
    nonmelodic = np.load(numpy_folder+"/nonmelodic.npy")
    mat = np.zeros((131,131))
    for i in range(131):
        for j in range(131):
            if nonmelodic[i][j] != 0:
                mat[i][j] = melodic[i][j]/nonmelodic[i][j]
            else:
                mat[i][j] = melodic[i][j] * pow(10,5)
            if mat[i][j] == 0:
                mat[i][j] = pow(10,-5)
            mat[i][j] = -1 * math.log(mat[i][j])
    np.save(numpy_folder+"/weight.npy",mat)

pitch_map = {
    12: "C",
    13: "C#",
    14: "D",
    15: "D#",
    16: "E",
    17: "F",
    18: "F#",
    19: "G",
    20: "G#",
    21: "A",
    22: "A#",
    23: "B"
    }

def get_pitch_name(pitch):
    num = pitch % 12
    return pitch_map[num + 12]


def evaluate(midi_file,weights=None):
    actual=midi2text(midi_file)
    g=song2graph(midi_file,weights)
    melody = g.melody()
    predicted = [get_pitch_name(pitch) for pitch in melody]
    predicted="".join(predicted)

    return(similarity(predicted,actual))

def evaluateFolder(midi_folder,num_files=-1,weights=None):
    files=sorted([f"{midi_folder}/{filename}" for filename in os.listdir(midi_folder)])
    if num_files==-1:
        num_files=len(files)
    df=pd.DataFrame(columns=["Filename","Score"])
    for i in tqdm(range(num_files)):
        file=files[i]
        score=evaluate(file,weights)
        df=df.append({"Filename":file,"Score":score},ignore_index=True)
    return(df)


if __name__ == "__main__":
    num_files=900

    # melody
    weights = np.load("Data/Numpy/noBERT/melodic.npy")

    df=evaluateFolder("Data/MIDI/Collection/Original Collection",num_files,weights)
    df.to_csv("Results/Melody/results_p.csv",index=False)

    # weights
    dumpNonMelodic("Data/MIDI/Collection/Original Collection", "Data/Numpy/noBERT",num_files=-1)
    dumpWeight("Data/Numpy/noBERT")
    weights = np.load("Data/Numpy/noBERT/weight.npy")

    df=evaluateFolder("Data/MIDI/Collection/Original Collection",num_files,weights)
    df.to_csv("Results/Melody/results_w.csv",index=False)