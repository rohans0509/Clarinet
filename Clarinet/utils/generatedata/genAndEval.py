from Clarinet.utils.generatedata import genTextQueries
from Clarinet.utils.fast import fast
import itertools
from Clarinet.evaluation import evaluate
import os
import shutil
def genAndEval(collection_dir,type,num_notes,num_queries,num_processes=4,num_collection=-1,stride_length=1,delete_data=True,query_midi_folder="",similarity_type="text",*args,**kwargs):
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

    result_folder=query_folder.replace('Data/Text/Queries','Results')
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    # Delete everything in result_folder
    if delete_data:
        for file in os.listdir(result_folder):
            file_path=os.path.join(result_folder,file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    kwargs=kwargs


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

        inputs.append((query_dir,collection_dir,num_queries,num_collection,stride_length,similarity_type,output_dir))
    fast(evaluate,inputs,num_processes=num_processes)