import json
import numpy as np

fname = 'res_text.json'

with open(fname) as json_file:
    data = json.load(json_file)


def getRecall(posn):
    score = 0
    for key, value in data.items():
        target = key.replace("_query", "")
        items = [filename for filename in value.keys()]
        rank = items.index(target)+1
        if rank <= posn:
            score += 1
    return score/len(data)


def getMeanRank():
    average_rank = 0
    for key, value in data.items():
        target = key.replace("_query", "")
        items = [filename for filename in value.keys()]
        rank = items.index(target)+1
        average_rank += rank
    average_rank /= len(data)
    return average_rank


def getNormSim():
    average_score = 0
    for key, value in data.items():
        target = key.replace("_query", "")
        items = [filename for filename in value.keys()]
        topsim = value[items[0]]
        sim = value[target]
        average_score += sim/topsim
    average_score /= len(data)
    return average_score


def getMargin(consider_only_top=False):
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


def getAvgConfidence():
    average_score = 0
    for key, value in data.items():
        target = key.replace("_query", "")
        items = [filename for filename in value.keys()]
        sim = value[target]
        average_score += sim
    average_score /= len(data)
    return average_score
