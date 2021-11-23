import os
from Clarinet.utils import extractMelodyFolder,preprocessFolder,clipFolder,extractNotes

def generateData(data_dir,mode="doc"):
    # Generate Clipped Data
    clipped=clipFolder(data_dir,mode=mode)
    # clipped="Data/Clipped/Consolidated_query"
    return

    # Generate Processed/Unprocessed
    unprocessed=clipped
    processed=preprocessFolder(unprocessed)
    # processed="Data/Clipped/Consolidated_query_processed"

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

data_dir="Data/Midi/Consolidated"

generateData(data_dir,"doc")
# generateData(data_dir,"query")