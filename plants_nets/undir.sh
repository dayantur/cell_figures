#!/bin/bash

##
## Compute the undirected simple graph associated  to a graph given as 
## imput, i.e., remove duplicate and reciprocated edges
##

if [ $# -le 0 ]; then
    echo "Usage: $0 <netfile>"
    exit 1
fi


for i; do 
#    echo $i 
#    awk '{if ($1 > $2) print $2, $1; else print $0}' $i | sort -n  | uniq > u.$i
    awk '{if ($1 > $2) print $2, $1; else print $0}' $i | sort -n  | uniq > u.$i

done

for file in u.*
do
  mv "$file" "${file/u./}"
done
