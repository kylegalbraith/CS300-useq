#!/usr/bin/env python  

# Copyright (C) 2013 by Kyle Galbraith
# Kyle Galbraith - CS300 - sequ compliance level 1

# Need sys to pass arguments in
import sys
import math
import string
from types import *
from sequ_obj import *
import argparse

# These are constants used throughout the program
SEQU_VERSION = "1.0"
SEQU_COPYRIGHT = "Copyright (C) 2013 Free Software Foundation, Inc."
SEQU_LICENSE = "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>. \nThis is free software: you are free to change and redistribute it. \nThere is NO WARRANTY, to the extent permitted by law."
SEQU_HELP = "Usage: \n\tsequ [OPTION]... LAST\n\tsequ [OPTION]... FIRST LAST\n\tsequ [OPTION]... FIRST INCREMENT LAST\nPrint numbers from FIRST to LAST, in steps of INCREMENT.\n\n\t-f, --format=FORMAT\tuse printf style floating-point FORMAT (%a is not supported)\n\t-s, --separator=STRING\tuse STRING to separate numbers (default: \\n)\n\t-w, --equal-width\tequalize width by padding with leading zeroes\n\t--help\tdisplay this help and exit\n\t--version\tdisplay version info and exit\n\nIf FIRST or INCREMENT is omitted, it defaults to 1. That is,\nan omitted INCREMENT defaults to 1 even when LAST is smaller than FIRST.\nFIRST, INCREMENT, and LAST are interpreted as floating point values.\nINCREMENT is usually positive if FIRST is smaller than LAST, and\nINCEREMENT is usually negative if FIRST is greater than LAST.\nFORMAT must be suitable for printing one argument of type 'float';\nit defaults to %.precf if FIRST, INCREMENT, and LAST are all fixed point\ndecimal numbers with maximum precision prec, and %g otherwise."

# usage will be the initial error handling function so if the initial requirements are not met, print out the correct thing to do.
def usage(errorCode, error=""):
    
    assert type(errorCode) is IntType, "Error code not recognized"
    helpString = '\nTry \'sequ --help\' for more information.'

    if(errorCode == 1):
        print 'sequ: format ' + "'" + error + "'" + ' has no % directive' 
        exit(1)
    elif(errorCode == 2):
        print 'sequ: format ' + "'" + error + "'" + ' has unknown ' + error + ' directive' 
        exit(1)
    elif(errorCode == 3):
        print 'sequ: extra operand ' + "'" + error + "'" + helpString 
        exit(1)
    elif(errorCode == 4):
        print 'sequ: option ' + "'" + error + "'" + ' requires an argument' + helpString
        exit(1)
    elif(errorCode == 5):
        print 'sequ: missing operand' + helpString
        exit(1)
    elif(errorCode == 6):
        print 'sequ: \'--equal-width\' flags (--pad, --pad-spaces) are distinct flags cannot be used with one another or with \'--format\'' + helpString
        exit(1)
    elif(errorCode == 7):
        print 'sequ: unrecognized option ' + "'" + error + "'"
        exit(1)
    elif(errorCode == 8):
        print 'sequ: \'--separator\' cannot be used with \'--words\''
        exit(1)
    elif(errorCode == 9):
        print 'sequ: \'--pad\' requires a single character pad' + helpString
        exit(1)
    else:
        print 'ERROR - An unexpected error has ocurred'

