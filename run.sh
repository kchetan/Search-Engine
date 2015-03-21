#!/bin/bash
## to the the files use ./run.sh $1 $2 
## where the $1 is the path of the input file to be indexed and the $2 is the index file path $3 is the input queries.
## example: ./run.sh ./src/s.xml Index/index.txt in
python ./src/assignment_index.py $1
python ./src/assignment_sindex.py $2
python src/assignment_sindex_title.py Tindex/Titles.txt
python ./src/assignment_query.py < $3 > ./src/output

