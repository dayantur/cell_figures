import os

real=98

f=open("./4flip_MFPT_deltadistances.txt", "w")
for n in range (0, real):
    with open ("./data/MFPT_quadrupleflip_data_"+str(n)+".txt") as fp:
        for line in fp:
            f.write("%s" % line)
f.close()
