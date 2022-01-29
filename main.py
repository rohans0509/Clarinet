# from Clarinet.converter.midi2audio import midi2audio
# from Clarinet.converter.audio2midi import audio2midi
# from  Clarinet.visualiser import visualise
# from Clarinet.melodyextraction import extractMelody
# from Clarinet.preprocessing import preprocess
# from Clarinet.utils import extractMelodyFolder,extractNotes,preprocessFolder
from generateData import generateNoisy
from generateQueries import genQuery, genQueryFromFolder
import miditoolkit
import os
import shutil
from tqdm import tqdm
filename = "Data/Audio/Birthday/happy_birthday.wav"
mode = "music-piano-v2"


# Convert File to Midi

# midi_filename=audio2midi(file=filename, mode=mode)

# midi_filename="Data/Midi/Birthday/happy_birthday.mid"

# Preprocess Midi File
# processed_filename=preprocess(midi_filename)

# Extract Melody from Midi and Save to Midi

# melody_midi_filename=extractMelody(processed_filename)


# extractNotes(processed_folder)


# processed_folder=preprocessFolder("Data/Midi/2018_clipped")
# melody_folder=extractMelodyFolder("Data/Midi/2018_clipped_processed")

# processed_folder=preprocessFolder("Data/Midi/2018_queries")
# melody_folder=extractMelodyFolder("Data/Midi/2018_queries_processed")


#generateNoisy("Data/Original Collection","Data/Noisy Collection")

# function to copy all .mid files from all subdirectories in folder 1 to folder 2
def copy_midi_files(folder1,folder2):
    # check if folder1 is a directory
    if not os.path.isdir(folder1):
        return
    filenames=os.listdir(folder1)
    filelocations=[f"{folder1}/{filename}" for filename in filenames]
    midi_filelocations=[filelocation for filelocation in filelocations if filelocation.endswith(".mid")]
    for file in midi_filelocations:
        shutil.copy(file,folder2)


# # loop through all folders in folder 1
# for folder in os.listdir("Data/Original Collection/POP909"):
#     copy_midi_files(f"Data/Original Collection/POP909/{folder}","Data/Original Collection")


#generateNoisy("Data/Original Collection","Data/Noisy Collection")

# loop through all mid files in folder 1
# for file in tqdm(os.listdir("Data/Original Collection")):
#     if file.endswith(".mid"):
#         mido_obj = miditoolkit.midi.parser.MidiFile(f"Data/Original Collection/{file}")
#         mido_obj.instruments[0].notes.sort(key=lambda x: x.start)
#         for i in range(1,len(mido_obj.instruments[0].notes)):
#             prev_end = mido_obj.instruments[0].notes[i-1].end
#             curr_start = mido_obj.instruments[0].notes[i].start
#             if prev_end>curr_start:
#                 mido_obj.instruments[0].notes[i-1].end = curr_start
#         mido_obj.instruments[0].notes.sort(key=lambda x: x.end)
#         mido_obj.dump(f"Data/Original Collection/{file}")

#genQueryFromFolder("Data/Original Collection","Data/Queries")

