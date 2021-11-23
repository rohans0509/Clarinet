import os
from Clarinet.utils import extractMelodyFolder,preprocessFolder,clipFolder


data_dir="Data/Midi/Birthday"

# Generate Clipped Data
clipped=clipFolder(data_dir)

# Generate Processed/Unprocessed
unprocessed=clipped
processed=preprocessFolder(unprocessed)

# Generate Melody

# Skyline
extractMelodyFolder(processed,"skyline")
extractMelodyFolder(unprocessed,"skyline")

# Modified
extractMelodyFolder(processed,"modified-skyline")
extractMelodyFolder(unprocessed,"modified-skyline")
    