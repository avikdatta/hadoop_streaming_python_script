#!/bin/bash
/usr/bin/env docker run -i                                 \
         -v /PATH/git/hadoop_streaming_python_script:/app  \
         avikdatta/python_data:latest                      \
         bash -c 'export PATH=$PATH:/root/bedtools2/bin; python /app/script/bed_peak_jaccard_calculation/bed_peak_mapper.py -f FILE_PREFIX -H MYSQL_HOST -n MYSQL_DBNAME -u MYSQL_USER -p MYSQL_PASS'