def setup():
    # Create a new sequ_obj which will have all of the defaults set for normal sequ operation.
    initialObj = sequ_obj()

    assert initialObj.startValue == 1, "Start value was not initialized correctly"
    assert initialObj.step == 1, "Step value was not initialized correctly" 
    assert initialObj.endValue == 0, "End value was not initialized correctly"
    assert initialObj.equalWidth == False, "Equal width boolean was not initialized correctly"
    assert initialObj.negativeStep == False, "Negative step was not initialized correctly"
    assert initialObj.separator == '\n', "Default separator not set correctly"

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

    #parser = argparse.ArgumentParser()
    #parser.add_argument("--version", nargs='?', help="print version info")
    #parser.add_argument("-f", "--format", nargs='?', help="format options" )
    #parser.add_argument("-s", "--separator", nargs='?', help="separator info")
    #parser.add_argument("-w", "--equal-width", nargs='?', help="equal width info")
    #parser.add_argument("start", type=float, help="start value")
    #parser.add_argument("increment", type=float, nargs='?', help="step value")
    #parser.add_argument("end", type=float, nargs='?', help="end value")
    #args = parser.parse_args()
    #if(args.increment):
     #   print args.increment
    #if(args.end):
     #   print args.end


    while stringParse < totalArgs:
        # Try to cast each argument to a float, if it works then we break out of the loop as we have hit the 
        # numerical portion of the args. Else continue parsing to see if the arg matches a flag.
        try:
            float(arguments[stringParse])
            break
        except ValueError:
            formatVerboseSub = "--format" in arguments[stringParse]
            formatSub = "-f" in arguments[stringParse]
            format = formatVerboseSub or formatSub

            separatorVerboseSub = "--separator" in arguments[stringParse]
            separatorSub = "-s" in arguments[stringParse]
            separator = separatorVerboseSub or separatorSub

            padVerboseSub = "--pad" in arguments[stringParse]
            padSub = "-p" in arguments[stringParse]
            pad = padVerboseSub or padSub

            if arguments[stringParse] == "--help":
                printHelp()
            elif arguments[stringParse] == "--version":
                printVersion()

            elif arguments[stringParse] == "--pad-spaces" or arguments[stringParse] == "-P":
                if(seenFormat == False and seenEw == False):
                    initialObj.equalWidth = True
                    initialObj.padChar = ' '
                    seenEw = True
                else:
                    usage(6)

            elif arguments[stringParse] == "--equal-width" or arguments[stringParse] == "-w":
                if(seenFormat == False and seenEw == False):
                    initialObj.equalWidth = True
                    seenEw = True
                else:
                    usage(6)

            elif arguments[stringParse] == "--words" or arguments[stringParse] == "-W":
                if(initialObj.separator == '\n'):
                    initialObj.separator = ' '
                else:
                    usage(8)
            
            elif format:               
                try:
                    if(seenEw == False):                       
                        verboseFormatLength = len("--format")
                        formatFlagLength = len("-f")
                        argumentLength = len(arguments[stringParse])            
                        
                        # There is no = behind the flag so we can assume that the format is the next place on the command line
                        if(argumentLength == verboseFormatLength or argumentLength == formatFlagLength):
                            stringParse += 1
                            if "%" in arguments[stringParse]:
                                initialObj.formatOption = arguments[stringParse]
                                seenFormat = True
                            else:
                                usage(1, arguments[stringParse])
                        # Need to parse the flag to find where the actual
                        # format is
                        else:
                            parsedFormat = parseFormat(arguments[stringParse])
                            if "%" in parsedFormat:
                                initialObj.formatOption = parsedFormat 
                                seenFormat = True
                            else:
                                usage(1, parsedFormat)                                                                                                                     
                    else:
                        usage(6)
                except IndexError:
                    usage(4, "--format")

            elif separator:
                if(initialObj.separator == '\n'):
                    try:
                        verboseSeparatorLength = len("--separator")
                        separatorFlagLength = len("-s")
                        argumentLength = len(arguments[stringParse])

                        if(argumentLength == verboseSeparatorLength or argumentLength == separatorFlagLength):
                            stringParse += 1
                            initialObj.separator = arguments[stringParse].decode("string_escape") 
                        else:
                            parsedEscapedSeparator = parseFlagWithEquals(arguments[stringParse], verboseSeparatorLength, separatorFlagLength)
                            initialObj.separator = parsedEscapedSeparator

                    except IndexError:
                        usage(4, "--separator")
                else:
                    usage(8)

            elif pad:
                # Check the length of the single character passed in to make sure that
                # it is a single character. Then Run equal-width check and then replace 
                # the 0s with the single character passed in.
                if(seenEw == False and seenFormat == False):
                    try:
                        padVerboseLength = len("--pad")
                        padFlagLength = len("-p")
                        argumentLength = len(arguments[stringParse])

                        if(argumentLength == padVerboseLength or argumentLength == 2):
                            stringParse += 1
                            padCharacter = arguments[stringParse].decode("string_escape")
                           
                            if(len(padCharacter) == 1):
                                initialObj.equalWidth = True
                                initialObj.padChar = padCharacter
                                seenEw = True
                            else:
                                usage(9)
                            # Check the pad character to escape / and to make sure its length == 1
                            # If that checks out then put the character on the sequ object and set seenEw to true
                        else:
                            # need to parse what is behind the = sign
                            parsedEscapedPad = parseFlagWithEquals(arguments[stringParse], padVerboseLength, padFlagLength)
                            if(len(parsedEscapedPad) == 1):
                                initialObj.equalWidth = True
                                initialObj.padChar = parsedEscapedPad
                                seenEw = True
                            else:
                                usage(9)

                    except IndexError:
                        usage(4, "--pad")
                else:
                    usage(6)
            else:
                usage(7, arguments[stringParse])
                      
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
        usage(3, arguments[4])

    lengthOfNumbers = len(numbers)

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

    # If -f/--format was used then the default value for format will not be present and this block of code will never run.
    if(initialObj.formatOption == "%g"):
        initialObj.leftDecimal = getLeftOfDecimal(numberStrings, initialObj.startValue, initialObj.step, initialObj.endValue)
        initialObj.rightDecimal = getRightOfDecimal(numberStrings, initialObj.startValue, initialObj.step)
        # Create the format option needed based on the number of places to the left and right of the decimal
        initialObj.formatOption = createFormatOption(initialObj.leftDecimal, initialObj.rightDecimal, initialObj.equalWidth)

    # double check the format option to make sure it is is valid. The likely case where
    # format option is invalid is when the user has used -f/--format
    try:
        checkFormat = initialObj.formatOption % initialObj.endValue
    except ValueError:
        usage(2, initialObj.formatOption)

    return initialObj

