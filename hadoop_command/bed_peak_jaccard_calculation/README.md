# A hadoop streaming command for BEDTools Jaccard score calculation

This is a hadoop streaming python script for calculation of BEDTools Jaccard score for ChIP-Seq peak call results files.

## Hadoop config

Raspberry pi3 specific hadoop config files can be found here [Hadoop config files](../../hadoop_config/).

## Docker config

I used a docker image for running this data analysis script. This image either can be built using the docker file present in git [python_docker_file](https://github.com/avikdatta/python_data_docker_files/tree/master/python_docker_file) or it can be fetched directly from the docker hub [python docker image](https://hub.docker.com/r/avikdatta/python_data/)

## MySQL tables

Input file path records are fetched from table created by [get_all_bed_files.py](https://github.com/avikdatta/python_scripts/tree/master/scripts/load_ftp_bed_files_in_db) script. 

Output scores are stored in a separate mysql table [bed_peak_jaccard.sql](../../sql/bed_peak_jaccard.sql)

<pre><code>
  mysql $DB_OPTIONS < bed_peak_jaccard.sql
</code></pre>

## Input file generation

This hadoop streaming script require a text input file present in the file system. It can be generated using following script [generate_input_pair.py](../../script/bed_peak_jaccard_calculation/generate_input_pair.py). This script require an index file from [Blueprint project's FTP site](http://ftp.ebi.ac.uk/pub/databases/blueprint/releases/current_release/homo_sapiens/20160816.data.index) as input.

<pre><code>
  python get_all_bed_files.py -i INDEX_FILE > HADOOP_INPUT_FILE
</code></pre>

The bed files were copied to every node due to lack of a network mounted filesystem.

## Hadoop mapper wrapper

I used following wrapper bash script for calling the python mapper scrypt with the specific docker options [bed_peak_jaccard_calculation_mapper.sh](../../hadoop_mapper_wrapper/bed_peak_jaccard_calculation_mapper.sh)

## Python mapper script

The python mapper script can be found here [bed_peak_mapper.py](../../script/bed_peak_jaccard_calculation/)

## Load input to HDFS

Following command can be used for loading the input text file to the HDFS file system

<pre><code>
  hadoop fs -put INPUT_FILE /INPUT_FILE
</code></pre>

## Run Yarn command

Once the input file is loaded to the HDFS system and the python and bash scripts are accessible from all the nodes, run the following command from master node (use screen) for submitting jobs [bed_peak_jaccard_calculation.sh](../../hadoop_command/bed_peak_jaccard_calculation/bed_peak_jaccard_calculation.sh).
