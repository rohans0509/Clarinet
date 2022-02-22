import os
from Clarinet.melodyextraction.skyline import skyline,mskyline
from constants import midi_folder

strategies={
    "skyline":skyline,
    "modified-skyline":mskyline
}

def extractMelody(file, output_dir=midi_folder,strategy="modified-skyline"):
    folder_name,filename=file.split('/')[-2],file.split('/')[-1].split('.')[0]

    if strategy=="modified-skyline":
        output_dir=f"{output_dir}/{folder_name}_modified"
    else:
        output_dir=f"{output_dir}/{folder_name}"


    strategy=strategies[strategy]

    mid_out = strategy(file)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    out=f"{output_dir}/{filename}_melody.mid"

    mid_out.dump(out)
    return(output_dir)
