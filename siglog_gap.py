#!/usr/bin/python

import sys

if len(sys.argv) != 2:
    sys.stderr.write("\n Usage: " + sys.argv[0] + " sigma.log \n\n")
    sys.exit()

# open files
f = open(sys.argv[1])
slurp = f.readlines()
f.close()

# number of bands printed in log file
numband = 4
evmax = 2
ecmin = 3
#print "index for band gap calculation"
#print "number of bands: ", numband, "Evmax: ", evmax, "Ecmin: ", ecmin 

# counts number of k points
numk = 0
for i in range( len(slurp) ):
    if slurp[i].find("k =  ") >= 0:
        numk = numk + 1

#print "number of k points: ", numk
        
# collect energies
# band index
n=[]
# quasiparticle energies
eqp=[]
for i in range( len(slurp) ):
    if slurp[i].find("n     elda") >= 0:
        # initialize
        kn=[] # band index at this k point
        keqp=[] # quasi-particle energy at this k point
        for j in range(1,numband+1):
            lsplit = slurp[i+j].split()
            kn.append( int( lsplit[0] ) )
            keqp.append( float( lsplit[-2] ) )
        # adding kn and keqp to n and eqp
        n.append(kn)
        eqp.append(keqp)


# find highest occupied and lowest unoccupied states
evmaxqp = -10000
ecminqp = 10000
for i in range( numk ):
    #print eqp[i]
    if evmaxqp < eqp[i][evmax-1]:
        evmaxqp = eqp[i][evmax-1]

    if ecminqp > eqp[i][ecmin-1]:
        ecminqp = eqp[i][ecmin-1]

#print "Evmax: " , evmaxqp
#print "Ecmin: " , ecminqp
print "Egap: " , ecminqp - evmaxqp
