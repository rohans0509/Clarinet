import json
import os
import miditoolkit
from tqdm import tqdm
from Clarinet.search.similarity_time import midiEt_to_note_sequence, midiEt_to_note, splitNotes, getStrides
from Clarinet.search import similarity, Note
import time
import random

factor = 768


def evaluate(query_json, data_json, similarity_algo="text", melody_algo="skyline", processing=False):
    with open(data_json, 'r') as f:
        fname_to_notes = json.load(f)
    with open(query_json, 'r') as f:
        query_to_notes = json.load(f)

    res = {}
    t1 = time.time()
    qnames = list(query_to_notes.keys())
    random.shuffle(qnames)
    qnames = qnames[:40]
    for query_name in tqdm(qnames, leave=False):
        query_notes = query_to_notes[query_name]
        qnotes = [note[0] for note in query_notes]
        query = midiEt_to_note_sequence(qnotes)
        fname_to_similarity = {}
        if similarity_algo == "sankoff":
            qrep = []
            prev_end = 0
            for n in notes:
                if n[1] > prev_end:
                    qrep.append(Note("C", int((n[1]-prev_end)/t), rest=True))
                qrep.append(Note(midiEt_to_note[n[0] % 12 + 12], int((n[2]-n[1])/t), rest=False))
                prev_end = n[2]
        for fname in tqdm(fname_to_notes, leave=False):
            sim = 0
            notes = fname_to_notes[fname]

            if similarity_algo == "time":
                notes = splitNotes(notes)
                strides = getStrides(notes, 5*factor)
                for stride in strides:
                    stride_notes = [note[0] for note in stride]
                    note_sequence = midiEt_to_note_sequence(stride_notes)
                    sim = max(sim, similarity(query, note_sequence, similarity_algo))

            elif similarity_algo == "text":
                nn = []
                for n in notes:
                    nn.append(n[0])
                note_sequence = midiEt_to_note_sequence(nn)
                sim = max(sim, similarity(query, note_sequence, similarity_algo))

            elif similarity_algo == "sankoff":
                #end_time = notes[-1][2]
                #tempo = 120
                #t = end_time/(4*tempo)
                t = 500
                rep = []
                prev_end = 0
                for n in notes:
                    if n[1] > prev_end:
                        rep.append(Note("C", int((n[1]-prev_end)/t), rest=True))
                    rep.append(Note(midiEt_to_note[n[0] % 12 + 12], int((n[2]-n[1])/t), rest=False))
                    prev_end = n[2]
                sim = similarity(qrep, rep, similarity_algo)
            fname_to_similarity[fname] = sim

        fname_to_similarity = dict(sorted(fname_to_similarity.items(), key=lambda item: item[1], reverse=True))
        res[query_name] = fname_to_similarity

    t2 = time.time()

    if processing:
        output_file = f"res_{similarity_algo}_{melody_algo}_processed.json"
    else:
        output_file = f"res_{similarity_algo}_{melody_algo}.json"

    try:
        with open("Results/timeres.json", 'r') as f:
            timedict = json.load(f)
        timedict[output_file] = t2-t1
    except:
        timedict = {}
        timedict[output_file] = t2-t1

    with open("Results/timeres.json", 'w') as f:
        json.dump(timedict, f)

    with open("Results/"+output_file, 'w') as f:
        json.dump(res, f)


if __name__ == "__main__":
    data_file = r"C:\Users\Kshitij Alwadhi\Documents\GitHub\Clarinet\Data\Json\Consolidated\notes.json"
    query_file = r"C:\Users\Kshitij Alwadhi\Documents\GitHub\Clarinet\Data\Json\Consolidated_query\notes.json"

    evaluate(query_file, data_file, similarity_algo="time", melody_algo="skyline", processing=False)
