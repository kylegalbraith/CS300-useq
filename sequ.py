#!/usr/bin/env python  

# Copyright (C) 2013 by Kyle Galbraith
# Kyle Galbraith - CS300 - sequ compliance level 1

# Need sys to pass arguments in
import sys
import math
import string
from types import *
from sequ_obj import *

# These are constants used throughout the program
SEQU_VERSION = "1.0"
SEQU_COPYRIGHT = "Copyright (C) 2013 Free Software Foundation, Inc."
SEQU_LICENSE = "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>. \nThis is free software: you are free to change and redistribute it. \nThere is NO WARRANTY, to the extent permitted by law."


def setup():
    # Create a new sequ_obj which will have all of the defaults set for normal sequ operation.
    initialObj = sequ_obj()

    assert initialObj.startValue == 1, "Start value was not initialized correctly"
    assert initialObj.endValue == 0, "End value was not initialized correctly"

    # Get the arguments that have been passed in, and ignore the first one since it is the invocation of the script
    arguments = sys.argv[1:len(sys.argv)]

    # Get the total args passed in as exactly 2 are required
    totalArgs = len(arguments)
    # loop variables. 
    # seenFormat = flag for we have seen the format flag
    # seenEw = flag for we have seen the equal-width
    stringParse = 0
    seenFormat = False
    seenEw = False

    while stringParse < totalArgs:
        # Try to cast each argument to a float, if it works then we break out of the loop as we have hit the 
        # numerical portion of the args. Else continue parsing to see if the arg matches a flag.
        try:
            float(arguments[stringParse])
            break
        except ValueError:
            if arguments[stringParse] == "--help":
                printHelp()
            if arguments[stringParse] == "--version":
                printVersion()
            if arguments[stringParse] == "--format" or arguments[stringParse] == "-f":
                stringParse += 1
                try:
                    if(seenEw == False):
                        initialObj.formatOption = arguments[stringParse]
                        seenFormat = True
                    else:
                        usage(6)
                except IndexError:
                    usage(4)
            if arguments[stringParse] == "--seperator" or arguments[stringParse] == "-s":
                stringParse += 1
                initialObj.seperator = arguments[stringParse]
                print arguments[stringParse]
            if arguments[stringParse] == "--equal-width" or arguments[stringParse] == "-w":
                if(seenFormat == False):
                    initialObj.equalWidth = True
                    seenEw = True
                else:
                    usage(6)  
            stringParse += 1   
  
    # Need to check that the number of args leftover is equal to or less than 3 but greater than 0
    totalNumberArgs = totalArgs - stringParse
    numbers = []
    numberStrings = []
    
    if(totalNumberArgs == 0):
        usage(5)
    
    if(totalNumberArgs <= 3):
        for x in range(stringParse, totalArgs):
            try:
                number = float(arguments[x])
                numberStrings.append(arguments[x])
                numbers.append(number)
            except ValueError:
                usage(3)
    else:
        usage(3)

    lengthOfNumbers = len(numbers)
    assert lengthOfNumbers < 4, "Error in number assignments"


    startValueString = ""
    stepValueString = ""
    endValueString = ""
    # Three different cases to consider for the numbers array. 3 numbers = start, step, and end need to be set. 2 numbers = start and end value need to be set. 1 number = just the end value needs to be set
    if(lengthOfNumbers == 3):
        initialObj.startValue = numbers[0]
        initialObj.step = numbers[1]
        initialObj.endValue = numbers[2]
        startValueString = numberStrings[0]
        stepValueString = numberStrings[1]
        endValueString = numberStrings[2]
        
        if(initialObj.step < 0):
            if(initialObj.startValue >= initialObj.endValue):
                initialObj.negativeStep = True
            else:
                exit(1)
        else:
            checkStartEnd(initialObj.startValue, initialObj.endValue)
    
    if(lengthOfNumbers == 2):
        initialObj.startValue = numbers[0]
        initialObj.endValue = numbers[1]
        checkStartEnd(initialObj.startValue, initialObj.endValue)
        startValueString = numberStrings[0]
        endValueString = numberStrings[1]
    if(lengthOfNumbers == 1):
        initialObj.endValue = numbers[0]
        endValueString = numberStrings[0]
    # end assigning start step end values

    # get the padding and setup format option for that, if equal-width is true we use 
    # a different format. If -f/--format was used then the default value for format will
    # not be present and this block of code will never run.
    if(initialObj.formatOption == "%g"):
        # need this code so if you enter fixed point arguments we can take the maximum number
        # of zeros from the arguments to use for the right of decimal.
        maxRightOfDecimal = 0
        if(len(numberStrings) > 1):
            for st in numberStrings:
                decimalIndex = st.find(".")
                if(decimalIndex > 0):
                    maxRightOfDecimal = max(maxRightOfDecimal, (len(st) - 1) - decimalIndex)    
                
        # variables to hold the number of places following '.' in the start value and step value
        startRightOfDecimal = 0
        stepRightOfDecimal = 0
        endRightOfDecimal = 0
        # get the remainder of the start and step value
        # if they are whole numbers they will 0, else they will be nonzero
        startRemainder = round(abs(initialObj.startValue % 1), 6)
        stepRemainder = round(abs(initialObj.step % 1), 6)
        if(startRemainder > 0):
            # doing floor to avoid floating point errors
            # There is a bug here in that if step remainder is 0.1 it could be interpreted as 0.09 which then causes startRightOfDecimal to be 2 instead of 1.
            # To resolve the problem I am adding 1 to the floor of the log of startRemaider
            startRightOfDecimal = -int(math.floor(math.log(startRemainder, 10)))
        if(stepRemainder > 0):
            stepRightOfDecimal = -int(math.floor(math.log(stepRemainder, 10)))

        if(maxRightOfDecimal > 0):
            rightOfDecimal = maxRightOfDecimal
        else:
            rightOfDecimal = max(startRightOfDecimal, stepRightOfDecimal)
               
        #if(initialObj.startValue <= 0):
            # If the startValue == 0 then we dont take the max, instead just use the endValue + 1 (the +1 is so we end up with the right # of 0's in this scenario)
            # seq -w 0 -1.1 -16.1
            #if(initialObj.endValue != 0):
         #       leftOfDecimal = -int(math.floor(math.log(abs(initialObj.endValue), 10)))
          #  else:
           #     leftOfDecimal = int(math.floor(math.log(abs(initialObj.step), 10)) + 1)
        #else:
        leftOfDecimal = int(math.floor(math.log(max(abs(initialObj.startValue), abs(initialObj.endValue)), 10)))

        if(initialObj.startValue < 0 or initialObj.endValue < 0):
            print 'got called'
            leftOfDecimal = leftOfDecimal + 1

        # added this on 11/5/13        
        if(leftOfDecimal == 0):
           print 'lod == 0'
           leftOfDecimal = leftOfDecimal + 1
        
        if(rightOfDecimal > 0):
            leftOfDecimal = leftOfDecimal + 1
        
        if(initialObj.equalWidth):
            initialObj.formatOption = "%0" + str(leftOfDecimal + rightOfDecimal + 1) + "." + str(rightOfDecimal) + "f"
        else:
            initialObj.formatOption = "%0." + str(rightOfDecimal) + "f"

        print initialObj.formatOption

    # double check the format option to make sure it is is valid. The likely case where
    # format option is invalid is when the user has used -f/--format
    try:
        checkFormat = initialObj.formatOption % initialObj.endValue
    except ValueError:
        usage(2, initialObj.formatOption)


    return initialObj

