from Clarinet.utils.generatedata import genAndEval

collection_dir="Data/Midi/Collection/Original Collection"
type="Noisy"

delete_data=True # If delete_data is True, all files in output_folder are deleted. 
                # If delete_data is False, all files in output_folder are moved to discarded.
num_notes=15
num_queries=30
stride_length=1 # Stride Length
collection_num=-1
num_processes=4 

args=[]
kwargs={"channel":[0],
"pitch":[0,0.05,0.1,0.2,0.3],
"extra":[0,0.05,0.1,0.2,0.3] ,
"delete":[0,0.05,0.1,0.15,0.2],
"velocity":[0],
"length":[0]}



genAndEval(collection_dir,type,num_notes,num_queries,num_processes=num_processes,collection_num=collection_num,stride_length=stride_length,delete_data=delete_data,query_midi_folder="",*args,**kwargs)