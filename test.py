# Set Pitch, Extra, Deleted range here and In misc.ipynb. 
# Run test.py first then Run first box in misc.ipynb. 
# Second box is for plotting which works but the graphs aren't great

import subprocess
from Clarinet.utils.fast import fast
from tqdm import tqdm

num_processes=1 # CPUs/4 (Check Clarinet.evaluation.evaluate.py, line 15)

query_folder="Text/Noisy Queries" # List of folders to evaluate
collection_dir="Text/Original Collection" # Always in TEXT form 
pitch_range=[0,0.1] # Pitch Range
extra_range=[0,0.1] # Extra Notes
deleted_range=[0,0.1] # Deleted Notes Range

query_length=-1 # Query Length
stride_length=30 # Stride Length
query_num=2 # Number of queries to evaluate



dont_convert="Text/" in query_folder

def run_fasteval(query_dir,collection_dir,query_length,stride_length,output_dir="",query_num="-1",dont_convert=False):
    if dont_convert:
        subprocess.run(["python3","fasteval.py","-q",query_dir,"-l",str(query_length),"-c",collection_dir,"-s",str(stride_length),"-o",output_dir,"-n",str(query_num),"-t"])
    else:
        subprocess.run(["python3","fasteval.py","-q",query_dir,"-l",str(query_length),"-c",collection_dir,"-s",str(stride_length),"-o",output_dir,"-n",str(query_num)])


# Save query folders in the form Data/Noisy Queries/pitch/extra/deleted


for pitch in tqdm(pitch_range):
    for extra in tqdm(extra_range):
        inputs=[]

        for deleted in deleted_range:
            input_dir=f"{query_folder}/{pitch}_{extra}_{deleted}"
            output_dir=f"{input_dir.replace('Data','Results').replace('Text','Results').replace('_','/')}"

            inputs.append((input_dir,collection_dir,query_length,stride_length,output_dir,query_num,dont_convert))

        fast(run_fasteval,inputs,num_processes=num_processes)