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
    # numbers is an array of floats
    numbers = []
    # numberStrings is an array of strings that represent the float
    numberStrings = []
    
    # No numbers were passed in
    if(totalNumberArgs == 0):
        usage(5)
    
    if(totalNumberArgs <= 3):
        for x in range(stringParse, totalArgs):
            try:
                number = float(arguments[x])
                # if the argument can be casted to a float, then push the string representation of the argument into the string array
                numberStrings.append(arguments[x])
                numbers.append(number)
            except ValueError:
                usage(3)
    # There is more than 3 arguments, meaning there is an extra operand
    else:
        usage(3)

    lengthOfNumbers = len(numbers)
    assert lengthOfNumbers < 4, "Error in number assignments"

    # These will store the string representation of start, step, and end values so we can count the places in each
    startValueString = ""
    stepValueString = ""
    endValueString = ""
    # Three different cases to consider for the numbers array. 
    # 3 numbers = start, step, and end need to be set
    # 2 numbers = start and end value need to be set
    # 1 number = just the end value needs to be set
    if(lengthOfNumbers == 3):
        initialObj.startValue = numbers[0]
        initialObj.step = numbers[1]
        initialObj.endValue = numbers[2]
        startValueString = numberStrings[0]
        stepValueString = numberStrings[1]
        endValueString = numberStrings[2]
        
        if(initialObj.step < 0):
            if(checkNegStepEnd(initialObj.startValue, initialObj.endValue)):
                initialObj.negativeStep = True
        else:
            # If start > end then just exit, nothing to output
            checkStartEnd(initialObj.startValue, initialObj.endValue)
    
    if(lengthOfNumbers == 2):
        initialObj.startValue = numbers[0]
        initialObj.endValue = numbers[1]
        startValueString = numberStrings[0]
        endValueString = numberStrings[1]
                
        # If start > end then just exit, nothing to output
        checkStartEnd(initialObj.startValue, initialObj.endValue)

    if(lengthOfNumbers == 1):
        initialObj.endValue = numbers[0]
        endValueString = numberStrings[0]
    # end assigning start step end values

    # TODO: Refactor the code below into their own functions so that this is much cleaner looking
    # If -f/--format was used then the default value for format will not be present and this block of code will never run.
    if(initialObj.formatOption == "%g"):
        # need this code so if start, step, and end are all fixed point arguments we can take the maximum number
        # of zeros from the arguments to use for the right of decimal.
        # This will return the maximum number of places behind the decimal point
        fixedPointRightOfDecimal = getMaxFixedPointRightOfDecimal(numberStrings)
        
        if(fixedPointRightOfDecimal > 0):
            rightOfDecimal = fixedPointRightOfDecimal
        else:
            rightOfDecimal = calculateRightOfDecimal(initialObj.startValue, initialObj.step)  
                
        ## variables to hold the number of places following '.' in the start value and step value
        #startRightOfDecimal = 0
        #stepRightOfDecimal = 0
        #endRightOfDecimal = 0
        ## get the remainder of the start and step value
        ## if they are whole numbers they will 0, else they will be nonzero
        #startRemainder = round(abs(initialObj.startValue % 1), 6)
        #stepRemainder = round(abs(initialObj.step % 1), 6)
        #if(startRemainder > 0):
        #    # doing floor to avoid floating point errors
        #    # There is a bug here in that if step remainder is 0.1 it could be interpreted as 0.09 which then causes startRightOfDecimal to be 2 instead of 1.
        #    # To resolve the problem I am adding 1 to the floor of the log of startRemaider
        #    startRightOfDecimal = -int(math.floor(math.log(startRemainder, 10)))
        #if(stepRemainder > 0):
        #    stepRightOfDecimal = -int(math.floor(math.log(stepRemainder, 10)))

        #if(maxPlacesRightOfDecimal > 0):
         #   rightOfDecimal = maxPlacesRightOfDecimal
        #else:
         #   rightOfDecimal = max(startRightOfDecimal, stepRightOfDecimal)
               
        #if(initialObj.startValue <= 0):
            # If the startValue == 0 then we dont take the max, instead just use the endValue + 1 (the +1 is so we end up with the right # of 0's in this scenario)
            # seq -w 0 -1.1 -16.1
            #if(initialObj.endValue != 0):
         #       leftOfDecimal = -int(math.floor(math.log(abs(initialObj.endValue), 10)))
          #  else:
           #     leftOfDecimal = int(math.floor(math.log(abs(initialObj.step), 10)) + 1)
        #else:
        leftOfDecimal = calculateLeftOfDecimal(initialObj.startValue, initialObj.endValue)

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

# If the args are not all fixed point then we will need to calculate how many places we need for output.
# This gives us the output format for %0.pf by calculating p and also the right hand side if -w is used
def calculateRightOfDecimal(startValue, stepValue):
    # variables to hold the number of places following '.' in the start
    # value and step value
    startRightOfDecimal = 0
    stepRightOfDecimal = 0
    endRightOfDecimal = 0
    # get the remainder of the start and step value
    # if they are whole numbers they will 0, else they will be nonzero
    startRemainder = round(abs(startValue % 1), 6)
    stepRemainder = round(abs(stepValue % 1), 6)
    
    if(startRemainder > 0):
        # doing floor to avoid floating point errors
        # There is a bug here in that if step remainder is 0.1 it could be
        # interpreted as 0.09 which then causes startRightOfDecimal to be 2
        # instead of 1.
        # To resolve the problem I am adding 1 to the floor of the log of
        # startRemaider
        startRightOfDecimal = -int(math.floor(math.log(startRemainder, 10)))
    
    if(stepRemainder > 0):
        stepRightOfDecimal = -int(math.floor(math.log(stepRemainder, 10)))
     
    return max(startRightOfDecimal, stepRightOfDecimal) 

# calculate the number of places needed to the left of the decimal
def calculateLeftOfDecimal(startValue, endValue):
    #int(math.floor(math.log(max(abs(initialObj.startValue), abs(initialObj.endValue)), 10)))
    
    absoluteStart = abs(startValue)
    absoluteEnd = abs(endValue)
    largest = max(absoluteStart, absoluteEnd)
    logOfLargestValue = math.log(largest, 10)
    floorLog = math.floor(logOfLargestValue)

    return int(floorLog)  

# Returns the maximum number of places to the right of decimal. Need this for the case where all 3 args are fixed point
def getMaxFixedPointRightOfDecimal(numberStrings):
    maxRightOfDecimal = 0
    if(len(numberStrings) > 1):
        for floatString in numberStrings:
            decimalIndex = floatString.find(".")
            if(decimalIndex > 0):
                maxRightOfDecimal = max(maxRightOfDecimal, (len(floatString) - 1) - decimalIndex)
    return maxRightOfDecimal 

# check if the start value > end value, if it is then exit without any output
def checkStartEnd (start, end):
    if start > end:
        exit(1)

# If the step < 0 then start must be >= end to output things in the correct order, else just exit.
def checkNegStepEnd(start, end):
    if(start >= end):
        return True
    else:
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




