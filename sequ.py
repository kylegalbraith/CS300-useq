#!/usr/bin/env python  

# Copyright (C) 2013 by Kyle Galbraith
# Kyle Galbraith - CS300 - sequ compliance level 1

# Need sys to pass arguments in
import sys
import math
from types import *
from sequ_obj import *

def setup():
    # Create a new sequ_obj which will have all of the defaults set for normal sequ operation.
    initialObj = sequ_obj()

    assert initialObj.startValue == 0, "Start value was not initialized correctly"
    assert initialObj.endValue == 0, "End value was not initialized correctly"

    # Get the arguments that have been passed in, and ignore the first one since it is the invocation of the script
    arguments = sys.argv[1:len(sys.argv)]

    # Get the total args passed in as exactly 2 are required
    totalArgs = len(arguments)
    parameterLoop = 0

    while parameterLoop < totalArgs and isinstance(arguments[parameterLoop], basestring):
        if arguments[parameterLoop] == "--help":
            print "Go To Help"
        if arguments[parameterLoop] == "--format" or arguments[parameterLoop] == "-f":
            print "format"
        parameterLoop += 1
        
    #if totalArgs > 2 or totalArgs == 1 or totalArgs == 0:
     #   usage(1)

    for x in range(totalArgs):
        try:
            arguments[x] = float(arguments[x])
        except ValueError:
            usage(2)
    
    assert type(arguments[0]) is FloatType, "Argument one was not casted as a float"
    assert type(arguments[1]) is FloatType, "Argument two was not casted as a float"
    
    initialObj.startValue = arguments[0]
    initialObj.endValue = arguments[1]
 
    return initialObj

# usage will be the initial error handling function so if the initial requirements are not met, print out the correct thing to do.
def usage(errorCode):
    
    assert type(errorCode) is IntType, "Error code not recognized"
    
    if(errorCode == 1):
        print 'ERROR - sequ requires exactly two integers'
        exit(1)
    elif(errorCode == 2):
        print 'ERROR - sequ CLO only accepts integer types'
        exit(1)
    elif(errorCode == 3):
        print 'WARNING - Start and end arguments should be integers'
    else:
        print 'ERROR - An unexpected error has ocurred'

# outputSeq will output the sequence between the integers passed in
def outputSeq(sequObj):
    start = sequObj.startValue
    end = sequObj.endValue
    
    # If the start is greater than the end then we just exit
    if start > end:
        exit(1)
    while start <= end:
        print sequObj.formatOption % + start + sequObj.seperator,
        start += sequObj.step

    #for x in range(dist + 1):
        #outputStr = float(x)
        #print sequObj.format % + outputStr + sequObj.seperator,
    # The program was successful
    exit(0)

# Create a new sequ_obj which will have all of the defaults set for normal sequ operation.
initialObj = setup()
outputSeq(initialObj)




