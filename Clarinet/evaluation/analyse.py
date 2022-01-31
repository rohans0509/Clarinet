import json
from pickle import TRUE
import numpy as np
import os
import pandas as pd

bad_queries = []


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



def analyse(output_dir):
    scores_location=f"{output_dir}/scores.json"
    collectionmap_location=f"{output_dir}/collectionmap.json"
    querymap_location=f"{output_dir}/querymap.json"

    with open(scores_location) as json_file:
        scores = json.load(json_file)

    with open(collectionmap_location) as json_file:
        collection = json.load(json_file)

    with open(querymap_location) as json_file:
        queries = json.load(json_file)

    for q in bad_queries:
        del scores[q]

    sorted_scores={}

    for key,value in scores.items():
        sorted_value={collection[k].split("/")[-1]: v for k, v in sorted(value.items(), key=lambda item: item[1],reverse=True)}
        sorted_scores[queries[key].split("/")[-1].replace("_noise", "").replace("_query", "")]=sorted_value
    
    data=sorted_scores

    for key,value in data.items():
        print(key,list(value.values())[0],list(value.values())[1])



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
        'Margin of Discrimination': margin,
        'Average Confidence': avg_confidence,
        'MRR': mrr
    }

    df=pd.DataFrame(results.items(), columns=["Metric","Value"])
    
    df.index+=1
    df.index.names = ['Index']

    
    return(df)