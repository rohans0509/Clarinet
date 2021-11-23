import json
import os
import miditoolkit
from tqdm import tqdm
from search.similarity_time import midiEt_to_note_sequence, midiEt_to_note, splitNotes, getStrides
from search.similarity_sankoff import similarity as similarity_sankoff
from search.similarity_text import similarity as similarity_text
from search.similarity_time import similarity as similarity_time


factor = 768

SIM_DICT = {
    "sankoff": similarity_sankoff,
    "text": similarity_text,
    "time": similarity_time
}


def similarity(query, data, similarity_algo="text"):
    sim_method = SIM_DICT[similarity_algo]
    return(sim_method(query, data))


def evaluate(query_json, data_json, output_file="res", similarity_algo="text"):
    with open(data_json, 'r') as f:
        fname_to_notes = json.load(f)
    with open(query_json, 'r') as f:
        query_to_notes = json.load(f)

    res = {}

    for query_name, query_notes in query_to_notes.items():
        fname_to_similarity = {}
        for fname in fname_to_notes:
            sim = 0
            notes = fname_to_notes[fname]

            if similarity_algo == "time":
                notes = splitNotes(notes)
                strides = getStrides(notes, 5*factor)
                for stride in strides:
                    stride_notes = [note[0] for note in stride]
                    note_sequence = midiEt_to_note_sequence(stride_notes)
                    sim = max(sim, similarity(query_notes, note_sequence, similarity_algo))

            elif similarity_algo == "text":
                nn = []
                for n in notes:
                    nn.append(n[0])
                note_sequence = midiEt_to_note_sequence(nn)
                sim = max(sim, similarity(query_notes, note_sequence, similarity_algo))

            elif similarity_algo == "sankoff":
                pass

            fname_to_similarity[fname] = sim
        fname_to_similarity = dict(sorted(fname_to_similarity.items(), key=lambda item: item[1], reverse=True))
        res[query_name] = fname_to_similarity

    if output_file == "res":
        output_file = f"res_{similarity_algo}.json"

    with open(output_file, 'w') as f:
        json.dump(res, f)
