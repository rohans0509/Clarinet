from Clarinet.evaluation import *
from tqdm import tqdm
import itertools
from multiprocessing.dummy import Pool as ThreadPool 
from functools import partial

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
num_processes=4
pool = ThreadPool(num_processes)
first=[path+tup[0]+ext for tup in iters]
second=[path+tup[1]+ext for tup in iters]
third=[tup[2] for tup in iters]
fourth=[tup[3] for tup in iters]
fifth=[tup[4] for tup in iters]

zipped_input=zip(first,second,third,fourth,fifth)
pool.starmap(evaluate,zipped_input)