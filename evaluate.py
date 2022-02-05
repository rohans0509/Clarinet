from typing import Dict

from numpy import sort
from Clarinet.search import similarity
from Clarinet.evaluation import analyse
from os import listdir,path
import json
from tqdm import tqdm
import miditoolkit

def computeScores(query_dir,collection_dir,num_queries=-1,num_collection=-1,stride_length=0,similarity_type="text",output_dir="Results"):
    # print("Reading queries....")
    queries=textFolderToDict(query_dir,num_queries) 
    query_filenames=list(queries.keys())

    # print("Reading collection....")
    collection=textFolderToDict(collection_dir,num_collection)
    collection_filenames=list(collection.keys())

    scores={} # Dict of form {query_num : {collection_num : sim}}
    # print("Computing Similarities..")
    for i in range(len(query_filenames)):
        query_filename=query_filenames[i]
        query_text=queries[query_filename]

        query_scores={} # Dict of form {collection_num : sim}

        for j in tqdm(range(len(collection_filenames))):
            collection_filename=collection_filenames[j]
            collection_text=collection[collection_filename]

            sim=similarity(query_text,collection_text,stride_length=stride_length,similarity_type=similarity_type) # Compute similarity

            query_scores[j]=sim

        scores[i]=query_scores

    with open(f"{output_dir}/scores.json", 'w') as fp:
        json.dump(scores, fp)

    with open(f"{output_dir}/querymap.json", 'w') as fp:
        querymap={i:query_filenames[i] for i in range(len(query_filenames))} 
        json.dump(querymap, fp)
    
    with open(f"{output_dir}/collectionmap.json", 'w') as fp:
        collectionmap={i:collection_filenames[i] for i in range(len(collection_filenames))} 
        json.dump(collectionmap, fp)

    # Evaluation Complete, now generate Analysis
    out=list(analyse(f"{output_dir}"))

    best_scores="\n".join(out[0])
    df=out[1]
    df.to_csv(f"{output_dir}/analysis.csv")

    with open(f"{output_dir}/bestscores.txt","w") as f:
        f.write(best_scores)

def textFolderToDict(folder:str,num_files:int)->Dict: # Returns a dict of form {filelocation:text_representation}
    file_locations=sort([f"{folder}/{filename}" for filename in listdir(folder)])
    
    output_dict={}
    if num_files==-1:
        for file in file_locations:
            if file.endswith(".txt"):
                with open(file,"r") as f:
                    output_dict[file]=f.readlines()[0]
        return(output_dict)
    else:
        for file in file_locations[:num_files]:
            if file.endswith(".txt"):
                with open(file,"r") as f:
                    output_dict[file]=f.readlines()[0]
        return(output_dict)
