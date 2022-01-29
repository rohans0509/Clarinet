from Clarinet.evaluation import *
from tqdm import tqdm

data_file = r"/Users/rohansharma/Desktop/IIT DELHI/Academics/Sem 5/COL764/Clarinet/Data/Json/2018_clipped_processed/melody.json"
query_file = r"/Users/rohansharma/Desktop/IIT DELHI/Academics/Sem 5/COL764/Clarinet/Data/Json/2018_queries_processed/melody.json"

evaluate(query_file, data_file, similarity_algo="sankoff", melody_algo="modified", processing=False)
