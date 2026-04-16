# Repository Overview

This repository contains scripts, data, and outputs related to the paper. Below there is 
- a description of the repository contents
- a description of how to generate the figures

## Contents

### Scripts
- **ClusterSizeTreelikeness.py**  
  Code for analyzing clusters and generating outputs related to size and treelikeness for real data.
  
- **ClusterSizeTreelikenessNulls.py**  
  Code for analyzing null reshufflings of cluster sizes and treelikeness.
  
- **FixedReshuffling.py**  
  Code for generating fixed reshufflings for null model analysis.

- **KSCalculations.py**  
  Code for computing Kolmogorov-Smirnov (KS) statistics between real and null datasets.

- **Fig2C.py**  
  Code for generating Fig 2C: Scatter plots comparing KS Size and KS Treelikeness.

- **Fig2D.py**  
  Code for generating Fig 2D: Ranked lists for species based on KS values and value of Kendall's Tau.

- **TableS1.py**  
  Code for generating TableS1: lists for species and their KS values (with p-values).

- **Fig3C.py**  
  Code for generating Fig3C and outputs relevant for FigS3.

- **Fig3D.py**  
  Code for generating Fig3D and outputs relevant for FigS3.

- **DeltaAnd123Flips.py**  
  Code for generating outputs relevant for FigS3.

- **FigS3.py**  
  Code for generating FigS3.

- **Fig4B-4C.r**  
  Code for generating Fig4B-4C.

- **Fig4D.py**  
  Code for generating Fig4D.

- **FigS3.py**  
  Code for generating FigS3.

- **FigS6.ipynb / .py**  
  Code for generating FigS6.

- **RelabelAttacked.py**  
  Code for generating  outputs relevant for Fig4B-C, FigS6 and TableS2.

- **ResilienceCalculations.py**  
  Code for generating  outputs relevant for Fig4B-D, FigS6 and TableS2.

- **RNDAndEGMAttacks.py**  
  Code for generating  outputs relevant for Fig4B-C, FigS6 and TableS2.

- **TableS2.py**  
  Code for generating TableS2.

### Folders

#### **dendros**
This folder contains files for Fig3C and Fig3D.

#### **generatedfigures**
This folder will contain all the .pdf figures that can be generated from the .py scripts.

#### **keynotes**
This folder contains all the keynote files (and exported .pdf files) that can be used to reconstruct more complex figures (i.e. figures that cannot be produced by only running python scripts).

#### **MFPT**
This folder contains subfolders for MFPT data analysis:

- **Nulls_MFPT** 

    Will contain Null_Fixed.zip with MFPT calculatons for null models. 

- **Real_MFPT**

    Contains MFPT files for real nets.

- **Attacks_MFPT**

    Contains MFPT files for attacked nets.

#### **outputs**
This folder contains the outputs of the main analysis scripts:
- **ClusterSizeTreelikeness**  
  Results of cluster size and treelikeness analyses for real datasets.  
  File format: `{species}_{colour}_clustersize.txt` or `{species}_{colour}_treel.txt`
  
- **ClusterSizeTreelikenessNulls**  
  Results of cluster size and treelikeness analyses for null datasets.  
  File format: `{species}_{colour}_null{number}_clustersize.txt` or `{species}_{colour}_null{number}_treel.txt`

- **KSStatistics**  
  Results of KS cluster size and treelikeness calculations.

#### **plants_nulls**
Collection of fixed reshufflings for null models.  
File format: `{species}_null{number}.txt`

#### **plants_nets**
Nets and nodeid-colour .txt files for each species.  
Files format: 
- `{species}_net_relabel.txt` 
is the edges list .txt file. First node is called '0', second node is called '1', and so on. 
- `{species}_colour_relabel.txt` 
is the nodeid-colour .txt file with no grey nodes (missing nodes are not included).
- `{species}_colour_relabel_p.txt` 
is the nodeid-colour .txt file with added grey nodes (missing nodes are now included and assigned colour '0').
Green is colour '1', blue is colour '2'.

