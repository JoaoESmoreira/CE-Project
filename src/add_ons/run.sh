#!/bin/bash

instance="data/MAP_4_BY_4/input01.txt"
algorithm="random"
prog="problem.py"

for i in {1..100}
do
	pypy3 ${prog} --input-file ${instance} --algorithm ${algorithm}
done

