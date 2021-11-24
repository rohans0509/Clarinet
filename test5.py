from Clarinet.evaluation import *
from tqdm import tqdm

path = "Data/Json/Consolidated"
ext = "notes.json"

iters = [
    ["_query_processed_modified/", "_processed_modified/", "text", "modified", True],
]

for tup in tqdm(iters):
    evaluate(path+tup[0]+ext, path+tup[1]+ext, tup[2], tup[3], tup[4])
