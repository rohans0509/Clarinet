# '''
# ===================
# Generate Queries
# ===================
# '''

# from Clarinet.utils.generatedata import genTextQueries

# collection_dir="Data/Midi/Collection/Original Collection"
# type="Noisy"
# output_folder=f"Data/Midi/Queries/{type} Queries"

# delete_data=True # If delete_data is True, all files in output_folder are deleted. 
#                 # If delete_data is False, all files in output_folder are moved to discarded.
# num_notes=15
# num_queries=2

# args=[]
# kwargs={"channel":[0],
# "pitch":[0,0.05,0.1,0.2,0.3],
# "extra":[0,0.05,0.1,0.2,0.3] ,
# "delete":[0,0.05,0.1,0.15,0.2],
# "velocity":[0],
# "length":[0]}

# genTextQueries(collection_dir,type,output_folder,delete_data,num_notes,num_queries,**kwargs)

# '''
# ===================
# Evaluate Model
# ===================
# '''
# import subprocess
# from Clarinet.utils.fast import fast
# from tqdm import tqdm
# import itertools

# num_processes=4 # CPUs/4 (Check Clarinet.evaluation.evaluate.py, line 15)

# query_folder=output_folder.replace("Midi","Text") # List of folders to evaluate
# collection_dir=collection_dir.replace("Midi","Text") # Always in TEXT form 

# query_length=-1 # Query Length
# stride_length=1 # Stride Length
# query_num=-1 # Number of queries to evaluate

# kwargs=kwargs

# dont_convert="Text/" in query_folder

# def run_fasteval(query_dir,collection_dir,query_length,stride_length,output_dir="",query_num="-1",dont_convert=False):
#     if dont_convert:
#         subprocess.run(["python3","fasteval.py","-q",query_dir,"-l",str(query_length),"-c",collection_dir,"-s",str(stride_length),"-o",output_dir,"-n",str(query_num),"-t"])
#     else:
#         subprocess.run(["python3","fasteval.py","-q",query_dir,"-l",str(query_length),"-c",collection_dir,"-s",str(stride_length),"-o",output_dir,"-n",str(query_num)])


# # Save query folders in the form Data/Noisy Queries/pitch/extra/deleted

# keys=list(kwargs.keys())
# values=list(kwargs.values())
# product=list(itertools.product(*values))

# inputs=[]

# for tup in product:
#     args=[]
#     kwargs={keys[i]:tup[i] for i in range(len(keys))}
#     name_list=[f"{key.capitalize()} {value}" for key,value in kwargs.items()]
#     output_dir=f"{output_folder}/{'/'.join(name_list)}"

#     input_dir=f"{query_folder}/{pitch}_{extra}_{deleted}"
#     output_dir=f"{input_dir.replace('Data','Results').replace('Text','Results').replace('_','/')}"

#     inputs.append((input_dir,collection_dir,query_length,stride_length,output_dir,query_num,dont_convert))

# fast(run_fasteval,inputs,num_processes=num_processes)

