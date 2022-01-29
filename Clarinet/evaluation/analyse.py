import json
import numpy as np
import os
import pandas as pd

bad_queries = ['MIDI-Unprocessed_Schubert7-9_MID--AUDIO_11_R2_2018_wav_melody.mid',
               'ORIG-MIDI_03_7_10_13_Group_MID--AUDIO_18_R3_2013_wav--3_melody.mid'
               ]


def getRecall(data,posn):
    score = 0
    for key, value in data.items():
        target = key.replace("_query", "")
        items = [filename for filename in value.keys()]
        rank = items.index(target)+1
        if rank <= posn:
            score += 1
    return score/len(data)


def getMeanRank(data):
    average_rank = 0
    for key, value in data.items():
        target = key.replace("_query", "")
        items = [filename for filename in value.keys()]
        rank = items.index(target)+1
        average_rank += rank
    average_rank /= len(data)
    return average_rank


def getNormSim(data):
    average_score = 0
    for key, value in data.items():
        target = key.replace("_query", "")
        items = [filename for filename in value.keys()]
        topsim = value[items[0]]
        sim = value[target]
        average_score += sim/topsim
    average_score /= len(data)
    return average_score


def getMargin(data,consider_only_top=False):
    average_score = 0
    total_len = len(data)
    for key, value in data.items():
        target = key.replace("_query", "")
        items = [filename for filename in value.keys()]
        idx = items.index(target)
        if consider_only_top and idx == 0:
            sim1 = value[items[idx]]
            sim2 = value[items[idx+1]]
            topsim = value[items[0]]
            average_score += (sim1-sim2)/topsim/(idx+1)
        elif consider_only_top == False:
            sim1 = value[items[idx]]
            sim2 = value[items[idx+1]]
            topsim = value[items[0]]
            average_score += (sim1-sim2)/topsim/(idx+1)
        else:
            total_len -= 1
    average_score /= total_len
    return average_score


def getAvgConfidence(data):
    average_score = 0
    for key, value in data.items():
        target = key.replace("_query", "")
        items = [filename for filename in value.keys()]
        sim = value[target]
        average_score += sim
    average_score /= len(data)
    return average_score


def getMRR(data):
    average = 0
    for key, value in data.items():
        target = key.replace("_query", "")
        items = [filename for filename in value.keys()]
        rank = items.index(target)+1
        average += 1/rank
    average /= len(data)
    return average



def analyse(file):
    with open(file) as json_file:
        data = json.load(json_file)
    for q in bad_queries:
        del data[q]
    recall1 = getRecall(data,1)
    recall3 = getRecall(data,3)
    recall5 = getRecall(data,5)
    recall10 = getRecall(data,10)
    mean_rank = getMeanRank(data)
    norm_sim = getNormSim(data)
    margin = getMargin(data)
    avg_confidence = getAvgConfidence(data)
    mrr = getMRR(data)


    results= {
        'Recall@1': recall1,
        'Recall@3': recall3,
        'Recall@5': recall5,
        'Recall@10': recall10,
        'Mean Rank': mean_rank,
        'Normalised Similarity': norm_sim,
        'Margin of Error': margin,
        'Average Confidence': avg_confidence,
        'MRR': mrr
    }

    df=pd.DataFrame(results.items(), columns=["Metric","Value"])

    
    return(df)

