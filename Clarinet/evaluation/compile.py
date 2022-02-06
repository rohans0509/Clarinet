import os
import itertools
import pandas as pd
from tqdm import tqdm

def compile(result_dir,naming={},metric="Mean Rank",output_dir="Results/Analysis"):
    values=list(naming.values())

    product=list(itertools.product(*values))

    metric2index={
        "Recall@1":0,
        "Recall@3":1,
        "Recall@5":2,
        "Recall@10":3,
        "Mean Rank":4,
        "Normalised Similarity":5,
        "Margin of Error":6,
        "Average Confidence":7,
        "MRR":8
    }


    metric_index=metric2index[metric]

    out_dict={}
    for location in tqdm(product):
        full_location=f"{result_dir}/{'/'.join([str(element) for element in location])}/analysis.csv"
        try:
            df=pd.read_csv(full_location)
            metric_value=df.iloc[metric_index]["Value"]
            out_dict[location]=metric_value
        except:
            print(f"Couldn't find {full_location}")

    columns=list(naming.keys())+[f"{metric}"]
    scores=pd.DataFrame(columns=columns)

    sorted_dict = {k: v for k, v in sorted(out_dict.items(), key=lambda item: item[1],reverse=True)}

    for location,score in sorted_dict.items():
        column_values=list(location)+[score]
        scores.loc[len(scores)] = column_values
    scores.index+=1
    scores.index.names = ['Index']

    # Check if folder does not exist and create it
    full_output_dir=f"{output_dir}/{result_dir.split('Results/')[1]}/CSV"
    if not os.path.exists(full_output_dir):
        os.makedirs(full_output_dir)
    scores.to_csv(f"{full_output_dir}/{metric}.csv")