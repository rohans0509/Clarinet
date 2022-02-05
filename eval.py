from evaluate import computeScores
import json
from tqdm import tqdm
import os
from os import listdir
from evaluate import analyse
# Noise Experiment 

# Query Folders to be named as pitch_extranotes_deleted

collection_dir="Text/Original Collection"

query_folders_location="Text/Noisy Queries"

for query_dir in tqdm(listdir(query_folders_location)):
    output_dir=f"Results/NoisyResults/{query_dir}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    query_dir=f"{query_folders_location}/{query_dir}"
    computeScores(query_dir,collection_dir,num_queries=-1,num_collection=-1,similarity_type="text",output_dir=output_dir,stride_length=4)