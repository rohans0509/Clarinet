import os
from Clarinet.utils import extractMelodyFolder,preprocessFolder,clipFolder,extractNotes
from Clarinet.usermodel import User
import miditoolkit
from tqdm import tqdm

def generateData(data_dir,mode="doc"):
    # Generate Clipped Data
    clipped=clipFolder(data_dir,mode=mode)

    # Generate Processed/Unprocessed
    unprocessed=clipped
    processed=preprocessFolder(unprocessed)


    # Generate Melody and Notes

    # Skyline
    melody_folder=extractMelodyFolder(processed,"skyline")
    extractNotes(melody_folder)

    melody_folder=extractMelodyFolder(unprocessed,"skyline")
    extractNotes(melody_folder)

    # Modified
    melody_folder=extractMelodyFolder(processed,"modified-skyline")
    extractNotes(melody_folder)

    melody_folder=extractMelodyFolder(unprocessed,"modified-skyline")
    extractNotes(melody_folder)


def generateNoisy(data_dir,output_folder,type="Noisy",*args,**kwargs):
    filenames=os.listdir(data_dir)
    filelocations=[f"{data_dir}/{filename}" for filename in filenames]
    midi_filelocations=[filelocation for filelocation in filelocations if filelocation.endswith(".mid")]
    for file in (midi_filelocations):
        user=User(type)
        user.use(file,output_folder,*args,**kwargs)

