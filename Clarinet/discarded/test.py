from Clarinet.evaluation import *
from tqdm import tqdm

path = "Data/Json/Consolidated"
ext = "notes.json"

iters = [
    ["_query/", "/", "time", "skyline", False],
    ["_query_processed/", "_processed/", "time", "skyline", True],
    ["_query_modified/", "_modified/", "time", "modified", False],
    ["_query_processed_modified/", "_processed_modified/", "time", "modified", True],
    ["_query/", "/", "text", "skyline", False],
    ["_query_processed/", "_processed/", "text", "skyline", True],
    ["_query_modified/", "_modified/", "text", "modified", False],
    ["_query_processed_modified/", "_processed_modified/", "text", "modified", True],
]

for tup in tqdm(iters):
    evaluate(path+tup[0]+ext, path+tup[1]+ext, tup[2], tup[3], tup[4])
