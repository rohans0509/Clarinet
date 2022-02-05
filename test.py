import subprocess
from Clarinet.utils.fast import fast
from tqdm import tqdm

num_processes=2 # CPUs/4 (Check Clarinet.evaluation.evaluate.py, line 15)

query_folders=["Data/Original Queries","Data/Expected Noise Queries"] # List of folders to evaluate
collection_dir="Text/Original Collection" # Always in TEXT form 
query_length_range=range(5,14) 
stride_length_range=range(1,2) # Stride Length=1
query_num=-1 # Number of queries to evaluate


def run_fasteval(query_dir,collection_dir,query_length,stride_length,output_dir="",query_num="-1"):
    subprocess.run(["python","fasteval.py","-q",query_dir,"-l",str(query_length),"-c",collection_dir,"-s",str(stride_length),"-o",output_dir,"-n",str(query_num)])

for query_length in tqdm(query_length_range):
    for stride_length in(stride_length_range):
        inputs=[]

        for query_dir in query_folders:
            output_dir=f"Results/{query_dir.split('Data/')[1]}/{query_length}/{stride_length}"
            inputs.append((query_dir,collection_dir,query_length,stride_length,output_dir,query_num))

        fast(run_fasteval,inputs,num_processes=num_processes)