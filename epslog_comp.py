#!/usr/bin/python

# Sometimes I have to compare values to check the convergence
# So I wanted to make this script to easy compare two files
# This script works for BerkeleyGW epsilon.log file

import re
from collections import deque

# First thing first, we need two files of epsilon.log
# set filename manually

fname1 = "epsilon.log_2"
fname2 = "epsilon.log_12"

try:
    f1 = open(fname1)
    f2 = open(fname2)
except: 
    print "Check the file name. Current file name is :", fname1, fname2

# define a function that reads and saves g, gp, and inverse epsilon
# input option: f (filename), q (qpt index)
def read_inveps(f,q):
    s = f.readlines()
    s = deque(s)
    qcount = 0
    g = []
    gp = []
    ieps = []
    while len(s) > 0:
        l = s.popleft()
        if qcount > q:
            break
        if qcount == q:
            sp = l.split()
            if len(sp) == 7:
                gvec=[ int(sp[0]), int(sp[1]), int(sp[2]) ]
                g.append( gvec )
                gvec = [ int(sp[3]), int(sp[4]), int(sp[5]) ]
                gp.append( gvec)
                ieps.append( float(sp[-1]) )
            if len( sp ) == 0:
                break
        if l.find("inverse epsilon") >=0:
            qcount = qcount + 1
    return g, gp, ieps


q1=2
q2=2
g1 = []
gp1 = []
ieps1 = []
g2 = []
gp2 = []
ieps2 = []

g1, gp1, ieps1 = read_inveps(f1,q1)
g2, gp2, ieps2 = read_inveps(f2,q2)
f1.close()
f2.close()


for i1 in range( len(g1) ):
    for i2 in range( len(g2) ):
        
        if g1[i1]==g2[i2] and gp1[i1]==gp2[i2]:
            print g1[i1], gp1[i1], ieps1[i1], ieps2[i2]
            break
