from typing import Dict
from numpy import sort
from Clarinet.converter import midi2text
from os import listdir,path
import os



def midiFolderToDict(folder:str,num_files:int,num_notes=-1,channel=0)->Dict: # Returns a dict of form {filelocation:text_representation}
    file_locations=sort([f"{folder}/{filename}" for filename in listdir(folder)])
    
    output_dict={}
    if num_files==-1:
        for file in file_locations:
            if file.endswith(".mid"):
                output_dict[file]=midi2text(file,channel=channel,num_notes=num_notes)
        return(output_dict)
    else:
        for file in file_locations[:num_files]:
            if file.endswith(".mid"):
                output_dict[file]=midi2text(file,channel=channel,num_notes=num_notes)
        return(output_dict)


def generateText(folder,num_files=-1,output_folder="Results",num_notes=-1,channel=0):
    out_dict=midiFolderToDict(folder,num_files,num_notes=num_notes,channel=channel)
    for file,text in out_dict.items():
        foldername=output_folder
        if not path.exists(foldername):
            os.mkdir(foldername)
        filename=f"{file.split('/')[-1]}".replace(".mid",".txt")
        with open(f"{foldername}/{filename}","w") as f:
            f.write(text)
