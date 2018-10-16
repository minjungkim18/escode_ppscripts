#!/usr/bin/python

# some basic mathematical functions that makes my life easier
# you probably need to learn numpy as it seems to have a lot of mathematical functions
# but for fast script writing, I'm just writing my own


import sys
import math

# norm = ||a - b||
# both a and b is an 1D array with same length
def norm( a, b ):
    if len(a) != len(b):
        print 'Error while calling norm: size of vector a and vector b do not match'
        sys.exit(1)
    n = len(a)
    sqrt = 0
    for i in range(n):
        sqrt += (a[i]-b[i])*(a[i]-b[i])
    sqrt = math.sqrt( sqrt )
    return sqrt


# find the average value of two vector
def average( a, b):
    if len(a) != len(b):
        print 'Error while calling average: size of vector a and vector b do not match'
        sys.exit(1)
    n = len(a)
    c=[]
    for i in range(n):
        c.append( (a[i]+b[i])*0.5 ) 
    return c
