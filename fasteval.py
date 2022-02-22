from Clarinet.evaluation import evaluate
import os
from Clarinet.utils.generatedata import midiFolder2Text
import argparse

'''
==============
INPUT PARAMETERS
==============
'''

parser = argparse.ArgumentParser(description="Evaluation for Clarinet")
parser.add_argument('-d','--disable_tqdm', required=False,help="Silence Tqdm",action="store_true")

parser.add_argument('-q','--query_dir', required=True,help="Query Directory")
parser.add_argument('-l','--query_length', required=False,type=int,help="Query Length (default : 10)")
parser.add_argument('-n','--query_num', required=False,type=int,help="Number of queries (default : All)")

parser.add_argument('-c','--collection_dir',required=False,help="TEXT form of Collection Directory (default : Text/Original Collection)")
parser.add_argument('-a','--collection_num', required=False,type=int,help="Number of collection songs (default : All)")
parser.add_argument('-o','--output_dir', required=False,help="Results Directory (default : Results/query_dir)")

parser.add_argument('-s','--stride_length', required=False,type=int,help="Stride Length (default : 1)")
parser.add_argument('-e','--channel', required=False,type=int,help="Channel (default : 0)")

# add argument dont_convert which is default False, and inclusion means True
parser.add_argument('-t','--dont_convert', required=False,help="Do not convert Query Folder to Text",action="store_true")



args = parser.parse_args()


query_dir=args.query_dir
collection_dir=args.collection_dir if args.collection_dir else "Text/Original Collection"
query_length=args.query_length if args.query_length else 10
stride_length=args.stride_length if args.stride_length else 1
output_dir=args.output_dir if args.output_dir!="" else f"Results/{query_dir.split('Data/')[-1]}"
channel=args.channel if args.channel else 0
query_num=int(args.query_num) if args.query_num else -1
collection_num=args.collection_num if args.collection_num else -1
disable=args.disable_tqdm if args.disable_tqdm else False
dont_convert=True if args.dont_convert else False

'''
==============
CONVERT QUERIES TO TEXT
==============
'''
# if dont_convert:
query_text_folder=query_dir
# else:
#     query_text_folder=f"Text/{query_dir.split('Data/')[1]}"

#     midiFolder2Text(query_dir,output_folder=query_text_folder,num_files=query_num,num_notes=query_length,channel=channel)

'''
==============
EVALUATE QUERIES
==============
'''

if not os.path.exists(collection_dir):
    raise Exception(f"Collection folder {collection_dir} does not exist, please convert midi collection folder to text first")

query_dir=query_text_folder

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

evaluate(query_dir,collection_dir,stride_length=stride_length,similarity_type="text",output_dir=output_dir,num_queries=query_num,num_collection=collection_num,disable=disable)