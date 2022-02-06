import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import miditoolkit
import os

def getStats(folder_name,num_notes_dict={},channel=0):
    if num_notes_dict=={}:
        num_notes_dict=numNotes(folder_name,channel)
    df=pd.DataFrame.from_dict(num_notes_dict, orient='index',columns=["Notes"])
    df.index.names = ['Index']
    print(f"Files with >=100 notes={len(df[df['Notes']>=100])}")

    
    
    num_notes=list(num_notes_dict.values())
    mean=int(np.mean(num_notes))
    std=int(np.std(num_notes))
    maximum=np.max(num_notes)
    minimum=np.min(num_notes)
    perc_10=int(np.percentile(num_notes,10))
    perc_25=int(np.percentile(num_notes,25))
    perc_50=int(np.percentile(num_notes,50))
    perc_75=int(np.percentile(num_notes,75))
    
    
    df=pd.DataFrame(columns=["Metric","Value"])
    df.loc[len(df)] = ["Expected",f"{mean}±{std}"]
    df.loc[len(df)] = ["Max",maximum]
    df.loc[len(df)] = ["75%",perc_75]
    df.loc[len(df)] = ["50%",perc_50]
    df.loc[len(df)] = ["25%",perc_25]
    df.loc[len(df)] = ["10%",perc_10]
    df.loc[len(df)] = ["Min",minimum]
    df.index+=1
    df.index.names = ['Index']
    counts, bins, _ = plt.hist(num_notes, bins=30)
    
    return(df)

def numNotes(folder_name,channel=0):
    num_notes_dict={}
    for file in tqdm(os.listdir(folder_name)):
        if file.endswith(".mid"):
            filename=f"{folder_name}/{file}"
            mid_in = miditoolkit.midi.parser.MidiFile(filename)
            notes = mid_in.instruments[channel].notes
            num_notes_dict[file]=len(notes)
    num_notes_dict = dict(sorted(num_notes_dict.items(), key=lambda item: item[1]))
    return(num_notes_dict)
