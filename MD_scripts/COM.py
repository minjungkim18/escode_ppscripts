#!/usr/bin/python

# input: xyz MD trajectory file

# This script creates data files for COM plots
# The trajectory file may be very large. Instead of saving the entire lines,
# each snapshot is being processed while reading the file.

# variable description
# natom : number of total atom at each snapshot of xyz file
# atom[natom] : atom species (e.g., H, He, Li, Be, ...)
# step0 : The first snapshot coordinates (used to find H2 pair index)
# num_H: total numer of H atom in one snapshot
# H_index[num_H] : H atom index
# num_H2pair : number of H2 molecules
# H2pair[num_H2pair][2] : indexes of two H atoms in H2 molecule
# thisstep_COM[num_H2pair][3] : coordinates of center of mass for each H2 molecule
# total_COM[total_num_step][num_H2pair][3] : COM for all step


import sys
import readxyz
import mymath

# Open trajectory file (xyz format) for reading
try:
    filename = sys.argv[1]
    natom = int( sys.argv[2] )
except: 
    print 'Usage: ./COM.py trajectory_file number_of_atom'
    sys.exit(1)

# read the first snapshot and save to "head"
print '\nReading first snapshot and find H2 pairs...'
with open(filename,'r') as f:
    head = [next(f) for x in xrange(natom+2)] 
    
atom=[]
step0=[] # dimension of step0 = [natom][3]
natom, atom, step0 = readxyz.readsnapshot( head )

# purpose of this script is to get COM of H2 molecule
# we want to find which H atom bonds to another H atom
# this is done with the first 

# In our run, there are two kinds of H atom, which is H and H0
# to make it simple, change H0 to H
for i in range(natom):
    if atom[i] == 'H0':
        atom[i] = 'H'

# let's save the index of H atom
counter=0
H_index=[]
for i in range(natom):
    if atom[i] == 'H':
        counter += 1
        H_index.append( i )
        
num_H = len(H_index)
counter = 0
H2pair=[]
H2cut = 1.2
print '\nCutoff value for H2 bonding:', H2cut , 'angstrom'
for i in range(num_H-1):
    index1 = H_index[i]
    H1 = step0[index1][:]
    for j in range(i+1,num_H):
        index2 = H_index[j]
        H2 = step0[index2][:]
        d = mymath.norm(H1, H2)
        #print d
        if d < H2cut:
            H2pair.append( [index1, index2] )
print '\nH2 pair index:', H2pair
num_H2pair = len(H2pair[:])

print '\nInitial Setup complete'
print '\nTotal number of H2 pair: ',num_H2pair
#sys.exit(1)

# function for center_of_mass
def center_of_mass( H2pair, coord ):
    num_H2pair = len(H2pair[:])
    COMcoord=[]
    for i in range(num_H2pair):
        H1index=H2pair[i][0]
        H2index=H2pair[i][1]
        H1=coord[H1index][:]
        H2=coord[H2index][:]
        # make sure if the two H atoms are bonded
        d = mymath.norm(H1,H2)
        if d > 1.2:
            print 'WARNING: Your H2',H1index,H2index,'seems dissociated, bond length=',d,'angstrom'
        Hcom = mymath.average(H1,H2)
        COMcoord.append(Hcom)
    return COMcoord


# Now we read files until hit the EOF
step = 0
counter = 0
total_COM=[]
with open(filename,'r') as f:
    while True:
        line=f.readline()
        if not line: break
        step += 1
        print 'Step:',step
        line=f.readline()
        block=[]
        for i in range(natom):
            block.append( f.readline() )
        coord=readxyz.readsnapshot_coord(block)
        # now we find the center of mass
        thisstep_COM = center_of_mass( H2pair, coord )
        total_COM.append(thisstep_COM)

#print total_COM
#sys.exit(1)


# File is written for MatLAB plot
outfilename='T300_FullMOF_COM.dat'
with open(outfilename,'w') as f:
    for i in range(step):
        for j in range(num_H2pair):
            xyz=total_COM[i][j]
            if j < num_H2pair-1:
                f.write('%f %f %f ' % (float(xyz[0]),float(xyz[1]),float(xyz[2])) )
            if j == num_H2pair-1:
                f.write('%f %f %f\n' % (float(xyz[0]),float(xyz[1]),float(xyz[2])) )
