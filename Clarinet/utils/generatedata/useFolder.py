import os
from Clarinet.utils.generatedata.preprocessFolder import preprocessFolder
from Clarinet.usermodel import User
import miditoolkit
from tqdm import tqdm

# def generateData(data_dir,mode="doc"):
#     # Generate Clipped Data
#     clipped=clipFolder(data_dir,mode=mode)

#     # Generate Processed/Unprocessed
#     unprocessed=clipped
#     processed=preprocessFolder(unprocessed)


#     # Generate Melody and Notes

#     # Skyline
#     melody_folder=extractMelodyFolder(processed,"skyline")
#     extractNotes(melody_folder)

#     melody_folder=extractMelodyFolder(unprocessed,"skyline")
#     extractNotes(melody_folder)

#     # Modified
#     melody_folder=extractMelodyFolder(processed,"modified-skyline")
#     extractNotes(melody_folder)

#     melody_folder=extractMelodyFolder(unprocessed,"modified-skyline")
#     extractNotes(melody_folder)


def useFolder(query_dir,output_folder,type="Noisy",*args,**kwargs):
    filenames=os.listdir(query_dir)
    filelocations=[f"{query_dir}/{filename}" for filename in filenames]
    midi_filelocations=[filelocation for filelocation in filelocations if filelocation.endswith(".mid")]
    for file in tqdm(midi_filelocations):
        user=User(type)
        user.use(midi_file=file,output_folder=output_folder,*args,**kwargs)

