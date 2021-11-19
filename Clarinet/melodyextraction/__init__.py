import os
from .skyline import skyline

strategies={
    "skyline":skyline
}

def extractMelody(file, output_dir="Data/Melody",strategy="skyline"):
    folder_name,filename=file.split('/')[-2],file.split('/')[-1].split('.')[0]

    output_dir=f"{output_dir}/{folder_name}"

    strategy=strategies[strategy]

    mid_out = strategy(file)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    out=f"{output_dir}/{filename}_melody.mid"

    mid_out.dump(out)
    return(out)
