import json
import numpy as np
import os

bad_queries = ['MIDI-Unprocessed_Schubert7-9_MID--AUDIO_11_R2_2018_wav_melody.mid',
               'ORIG-MIDI_03_7_10_13_Group_MID--AUDIO_18_R3_2013_wav--3_melody.mid'
               ]


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


if __name__ == '__main__':
    results = {}
    files = os.listdir(os.getcwd())
    for f in files:
        if f.endswith('.json'):
            with open(f) as json_file:
                data = json.load(json_file)
            for q in bad_queries:
                del data[q]
            recall1 = getRecall(1)
            recall3 = getRecall(3)
            recall5 = getRecall(5)
            recall10 = getRecall(10)
            mean_rank = getMeanRank()
            norm_sim = getNormSim()
            margin = getMargin()
            avg_confidence = getAvgConfidence()
            results[f] = {
                'recall1': recall1,
                'recall3': recall3,
                'recall5': recall5,
                'recall10': recall10,
                'mean_rank': mean_rank,
                'norm_sim': norm_sim,
                'margin': margin,
                'avg_confidence': avg_confidence
            }

    with open('results.json', 'w') as outfile:
        json.dump(results, outfile)