# Get the number of places we need for left of the decimal. If fixed point > 0 then we will just use that for left of decimal.
# Otherwise need to go calculate the number of places left of decimal
def getLeftOfDecimal(numberStrings, startValue, stepValue, endValue):
    startRem = startValue % 1
    stepRem = stepValue % 1
    endRem = endValue % 1

    fixedPointLeftOfDecimal = getMaxFixedPointLeftOfDecimal(numberStrings)

    if(fixedPointLeftOfDecimal > 0):
        leftOfDecimal = fixedPointLeftOfDecimal
        checkRem = startRem > 0 or stepRem > 0 or endRem > 0
        if(not checkRem):
            leftOfDecimal = leftOfDecimal - 1
    else:
        leftOfDecimal = calculateLeftOfDecimal(startValue, endValue)   
        if(startValue <= 0 and endValue <= 0):
            leftOfDecimal = leftOfDecimal + 1
        # 11/17/13 no longer need the checks below because I check for largest > 1 in calculateLeftOfDecimal
        #if(startValue > 0 and endValue < 0):
         #   leftOfDecimal = leftOfDecimal + 1
        #elif(startValue < 0 and endValue > 0 or rightOfDecimal > 0):
         #   leftOfDecimal = leftOfDecimal + 1
    
    return leftOfDecimal

# Get the number of decimal places to the right of the decimal. If fixed point > 0 then use that, otherwise go calculate the right of decimal
def getRightOfDecimal(numberStrings, startValue, stepValue):
    fixedPointRightOfDecimal = getMaxFixedPointRightOfDecimal(numberStrings)

    if(fixedPointRightOfDecimal > 0):
        rightOfDecimal = fixedPointRightOfDecimal
    else:
        rightOfDecimal = calculateRightOfDecimal(startValue, stepValue)

    return rightOfDecimal
     

