from Clarinet.utils.generatedata import genTextQueries
import subprocess
from Clarinet.utils.fast import fast
from tqdm import tqdm
import itertools

def genAndEval(collection_dir:str,type,num_notes,num_queries,num_processes=4,collection_num=-1,stride_length=1,delete_data=True,query_midi_folder="",*args,**kwargs):
    '''
    ===================
    Generate Queries
    ===================
    '''
    if query_midi_folder=="":
        query_midi_folder=f"Data/Midi/Queries/{type} Queries"

    args=args
    kwargs=kwargs

    genTextQueries(collection_dir,type,query_midi_folder,delete_data,num_notes,num_queries,**kwargs)

    '''
    ===================
    Evaluate Model
    ===================
    '''

    query_folder=query_midi_folder.replace("Midi","Text") # List of folders to evaluate
    collection_dir=collection_dir.replace("Midi","Text") # Always in TEXT form 

    query_length=num_notes # Query Length

    kwargs=kwargs

    dont_convert="Text/" in query_folder

    # Save query folders in the form Data/Noisy Queries/pitch/extra/deleted

    keys=list(kwargs.keys())
    values=list(kwargs.values())
    product=list(itertools.product(*values))

    inputs=[]

    for tup in product:
        args=[]
        kwargs={keys[i]:tup[i] for i in range(len(keys))}

        name_list=[f"{key.capitalize()} {value}" for key,value in kwargs.items()]
        query_dir=f"{query_folder}/{'/'.join(name_list)}"

        output_dir=f"{query_dir.replace('Data/Text/Queries','Results')}"

        inputs.append((query_dir,collection_dir,query_length,stride_length,output_dir,num_queries,dont_convert,collection_num))

    fast(run_fasteval,inputs,num_processes=num_processes)

def run_fasteval(query_dir,collection_dir,query_length,stride_length,output_dir="",query_num="-1",dont_convert=False,collection_num=-1):
        if dont_convert:
            subprocess.run(["python3","fasteval.py","-q",query_dir,"-l",str(query_length),"-c",collection_dir,"-s",str(stride_length),"-o",output_dir,"-n",str(query_num),"-t","-a",str(collection_num)])
        else:
            subprocess.run(["python3","fasteval.py","-q",query_dir,"-l",str(query_length),"-c",collection_dir,"-s",str(stride_length),"-o",output_dir,"-n",str(query_num),"-a",str(collection_num)])