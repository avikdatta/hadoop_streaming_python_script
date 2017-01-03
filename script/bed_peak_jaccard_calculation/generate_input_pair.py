import sys, os
import argparse
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument('-i','--index_file',required=True, help='Blueprint's experiment list index file')
args=parser.parse_args()

index=args.index_file

def generate_exp_pair(index_file):
  '''
  A function for generating exp_id pairs
  '''

  index_data=pd.read_table(index_file, chunksize=4000)
  experiment_set = set()
  experiment_pair_set = set()

  for data_chunk in index_data:
    chip_exps=data_chunk.groupby('LIBRARY_STRATEGY').get_group('ChIP-Seq').groupby('EXPERIMENT_ID').groups.keys()
    data_chunk=data_chunk.set_index('EXPERIMENT_ID')

    for exp_id in chip_exps:
      try:
        if type(data_chunk.loc[exp_id]['FILE']) is str:
          file_uri=data_chunk.loc[exp_id]['FILE']
        else:
          file_uri=data_chunk.loc[exp_id][data_chunk.loc[exp_id]['FILE'].str.contains('bed.gz')]['FILE'][exp_id]
      
        if file_uri.endswith('bed.gz'):
          experiment_set.add(exp_id)

      except Exception as e:
        print('Error in data block:{0}'.format(e))

  for exp_id1 in experiment_set:
    for exp_id2 in experiment_set:
      if exp_id1 != exp_id2:
        exp_pair='{0}_{1}'.format(exp_id1, exp_id2)
        exp_rev_pair='{0}_{1}'.format(exp_id2, exp_id1)

        if exp_rev_pair not in experiment_pair_set:
          if exp_pair not in experiment_pair_set:
            experiment_pair_set.add(exp_pair) 
  return experiment_pair_set

exp_pair_set=generate_exp_pair(index_file=index)

for exp_pair in exp_pair_set:
  print("\t".join(exp_pair.split('_')))