# create format option will create the format option based on how many places are needed
# left of decimal and right of decimal. The format option needed will also depend on whether 
# --equal-width has been passed in
def createFormatOption(leftOfDecimal, rightOfDecimal, ewFlag):
    formatOption = ""
               
    if(ewFlag):
        formatOption = "%0" + str(leftOfDecimal + rightOfDecimal + 1) + "." + str(rightOfDecimal) + "f"
    else:
        formatOption = "%0." + str(rightOfDecimal) + "f"

    return formatOption

# parse the passed in separator argument into a valid format
def parseFlagWithEquals(argumentString, verboseSepLength, sepFlagLength):
    argumentLength = len(argumentString)
    passedSeparator = argumentString
    startHere = passedSeparator.find('=')
    appendString = ""
    parsedSeparator = ""
    # If there is no equals then grab everything behind the arguments
    if(startHere == -1):
        # See if we need to grab the data behind -s or behind --separator
        greaterThanFlag = argumentLength > sepFlagLength
        lessThanVerbose = argumentLength < verboseSepLength

        if(greaterThanFlag and lessThanVerbose):
            for x in range(sepFlagLength, argumentLength):
                appendString += passedSeparator[x]
            parsedSeparator = appendString.decode("string_escape")
        else:
            usage(7, passedSeparator)
    else:
        for x in range(startHere + 1, argumentLength):
            appendString += passedSeparator[x]  
        parsedSeparator = appendString.decode("string_escape")
        
    return parsedSeparator

# parse the format argument after the = into a valid format
def parseFormat(argumentString):
    argumentLength = len(argumentString)
    
    formatString = argumentString
    startHere = formatString.find('=') + 1
    appendString = ""
    for x in range(startHere, argumentLength):
        appendString += formatString[x]
    
    return appendString
  
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
        startRightOfDecimal = -int(math.floor(math.log(startRemainder, 10)))
    
    if(stepRemainder > 0):
        stepRightOfDecimal = -int(math.floor(math.log(stepRemainder, 10)))
     
    return max(startRightOfDecimal, stepRightOfDecimal) 

# calculate the number of places needed to the left of the decimal in case fixed point is not > 0
def calculateLeftOfDecimal(startValue, endValue):
    
    absoluteStart = abs(startValue)
    absoluteEnd = abs(endValue)
    largest = max(absoluteStart, absoluteEnd)
    # 11/17/13 Changed this to be largest > 1 to account for -w -1 1 1 and -w -1 10
    if(largest > 1):
        logOfLargestValue = math.log(largest, 10)
    else:
        logOfLargestValue = 1
    floorLog = math.floor(logOfLargestValue)

    return int(floorLog)  

# Returns the maximum number of places to the right of decimal. Need this for the case where all 3 args are fixed point
def getMaxFixedPointRightOfDecimal(numberStrings):
    maxRightOfDecimal = 0
    if(len(numberStrings) > 1):
        for floatString in numberStrings:
            decimalIndex = floatString.find(".")
            # Off by one error on 11/10/13
            if(decimalIndex >= 0):
                maxRightOfDecimal = max(maxRightOfDecimal, (len(floatString) - 1) - decimalIndex)
    return maxRightOfDecimal

# need this code so if start, step, and end are all fixed point arguments we can take the maximum number
# of zeros from the arguments to use for the left of decimal. This will return the maximum number of places behind the left of decimal point
def getMaxFixedPointLeftOfDecimal(numberStrings):
    maxLOD = 0
    if(len(numberStrings) > 1):
        for floatString in numberStrings:
            decimalIndex = floatString.find(".")
            if(decimalIndex >= 0):
                maxLOD = max(maxLOD, decimalIndex)
            # If there is '.' then maxLOD is just the length of the string
            else:
                maxLOD = max(maxLOD, len(floatString))

    return maxLOD

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

# print help information
def printHelp():
    print SEQU_HELP
    exit(0)

def printVersion():
    print 'sequ (CS300 Term Project) ' + SEQU_VERSION + '\n' + SEQU_COPYRIGHT + '\n' + SEQU_LICENSE + '\n\n' + 'Written by Kyle Galbraith.'
    exit(0)

# Create a new sequ_obj which will have all of the defaults set for normal sequ operation.
initialObj = setup()
initialObj.outputQuick()





