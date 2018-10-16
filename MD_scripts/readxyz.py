#!/usr/bin/python

# Read first coordinates of the xyz trajectory file

# input: xyz coordinate file snapshot
# output: natom, atom (atom species), coord (coordinates )

def readsnapshot( lines ):
    natom = int( lines[0] )
    atom = []
    coord = []
    
    for i in range(2,natom+2):
        xyz = lines[i].split()
        atom.append( xyz[0] )
        coord.append( [float( xyz[1]), float(xyz[2]), float(xyz[3])] ) 

    return natom, atom, coord


def readsnapshot_coord( lines ):
    coord=[]
    for i in range( len(lines) ):
        line = lines[i].split()
        coord.append( [float(line[1]), float(line[2]), float(line[3])] )
    return coord