# check if the start value > end value, if it is then exit without any output
def checkStartEnd (start, end):
    if start > end:
        exit(1)

# usage will be the initial error handling function so if the initial requirements are not met, print out the correct thing to do.
def usage(errorCode, error=""):
    
    assert type(errorCode) is IntType, "Error code not recognized"
    helpString = '\nTry \'sequ --help\' for more information.'

    if(errorCode == 2):
        print 'sequ: format ' + "'" + error + "'" + ' has unknown ' + error + ' directive' 
        exit(1)
    elif(errorCode == 3):
        print 'sequ: extra operand' + helpString 
        exit(1)
    elif(errorCode == 4):
        print 'Invalid format string. Use --help for more information.'
        exit(1)
    elif(errorCode == 5):
        print 'sequ: missing operand' + helpString
        exit(1)
    elif(errorCode == 6):
        print 'sequ: format string may not be used when printing equal width strings' + helpString
        exit(1)
    else:
        print 'ERROR - An unexpected error has ocurred'

# print help information
def printHelp():
    print 'help information'
    exit(0)

def printVersion():
    print 'sequ (CS300 Term Project) ' + SEQU_VERSION + '\n' + SEQU_COPYRIGHT + '\n' + SEQU_LICENSE + '\n\n' + 'Written by Kyle Galbraith.'
    exit(0)

# outputSeq will output the sequence between the integers passed in
def outputSeq(sequObj):
    start = sequObj.startValue
    end = sequObj.endValue
    step = sequObj.step
    negativeStep = sequObj.negativeStep

    if(negativeStep):
        while start >= end:
            print sequObj.formatOption % + start + sequObj.seperator,
            start += step
    else:
        while start <= end:
            print sequObj.formatOption % + start + sequObj.seperator,
            start += step    

    # The program was successful
    exit(0)

# Create a new sequ_obj which will have all of the defaults set for normal sequ operation.
initialObj = setup()
outputSeq(initialObj)




