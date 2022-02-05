import itertools
from multiprocessing.dummy import Pool as ThreadPool 
from tqdm import tqdm
import Clarinet.utils.fast.istarmap

def fast(function,inputs,num_processes=4):
    print("-------------------------------")
    print(f"Running {num_processes} processes")
    pool = ThreadPool(num_processes)

    for _ in tqdm(pool.istarmap(function, inputs),
                        total=len(inputs)):
        pass


    
    # pool.starmap(function,tqdm(inputs))

    print("\n\n\n\n\n-------------------------------")
    print(f"All processes run")

