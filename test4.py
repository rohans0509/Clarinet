from Clarinet.evaluation import *
from tqdm import tqdm

path = "Data/Json/Consolidated"
ext = "notes.json"

iters = [
    ["_query_modified/", "_modified/", "text", "modified", False],
]

for tup in tqdm(iters):
    evaluate(path+tup[0]+ext, path+tup[1]+ext, tup[2], tup[3], tup[4])
