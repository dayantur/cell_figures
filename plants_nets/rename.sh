#!/bin/bash

##
## Compute the undirected simple graph associated  to a graph given as 
## imput, i.e., remove duplicate and reciprocated edges
##

if [ $# -le 0 ]; then
    echo "Usage: $0 <netfile>"
    exit 1
fi


for file in u.*
do
  mv "$file" "${file/u./}"
done


