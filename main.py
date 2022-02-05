import subprocess
from Clarinet.utils.fast import fast

def run_fasteval(query_dir,collection_dir,query_length,stride_length,output_dir="",query_num="-1"):
    subprocess.run(["python","fasteval.py","-q",query_dir,"-l",str(query_length),"-c",collection_dir,"-s",str(stride_length),"-o",output_dir,"-n",str(query_num)])


query_folders=["Data/Original Queries"]
collection_dir="Text/Original Collection" # Collection dir is always in text form
query_length=5
stride_length=15
num_processes=1
query_num=2
output_dir=""



inputs=[]

for query_dir in query_folders:
    inputs.append((query_dir,collection_dir,query_length,stride_length,output_dir,query_num))

fast(run_fasteval,inputs,num_processes=num_processes)


