import os, sys
import argparse
import pymysql.cursors
from pybedtools import BedTool


parser=argparse.ArgumentParser()
parser.add_argument('-H','--mysql_host', default='localhost', help='MySQL server host name, default: localhost')
parser.add_argument('-P','--mysql_port', default='3306', help='MySQL server port id, default: 3306')
parser.add_argument('-n','--mysql_dbname', required=True, help='MySQL server database name')
parser.add_argument('-u','--mysql_user', required=True, help='MySQL server user name')
parser.add_argument('-p','--mysql_pass', required=True, help='MySQL server password name')
parser.add_argument('-f','--file_path',  required=True, help='File path prefix')


args=parser.parse_args()

mysql_host   = args.mysql_host
mysql_port   = args.mysql_port
mysql_dbname = args.mysql_dbname
mysql_user   = args.mysql_user
mysql_pass   = args.mysql_pass
path_prefix  = args.file_path

dbparams={ 'host': mysql_host, 'password': mysql_pass, 'user': mysql_user, 'db': mysql_dbname, 'port':mysql_port }

# connect to MySQL db
db_conn = pymysql.connect(**dbparams)


# Copying all function to the main script

def fetch_path_for_exp(db_conn, exp_id):
  '''
  Function for collecting file path from database
  '''

  sql='''
      select filename from bed_files where experiment_id = %s
      '''
  try:
    with db_conn.cursor() as cursor:
      hit_count=cursor.execute(sql,(exp_id))
      
      if hit_count > 1:
        raise Exception('more than one file found for {0}'.format(exp_id))
      filepath=(cursor.fetchone())[0]
  except Exception as e:
    print('error is: {0}'.format(e))
  else: 
    return filepath

def check_peak_interaction_db(db_conn, exp_idA, exp_idB):
  '''
  Function for checking if the peak intersection data already exists in db
  '''
  sql='''
      SELECT * from `peak_intersection` 
      where 
      `experiment_idA` = %s AND 
      `experiment_idB` = %s
      '''
  
  val_exist=False

  with db_conn.cursor() as cursor:
    try:
      cursor.execute(sql,(exp_idA, exp_idB))
      hit_count=cursor.fetchall()
    except Exception as e:
      print('got errpt {0}'.format(e))

  if hit_count:
    val_exist=True

  return val_exist


def calculate_bedtool_jaccard(bedA, bedB, **args):
  '''
  This function use pybedtools package for calculating jaccard stats
  between two bed files
  '''
  
  # check if files are present
  if not os.path.exists(bedA):
    sys.exit('bed file not found, {0}'.format(bedA))

  if not os.path.exists(bedB):
    sys.exit('bed file not found, {0}'.format(bedB))

  # load files
  bedA_obj=BedTool(bedA)
  bedB_obj=BedTool(bedB)
 
  
  # calculate jaccard stats

  try:  
    jaccard_stats=bedA_obj.jaccard(bedB_obj, **args)
  except Exception as e:
    print('Failed jaccard run for {0}, {1}: {2}'.format(bedA, bedB, e))
  else:
    return jaccard_stats

def store_peak_interaction_stat(db_conn, exp_idA, exp_idB, data):
  '''
  Function for storing the data in db
  '''

  sql='''
      INSERT INTO `peak_intersection` ( `experiment_idA`, `experiment_idB`, 
      `jaccard`, `n_intersections`) VALUES ( %s, %s, %s, %s)
      '''

  jaccard_val=data['jaccard']
  n_intersections=data['n_intersections']

  with db_conn.cursor() as cursor:
    try:
      # insert value of A, B
      cursor.execute(sql, (exp_idA, exp_idB, jaccard_val, n_intersections))

      # insert value of B, A
      cursor.execute(sql, (exp_idB, exp_idA, jaccard_val, n_intersections))
    except Exception as e:
      print('Got error: {0}'.format(e))
    else:
      db_conn.commit()


if __name__=='__main__':

  for line in sys.stdin:
    # read streaming lines as input

    (exp_idA, exp_idB)=line.rstrip().split("\t")
    print('Running for {0}, {1}'.format(exp_idA, exp_idB))

    val_exist=check_peak_interaction_db(db_conn=db_conn, exp_idA=exp_idA, exp_idB=exp_idB)


    if not val_exist:
      try:
        fileA=os.path.join(path_prefix, fetch_path_for_exp(db_conn=db_conn, exp_id=exp_idA))
     
        fileB=os.path.join(path_prefix, fetch_path_for_exp(db_conn=db_conn, exp_id=exp_idB))

        data=calculate_bedtool_jaccard(bedA=fileA, bedB=fileB, f=0.95, r=True)

        store_peak_interaction_stat(db_conn=db_conn, exp_idA=exp_idA, exp_idB=exp_idB, data=data)
      except Exception as e:
        print('Got error {0}'.format(e))
      
  db_conn.close()
