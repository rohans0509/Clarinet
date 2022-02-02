from typing import Dict

from numpy import sort
from Clarinet.search import similarity
from Clarinet.evaluation import analyse
from Clarinet.converter import midi2text
from os import listdir,path
import os
import json
from tqdm import tqdm
import miditoolkit


def midiFolderToDict(folder:str,num_files:int)->Dict: # Returns a dict of form {filelocation:text_representation}
    file_locations=sort([f"{folder}/{filename}" for filename in listdir(folder)])
    
    output_dict={}
    if num_files==-1:
        for file in tqdm(file_locations):
            if file.endswith(".mid"):
                output_dict[file]=midi2text(file)
        return(output_dict)
    else:
        for file in tqdm(file_locations[:num_files]):
            if file.endswith(".mid"):
                output_dict[file]=midi2text(file)
        return(output_dict)


def generateText(folder,num_files=-1,output_folder="Text"):
    out_dict=midiFolderToDict(folder,num_files)
    for file,text in out_dict.items():
        foldername=f"{output_folder}/{file.split('/')[-2]}"
        if not path.exists(foldername):
            os.mkdir(foldername)
        filename=f"{file.split('/')[-1]}".replace(".mid",".txt")
        with open(f"{foldername}/{filename}","w") as f:
            f.write(text)

for folder in tqdm(os.listdir("Data/Noisy Queries")):
    folder_location=f"Data/Noisy Queries/{folder}"
    generateText(folder_location,output_folder="Text/Noisy Queries",num_files=-1)
    # print(folder_location)