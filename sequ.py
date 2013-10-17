#!/usr/bin/env python  

# Copyright (C) 2013 by Kyle Galbraith
# Kyle Galbraith - CS300 - useq compliance level 0

# Need sys to pass arguments in
import sys
import math
from sequ_obj import *

def setup():
    # Create a new sequ_obj which will have all of the defaults set for normal sequ operation.
    initialObj = sequ_obj()

    # Get the arguments that have been passed in, and ignore the first one since it is the invocation of the script
    arguments = sys.argv[1:len(sys.argv)]

    # Get the total args passed in as exactly 2 are required
    totalArgs = len(arguments)

    if totalArgs > 2 or totalArgs == 1 or totalArgs == 0:
        usage(1)

    for x in range(totalArgs):
        try:
            arguments[x] = float(arguments[x])
        except ValueError:
            usage(2)
    
    # Warn if arguments are not integers. Is there a fractional part.
    if not math.floor(arguments[0]) == arguments[0]:
        usage(3)
    if not math.floor(arguments[1]) == arguments[1]:
        usage(3)

    initialObj.startValue = int(arguments[0])
    initialObj.endValue = int(arguments[1])
    
    return initialObj

# usage will be the initial error handling function so if the initial requirements are not met, print out the correct thing to do.
def usage(errorCode):
    if(errorCode == 1):
        print 'ERROR - sequ requires exactly two integers'
        exit(1)
    elif(errorCode == 2):
        print 'ERROR - sequ CLO only accepts integer types'
        exit(1)
    elif(errorCode == 3):
        print 'WARNING - Start and end arguments should be integers'

# outputSeq will output the sequence between the integers passed in
def outputSeq(sequObj):
    start = sequObj.startValue
    end = sequObj.endValue
    
    # If the start is greater than the end then we just exit
    if start > end:
        exit(1)
    for x in range(start, end + 1):
        print x
    # The program was successful
    exit(0)

# Create a new sequ_obj which will have all of the defaults set for normal sequ operation.
initialObj = setup()
outputSeq(initialObj)




