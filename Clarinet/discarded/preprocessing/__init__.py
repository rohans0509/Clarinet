from .transpose import transpose,getKey
from .clipper import clip
import os
def preprocess(midi_filename):
    try:
        out=transpose(midi_filename)
    except:
        print(midi_filename)
    return(out)

def clipFile(file, output_dir="Data/Clipped",mode="doc"):
    try:
        folder_name,filename=file.split('/')[-2],file.split('/')[-1].split('.')[0]

        output_dir=f"{output_dir}/{folder_name}" if mode=="doc" else f"{output_dir}/{folder_name}_query"

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        mid_out=clip(file,mode=mode)

        out=f"{output_dir}/{filename}.mid"
        mid_out.dump(out)
    except:
        print("-------")
        print(file)
        print("-------")
    return(output_dir)