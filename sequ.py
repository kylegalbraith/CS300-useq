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
    stringParse = 0

    while stringParse < totalArgs:
        # Try to cast each argument to a float, if it works then we break out of the loop as we have hit the 
        # numerical portion of the args. Else continue parsing to see if the arg matches a flag.
        try:
            arguments[stringParse] = float(arguments[stringParse])
            break
        except ValueError:
            if arguments[stringParse] == "--help":
                usage(1)
            if arguments[stringParse] == "--version":
                usage(2)
            if arguments[stringParse] == "--format" or arguments[stringParse] == "-f":
                stringParse += 1
                try:
                    initialObj.formatOption = arguments[stringParse]
                except IndexError:
                    usage(4)
                print initialObj.formatOption 
            if arguments[stringParse] == "--seperator" or arguments[stringParse] == "-s":
                print "sep for string"
            if arguments[stringParse] == "--equal-width" or arguments[stringParse] == "-w":
                print "set equal-width"     
            stringParse += 1
    
    totalNumberArgs = totalArgs - stringParse
    numbers = []
    assert totalNumberArgs >= 1, "There are no numbers in here"
    
    if(totalNumberArgs <= 3):
        for x in range(stringParse, totalArgs):
            try:
                number = float(arguments[x])
                numbers.append(number)
            except ValueError:
                usage(3)
    else:
        usage(3)

    lengthOfNumbers = len(numbers)
    assert lengthOfNumbers < 4, "Error in number assignments"

    # Three different cases to consider for the numbers array. 3 numbers = start, step, and end need to be set. 2 numbers = start and end value need to be set. 1 number = just the end value needs to be set
    if(lengthOfNumbers == 3):
        initialObj.startValue = numbers[0]
        initialObj.step = numbers[1]
        initialObj.endValue = numbers[2]
        checkStartEnd(initialObj.startValue, initialObj.endValue)
    if(lengthOfNumbers == 2):
        initialObj.startValue = numbers[0]
        initialObj.endValue = numbers[1]
        checkStartEnd(initialObj.startValue, initialObj.endValue)
    if(lengthOfNumbers == 1):
        initialObj.endValue = numbers[0]

    checkFormat = initialObj.formatOption % initialObj.endValue
  
    return initialObj

# check if the start value > end value, if it is then exit without any output
def checkStartEnd (start, end):
    if start > end:
        exit(1)

# usage will be the initial error handling function so if the initial requirements are not met, print out the correct thing to do.
def usage(errorCode):
    
    assert type(errorCode) is IntType, "Error code not recognized"
    
    if(errorCode == 1):
        print 'Print help documentation'
        exit(1)
    elif(errorCode == 2):
        print 'Print version info'
        exit(1)
    elif(errorCode == 3):
        print 'sequ: extra operand'
        exit(1)
    elif(errorCode == 4):
        print 'Invalid format string. Use --help for more information.'
        exit(1)
    else:
        print 'ERROR - An unexpected error has ocurred'

# outputSeq will output the sequence between the integers passed in
def outputSeq(sequObj):
    start = sequObj.startValue
    end = sequObj.endValue

    while start <= end:
        print sequObj.formatOption % + start + sequObj.seperator,
        start += sequObj.step

    # The program was successful
    exit(0)

# Create a new sequ_obj which will have all of the defaults set for normal sequ operation.
initialObj = setup()
outputSeq(initialObj)