## How to generate

### Fig2C-Fig2D
1. 
- Run FixedReshuffling.py
- Check that the null models has been created in plants_nulls

2. 
- Run ClusterSizeTreelikeness.py
- Check that the ClusterSizeTreelikeness.zip folder has been created in outputs/ClusterSizeTreelikeness

3.
- Run ClusterSizeTreelikenessNulls.py
- Check that the ClusterSizeTreelikenessNulls.zip folder has been created in outputs/ClusterSizeTreelikenessNulls

4. 
- Run KSCalculations.py
- Check that the KSStatistics folder has ben populated with KS_Size.csv and KS_Treel.csv

5. 
- Run Fig2C.py
- Check that the Fig2C.pdf has ben generated in generatedfigures

6. 
- Run Fig2D.py
- Check that the Fig2D.pdf has ben generated in generatedfigures
- Save the Kendall's Tau shown in the terminal

7.
- Use .pdf and keynote in keynote folder to create Fig2D by mixing Fig2D.pdf, Kendall's Tau value and other components.

### TableS1
1. Follow steps 1-5 of Fig2C-Fig2D.

2. 
- Run TableS1.py
- Check that the TableS1.pdf has ben generated in generatedfigures

### Fig3C
<!-- 1. @Liam create a .csv file similar as the current ./dendros/renamed_evolutionary_matrix.csv, but with the new species included. Rename the old file as ./dendros/old_renamed_evolutionary_matrix.csv and save this new file as ./dendros/renamed_evolutionary_matrix.csv (i.e. name it as renamed_evolutionary_matrix.csv in folder dendros) -->


1.
- Run Fig3C.py
- Check that Fig3C.pdf has ben generated in generatedfigures

### Fig3D
<!-- 1. Run 10^4 random-walks-per-node MFPT calculations for the new species using V.N. MFPT Code with  `{newspecies}_net_relabel.txt` (network) and `{newspecies}_colour_relabel_p.txt` (nodeid col file). Store the MFPT .txt file into ./MFPT/Real_MFPT/ in the format`10^4_mfpt_{newspecies}.txt`.  -->

<!-- 2. @Enzo run 10^4 random-walks-per-node MFPT calculations for each null model of EACH species using `{species}_net_relabel.txt` in ./plants_nets as network (network files) and the nulls in FixedReshuffling (nodeid col files) that you should have already generated while doing step 2 of Fig2C-Fig2D task. Files names for nulls MFPT should end with `{newspecies}_.txt`. Compress the nulls MFPT into a .zip folder called Null_Fixed.zip and move it into ./MFPT/Nulls_MFPT/.  -->

1. 
- Run Fig3D.py
- Check that, for each species, the script has stored a taualfabeta matrix .txt file in ./outputs/TauAlfaBetaMatrices called `{species}_talfabeta_normalised.txt`.
- Check that Fig3D.pdf has ben generated in generatedfigures.

### FigS3

1. Follow steps for Fig3C and Fig3D.

2.
- Run DeltaAnd123Flips.py
- Check that `Phylogenetic_originaldistancematrix.txt` and `MFPT_originaldistancematrix.txt` has been generated in ./outputs/DeltaAndFlips/QuadrupleFlip/
- Store the value of Delta (printed on the terminal).
- Check that `{flip}_Phylogenetic_deltadistances.txt` and `{flip}_MFPT_deltadistances.txt` has been generated in ./outputs/DeltaAndFlips/ for 1flip, 2flip and 3flip.

3.
- Transfer QuadrupleFlip folder to an HPC
- Launch PHY_flip.sh
- Check that outputs for Phylogenetic have been generated in QuadrupleFlip/data folder
- Launch MFPT_flip.sh
- Check that outputs for MFPT have been generated in QuadrupleFlip/data folder
- Launch merge_flip_PHY.sh
- Check that `4flip_Phylogenetic_deltadistances.txt` has been generated in QuadrupleFlip folder
- Launch merge_flip_MFPT.sh
- Check that `4flip_MFPT_deltadistances.txt` has been generated in QuadrupleFlip folder
- Download QuadrupleFlip into ./outputs/DeltaAndFlips/

