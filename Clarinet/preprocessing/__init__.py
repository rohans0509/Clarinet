from .transpose import transpose,getKey
from .clipper import clip
import os
def preprocess(midi_filename):
    print(f"Preprocessing {midi_filename}")
    return(transpose(midi_filename))

def clipFile(file, output_dir="Data/Clipped"):
    folder_name,filename=file.split('/')[-2],file.split('/')[-1].split('.')[0]
    output_dir=f"{output_dir}/{folder_name}"

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    mid_out=clip(file)

    out=f"{output_dir}/{filename}.mid"
    mid_out.dump(out)
    
    return(output_dir)