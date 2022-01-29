from typing import Dict
from Clarinet.search import similarity
from Clarinet.evaluation import analyse
from os import listdir,path
import json
from tqdm import tqdm
import miditoolkit


query_dir="Data/Queries"
collection_dir="Data/Original Collection"
output_dir="Results"

def computeScores(query_dir,collection_dir,stride_length=0,similarity_type="text",output_dir="Results"):
    queries=midiFolderToDict(query_dir) 
    query_filenames=queries.keys()

    collection=midiFolderToDict(collection_dir)
    collection_filenames=collection.keys()

    scores={} # Dict of form {query_num : {collection_num : sim}}

    for i in tqdm(range(len(query_filenames))):
        query_filename=query_filenames[i]
        query_text=queries[query_filename]

        query_scores={} # Dict of form {collection_num : sim}

        for j in range(len(collection_filenames)):
            collection_filename=collection_filenames[j]
            collection_text=collection[collection_filename]

            sim=similarity(query_text,collection_text,stride_length=stride_length,similarity_type=similarity_type) # Compute similarity

            query_scores[j]=sim

        scores[i]=query_scores

    with open(f"{output_dir}/scores.json", 'w') as fp:
        json.dump(scores, fp)

    with open(f"{output_dir}/querymap.json", 'w') as fp:
        querymap={i:query_filenames[i] for i in range(len(query_filenames))} 
        json.dump(querymap, fp)
    
    with open(f"{output_dir}/collectionmap.json", 'w') as fp:
        collectionmap={i:collection_filenames[i] for i in range(len(collection_filenames))} 
        json.dump(collectionmap, fp)

    # Evaluation Complete, now generate Analysis
    df=analyse(f"{output_dir}/scores.json")
    df.to_csv(f"{output_dir}/analysis.csv")

def midiFileToText(filename,channel=0): # Takes input midi filename, outputs text representation of it
    mid_in = miditoolkit.midi.parser.MidiFile(filename)
    notes = mid_in.instruments[channel].notes
    notes = sorted(notes, key=lambda x: x.start)
    rep=[note.pitch for note in notes]


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

    out=[]
    for pitch in rep:
        num = pitch % 12
        out.append(pitch_map[num + 12])
    return "".join(out)

def midiFolderToDict(folder:str)->Dict: # Returns a dict of form {filelocation:text_representation}
    file_locations=[f"{folder}/{filename}" for filename in listdir(folder)]
    
    output_dict={}
    for file in tqdm(file_locations):
        if file.endswith(".mid"):
            output_dict[file]=midiFileToText(file)
    return(output_dict)

computeScores(query_dir,collection_dir,stride_length=0,similarity_type="text",output_dir=output_dir)