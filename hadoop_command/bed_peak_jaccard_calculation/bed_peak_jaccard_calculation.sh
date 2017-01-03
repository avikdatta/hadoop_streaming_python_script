#!/bin/bash

yarn jar /PATH/hadoop-2.7.3/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar \
 -D mapred.reduce.tasks=0 \
 -mapper /PATH/git/hadoop_streaming_python_script/hadoop_mapper_wrapper/bed_peak_jaccard_calculation_mapper.sh \
 -input /INPUT_FILE \
 -output /pair_count

