#!/bin/bash

INDEXES=$(seq 1 14)
for i in $INDEXES
do
    INDEXES2=$(seq 0 $i)
    for j in $INDEXES2
    do
        echo "Running bagging for index $i"
        nice -19 python3 main_dutch.py --bagging_index $j --num_bagging $i
    done
done 