4. 
- Run FigS3.py
- Check that FigS3.pdf has been generated in generated figures.

### Fig4B-C

1. 
- Run RGMAndEGMAttacks.py
- Check that the script has stored 100 RND (and 100 EGM) .txt files for each percentage in ./outputs/Attacks/RND/ (and ./outputs/Attacks/EGM/) called `{species_name}_net_rndatt_p{perc}_{count}.txt` (and `{species_name}_net_egmatt_p{perc}_{count}.txt`).

2.
- Run RelabelAttacked.py
- Check that the script has stored 100 RND (and 100 EGM) .txt files for each percentages in ./outputs/Attacks/{att_u}/{species_name}/Relabel/ called `{species_name}_net_{att}att_p{p}_{r}_r.txt`
- Check that the script has stored 100 RND (and 100 EGM) .txt files for each percentages in ./outputs/Attacks/{att_u}/{species_name}/Relabel/ called `{species_name}_colours_{att}att_p{p}_{r}_r.txt`

3. 
<!-- - Run 10^4 random-walks-per-node MFPT calculations for each attacked net (100 realisation per percentages per attack per species, i.e. 100 * 6 * 2 in total) of the new species using `{species_name}_net_{att}att_p{p}_{r}_r.txt` in ./outputs/Attacks/{att_u}/{species_name}/Relabel/ as network (network files) and the `{species_name}_colours_{att}att_p{p}_{r}_r.txt` in ./outputs/Attacks/{att_u}/{species_name}/Relabel/ (nodeid col files) that should have already been generated while doing step 3 of Fig4B-4C. 
- @Enzo: outputs should be saved in this format: `10^4_mfpt_{speciesname}_r{numofrealisation}_{att}worm_p{percentage}.txt`, where att must be either 'rnd' or 'egm' according to type of attack, and percentage must be '10', '20', '30', etc.  -->
- Run ResilienceCalculations.py
- Check that the following files has been created: `{species}_talfabeta.txt` in ./outputs/TauAlfaBetaAttacked/Real/ (for each species); `{species}_{attack.lower()}worm_p{perc}_talfabeta.txt` in ./outputs/TauAlfaBetaAttacked/Attacked/ (for each species, attack, percentage); `{species}_{attack.lower()}_resilience.txt` in ./outputs/Resilience/ (for each species, attack); `alluvial_data.csv` in ./outputs/Resilience/; `species_colors.txt` in ./outputs/Resilience/.  

4.
- Run Fig4B-4C.r
- Check that Fig4B-4C.pdf has been generated in ./generatedfigures folder.

### Fig4D

1. Follow steps 1-5 for Fig4B-C
2. Follow steps 1-5 for Fig2C-Fig2D
3.  
- Run Fig4D.py
- Check that the Fig4D.pdf has ben generated in generatedfigures
- Save the Kendall's Taus shown in the terminal

4. 
- Use .pdf and keynote in keynote folder to create Fig4D by mixing Fig4D.pdf, Kendall's Tau value and other components.

### FigS6

1. Follow steps 1-5 for Fig4B-C
2. 
- Run FigS6.py
- Check that FigS6.pdf has been generated in generatedfigures folder.

### TableS2
1. Follow steps 1-5 for Fig4B-C
2. Follow steps 1-5 for Fig2C-Fig2D
3. 
- Run TableS2.py
- Check that TableS2_part1.pdf, TableS2_part2.pdf and TableS2_part3.pdf has been generated in generatedfigures folder
- Merge together TableS2_part1.pdf, TableS2_part2.pdf and TableS2_part3.pdf to get TableS2 figure
