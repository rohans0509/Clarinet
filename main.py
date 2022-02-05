import subprocess
from Clarinet.utils.fast import fast

def run_fasteval(query_dir,collection_dir,query_length,stride_length):
    subprocess.run(["python","fasteval.py","-q",query_dir,"-l",str(query_length),"-c",collection_dir,"-s",str(stride_length)])


query_folders=["Data/Expected Noise Queries"]
collection_dir="Text/Original Collection" # Collection dir is always in text form
query_length=11
stride_length=1
num_processes=4
# output_dir="Results/Expected Noise Queries"
# disable_tqdm=False

inputs=[]

for query_dir in query_folders:
    inputs.append((query_dir,collection_dir,query_length,stride_length))

fast(run_fasteval,inputs,num_processes=num_processes)


