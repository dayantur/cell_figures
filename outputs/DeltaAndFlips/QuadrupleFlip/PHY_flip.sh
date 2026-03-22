#!/bin/bash
#$ -m ea
#$ -M s.rognone@qmul.ac.uk
#$ -cwd -V
#$ -S /bin/bash
#$ -r y
#$ -l h_rt=02:00:00
#$ -t 1-99
#$ -tc 99 

module load python/3.10.7

if ! python3 -c "import numpy" &>/dev/null; then
    echo "Installing numpy..."
    python3 -m pip install --user numpy
else
    echo "Numpy is already installed."
fi

TASK=$(sed -n "${SGE_TASK_ID}p" ./idjobs.txt)
python3 quadruple_PHY.py ${TASK}

