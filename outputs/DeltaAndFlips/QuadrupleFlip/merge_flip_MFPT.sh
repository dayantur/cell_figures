#!/bin/bash
#$ -m ea
#$ -M s.rognone@qmul.ac.uk
#$ -cwd -V
#$ -S /bin/bash
#$ -r y
#$ -l h_rt=02:00:00
#$ -t 1-1
#$ -tc 1

module load python
python3 merge_flip_MFPT.py
