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
import re

# These are constants used throughout the program
SEQU_VERSION = "4.0"
SEQU_COPYRIGHT = "Copyright (C) 2013 Free Software Foundation, Inc."
SEQU_LICENSE = "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>. \nThis is free software: you are free to change and redistribute it. \nThere is NO WARRANTY, to the extent permitted by law."
SEQU_HELP = "Usage: \n\tsequ [OPTION]... LAST\n\tsequ [OPTION]... FIRST LAST\n\tsequ [OPTION]... FIRST INCREMENT LAST\nPrint numbers from FIRST to LAST, in steps of INCREMENT.\n\n\t-f, --format=FORMAT\tuse printf style floating-point FORMAT (%a is not supported)\n\t-s, --separator=STRING\tuse STRING to separate numbers (default: \\n)\n\t-w, --equal-width\tequalize width by padding with leading zeroes\n\t-p, --pad\t\toutput the sequence with elements padded on the left to be all of equal width: the pad character is given by the single-char pad string\n\t-W, --words\t\toutput the sequence as a single space-separated line\n\t-P, --pad-spaces\toutput the sequence with elements padded with spaces on the left to be all of equal width\n\t--help\t\t\tdisplay this help and exit\n\t--version\t\tdisplay version info and exit\n\nIf FIRST or INCREMENT is omitted, it defaults to 1. That is,\nan omitted INCREMENT defaults to 1 even when LAST is smaller than FIRST.\nFIRST, INCREMENT, and LAST are interpreted as floating point values.\nINCREMENT is usually positive if FIRST is smaller than LAST, and\nINCEREMENT is usually negative if FIRST is greater than LAST.\nFORMAT must be suitable for printing one argument of type 'float';\nit defaults to %.precf if FIRST, INCREMENT, and LAST are all fixed point\ndecimal numbers with maximum precision prec, and %g otherwise."

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
    elif(errorCode == 10):
        print 'sequ: one or more operands do not match the \'--format-word\' specified: ' + error + helpString
        exit(1)
    elif(errorCode == 11):
        print 'sequ: increment option must be arabic when using alpha in \'--format-word\'' + helpString
        exit(1)
    elif(errorCode == 12):
        print 'sequ: invalid format for \'--format-word\' ' + error + helpString
        exit(1)
    elif(errorCode == 13):
        print 'sequ: ' + "'" + error + "'" + ' is not a valid representation of a number'
        exit(1)
    else:
        print 'ERROR - An unexpected error has ocurred'
        exit(1)

def setup():
    # Create a new sequ_obj which will have all of the defaults set for normal
    # sequ operation.
    initialObj = sequ_obj()

    assert initialObj.startValue == 1, "Start value was not initialized correctly"
    assert initialObj.step == 1, "Step value was not initialized correctly" 
    assert initialObj.endValue == 0, "End value was not initialized correctly"
    assert initialObj.equalWidth == False, "Equal width boolean was not initialized correctly"
    assert initialObj.negativeStep == False, "Negative step was not initialized correctly"
    assert initialObj.separator == '\n', "Default separator not set correctly"

    # Get the arguments that have been passed in, and ignore the first one
    # since it is the invocation of the script
    arguments = sys.argv[1:len(sys.argv)]

    # Get the total args passed in as exactly 2 are required
    totalArgs = len(arguments)
    # loop variables.
    # seenFormat = flag for we have seen the format flag
    # seenEw = flag for we have seen the equal-width
    stringParse = 0
    seenFormat = False
    seenEw = False
    seenFormatWord = False

    while checkArgumentFormat(arguments[stringParse]) == "cl_argument":
        #parse '-' flags to assign them to the sequ object
        formatVerboseSub = "--format" in arguments[stringParse] and "-word" not in arguments[stringParse]
        formatSub = "-f" in arguments[stringParse] and "--f" not in arguments[stringParse]
        format = formatVerboseSub or formatSub

        separatorVerboseSub = "--separator" in arguments[stringParse]
        separatorSub = "-s" in arguments[stringParse]
        separator = separatorVerboseSub or separatorSub

        padVerboseSub = "--pad" in arguments[stringParse]
        padSub = "-p" in arguments[stringParse]
        pad = padVerboseSub or padSub

        formatWordVerboseSub = "--format-word" in arguments[stringParse] and "-word" in arguments[stringParse]
        formatWordSub = "-F" in arguments[stringParse]
        formatWord = formatWordVerboseSub or formatWordSub

        if arguments[stringParse] == "--help":
            printHelp()
        elif arguments[stringParse] == "--version":
            printVersion()

        elif arguments[stringParse] == "--pad-spaces" or arguments[stringParse] == "-P":
            if(seenFormat == False and seenEw == False and seenFormatWord == False):
                initialObj.equalWidth = True
                initialObj.padChar = ' '
                seenEw = True
            else:
                usage(6)

        elif arguments[stringParse] == "--equal-width" or arguments[stringParse] == "-w":
            if(seenFormat == False and seenEw == False and seenFormatWord == False):
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
                if(seenEw == False and seenFormatWord == False):                       
                    verboseFormatLength = len("--format")
                    formatFlagLength = len("-f")
                    argumentLength = len(arguments[stringParse])            
                        
                    # There is no = behind the flag so we can assume that
                    # the format is the next place on the command line
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
            # Check the length of the single character passed in to make
            # sure that
            # it is a single character.  Then Run equal-width check and
            # then replace
            # the 0s with the single character passed in.
            if(seenEw == False and seenFormat == False and seenFormatWord == False):
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
                        # Check the pad character to escape / and to make
                        # sure its length == 1
                        # If that checks out then put the character on the
                        # sequ object and set seenEw to true
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
            
        elif formatWord:
            if(seenEw == False and seenFormat == False):
                try:    
                    formatWordVerboseLength = len("--format-word")
                    formatWordFlagLength = len("-F")
                    argumentLength = len(arguments[stringParse])

                    if(argumentLength == formatWordVerboseLength or argumentLength == formatWordFlagLength):
                        stringParse += 1
                        if(checkArgumentFormat(arguments[stringParse]) == "alpha"):
                            validWordFormat = checkWordFormat(arguments[stringParse])
                            initialObj.formatWord = validWordFormat
                        else: 
                            initialObj.formatWord = ""
                            stringParse -= 1
                        
                        initialObj.formatWordBool = True
                    else:
                        parsedFormatWord = parseFlagWithEquals(arguments[stringParse], formatWordVerboseLength, formatWordFlagLength)
                        if(checkArgumentFormat(parsedFormatWord) == "alpha"):
                            validWordFormat = checkWordFormat(parsedFormatWord)
                            initialObj.formatWord = validWordFormat
                        else:
                            initialObj.formatWord = ""

                        initialObj.formatWordBool = True
                except IndexError:
                    usage(4, "--format-word") 
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
    
    if(initialObj.formatWord == "" and not initialObj.formatWordBool):
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
    
        if(lengthOfNumbers == 2):
            initialObj.startValue = numbers[0]
            initialObj.endValue = numbers[1]
            startValueString = numberStrings[0]
            endValueString = numberStrings[1]
                
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
    # TODO: Refactor this out into its own function(s) somehow because it is going to get ugly
    else:
        for x in range(stringParse, totalArgs):
            try:
                numbers.append(arguments[x])
            except ValueError:
                usage(3)
        
        lengthOfCl = len(numbers)

        # TODO: Refactor the code below this into setupFormatWordOutput function, it will return an array object that we will then check
        #limitArguments = setupFormatWordOutput(numbers, lengthOfCl, initialObj.formatWord)
       
        #start, step, end
        if(lengthOfCl == 3):
            print '3 args to parse'
            startFormat = checkArgumentFormat(numbers[0])
            stepFormat = checkArgumentFormat(numbers[1])
            endFormat = checkArgumentFormat(numbers[2])

            if(initialObj.formatWord == ""):
                initialObj.formatWord = endFormat

            # If the format is alpha, then the step format must be arabic
            if(initialObj.formatWord == "alpha" or initialObj.formatWord == "ALPHA"):
                if(stepFormat == "arabic"):
                    if(startFormat == initialObj.formatWord.lower() and endFormat == initialObj.formatWord.lower()):
                        initialObj.startValue = wordToInt(numbers[0])
                        initialObj.step = int(numbers[1])
                        initialObj.endValue = wordToInt(numbers[2])
                    else:
                        usage(10, initialObj.formatWord)
                else:
                    usage(11)
            
            elif(initialObj.formatWord == "roman" or initialObj.formatWord == "ROMAN"):
                # Boolean test, if start/step/end == roman we are good to go, however, if one or more of them == arabic we are still good to go because we
                # can promote arabic to roman if roman output is requested.
                formatEqualsRoman = (startFormat == initialObj.formatWord.lower() or startFormat == "arabic") and (stepFormat == initialObj.formatWord.lower() or stepFormat == "arabic") and (endFormat == initialObj.formatWord.lower() or endFormat == "arabic")
                if(formatEqualsRoman):
                    if(startFormat == "arabic"):
                        initialObj.startValue = int(numbers[0])
                    else:
                        initialObj.startValue = romanToNumber(numbers[0])
                    if(stepFormat == "arabic"):
                        initialObj.step = int(numbers[1])
                    else:
                        initialObj.step = romanToNumber(numbers[1])
                    if(endFormat == "arabic"):
                        initialObj.endValue = int(numbers[2])
                    else:
                        initialObj.endValue = romanToNumber(numbers[2])
                else:
                    usage(10, initialObj.formatWord)

            elif(initialObj.formatWord == "arabic"):
                print 'arabic format'
                if(startFormat == initialObj.formatWord and stepFormat == initialObj.formatWord and endFormat == initialObj.formatWord):
                    initialObj.startValue = int(numbers[0])
                    initialObj.step = int(numbers[1])
                    initialObj.endValue = int(numbers[2])
                else:
                    usage(10, initialObj.formatWord)

            elif(initialObj.formatWord == "floating"):
                print 'floating format'
                if(startFormat == initialObj.formatWord and stepFormat == initialObj.formatWord and endFormat == initialObj.formatWord):
                    initialObj.startValue = float(numbers[0])
                    initialObj.step = float(numbers[1])
                    initialObj.endValue = float(numbers[2])
                else:
                    usage(10, initialObj.formatWord)
          
        #start, end
        if(lengthOfCl == 2):
            print '2 args to parse'
            startFormat = checkArgumentFormat(numbers[0])
            endFormat = checkArgumentFormat(numbers[1])

            if(initialObj.formatWord == ""):
                initialObj.formatWord = endFormat

            if(initialObj.formatWord == "alpha" or initialObj.formatWord == "ALPHA"):
                if(startFormat == initialObj.formatWord.lower() and endFormat == initialObj.formatWord.lower()):
                    initialObj.startValue = wordToInt(numbers[0])
                    initialObj.endValue = wordToInt(numbers[1])
                else:
                    usage(10, initialObj.formatWord)

            elif(initialObj.formatWord == "roman" or initialObj.formatWord == "ROMAN"):
                formatEqualsRoman = (startFormat == initialObj.formatWord.lower() or startFormat == "arabic") and (endFormat == initialObj.formatWord.lower() or endFormat == "arabic")
                if(formatEqualsRoman):
                    if(startFormat == "arabic"):
                        initialObj.startValue = int(numbers[0])
                    else:
                        initialObj.startValue = romanToNumber(numbers[0])
                    if(endFormat == "arabic"):
                        initialObj.endValue = int(numbers[1])
                    else:
                        initialObj.endValue = romanToNumber(numbers[1])
                else:
                    usage(10, initialObj.formatWord)

            elif(initialObj.formatWord == "arabic"):
                if(startFormat == initialObj.formatWord and endFormat == initialObj.formatWord):
                    initialObj.startValue = int(numbers[0])
                    initialObj.endValue = int(numbers[1])
                else:
                    usage(10, initialObj.formatWord)

            elif(initialObj.formatWord == "floating"):
                if(startFormat == initialObj.formatWord and endFormat == initialObj.formatWord):
                    initialObj.startValue = float(numbers[0])
                    initialObj.endValue = float(numbers[1])
                else:
                    usage(10, initialObj.formatWord)

        #end
        if(lengthOfCl == 1):
            print '1 arg to parse'
            endFormat = checkArgumentFormat(numbers[0])

            if(initialObj.formatWord == ""):
                initialObj.formatWord = endFormat

            if(initialObj.formatWord == "alpha" or initialObj.formatWord == "ALPHA"):
                if(endFormat == initialObj.formatWord.lower()):
                    initialObj.endValue = wordToInt(numbers[0])
                else:
                    usage(10, initialObj.formatWord)

            elif(initialObj.formatWord == "roman" or initialObj.formatWord == "ROMAN"):
                formatEqualsRoman = (endFormat == initialObj.formatWord.lower() or endFormat == "arabic")
                if(formatEqualsRoman):
                    if(endFormat == "arabic"):
                        initialObj.endValue = int(numbers[0])
                    else:
                        initialObj.endValue = romanToNumber(numbers[0])
                else:
                    usage(10, initialObj.formatWord)

            elif(initialObj.formatWord == "arabic"):
                if(endFormat == initialObj.formatWord):
                    initialObj.endValue = int(numbers[0])
                else:
                    usage(10, initialObj.formatWord)

            elif(initialObj.formatWord == "floating"):
                if(endFormat == initialObj.formatWord):
                    initialObj.endValue = float(numbers[0])
                else:
                    usage(10, initialObj.formatWord)

    if(initialObj.step < 0):
        if(checkNegStepEnd(initialObj.startValue, initialObj.endValue)):
            initialObj.negativeStep = True
        else:
            checkStartEnd(initialObj.startValue, initialObj.endValue)
    else:
        checkStartEnd(initialObj.startValue, initialObj.endValue)

    return initialObj

# Roman numeral to integer
def romanToNumber(string):
    returnNumber = 0
    table = [
        ['M',1000],['CM',900],['D',500],['CD',400],['C',100],['XC',90],['L',50],['XL',40],['X',10],['IX',9],['V',5],['IV',4],['I',1],
        ['m',1000],['cm',900],['d',500],['cd',400],['c',100],['xc',90],['l',50],['xl',40],['x',10],['ix',9],['v',5],['iv',4],['i',1]  
    ] 

    for pair in table:
        keepGoing = True
        while keepGoing:
            if len(string) >= len(pair[0]):
                if string[0:len(pair[0])] == pair[0]:
                    returnNumber += pair[1]
                    string = string[len(pair[0]):]
                else:
                    keepGoing = False
            else:
                keepGoing = False

    return returnNumber

# I found this implementation on stackoverflow: http://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers-python
# My thinking is that you want to convert the alpha representation to a number and then convert it back
# when you actually output.
def wordToInt(textNumber, numWordsDict={}):
    if not numWordsDict:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]
        numWordsDict["and"] = (1, 0)
        for idx, word in enumerate(units):
            numWordsDict[word] = (1, idx)
        for idx, word in enumerate(tens):
            numWordsDict[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numWordsDict[word] = (10 ** (idx * 3 or 2), 0)

    current = 0
    result = 0
    for word in textNumber.split():
        if word not in numWordsDict:
            usage(13, word)

        scale, increment = numWordsDict[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

def checkArgumentFormat(clArg):
    flagRegex = '^-+[a-zA-Z]'
    isArgFlag = re.compile(flagRegex)

    arabicRegex = '^-?\d+$'
    isArgArabic = re.compile(arabicRegex)

    floatRegex = '^[-+]?[0-9]*\.[0-9]+$'
    isArgFloat = re.compile(floatRegex)

    alphaRegex = '^[a-zA-Z\s+]+$'
    isArgAlpha = re.compile(alphaRegex)

    romanRegex = '^(M{0,4}|m{0,4})((CM|CD|D?C{0,3})|(cm|cd|d?c{0,3}))((XC|XL|L?X{0,3})|(xc|xl|l?x{0,3}))((IX|IV|V?I{0,3})(ix|iv|v?i{0,3}))$'
    isArgRoman = re.compile(romanRegex)

    if(isArgFlag.match(clArg)):
        return "cl_argument"
    elif(isArgArabic.match(clArg)):
        return "arabic"
    elif(isArgFloat.match(clArg)):
        return "floating"
    elif(isArgRoman.match(clArg)):
        return "roman"
    elif(isArgAlpha.match(clArg)):
        return "alpha"

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
    
    return leftOfDecimal

def checkWordFormat(wordFormat):
    if(wordFormat == "arabic" or wordFormat == "floating" or wordFormat == "alpha" or wordFormat == "ALPHA" or wordFormat == "roman" or wordFormat == "ROMAN"):
        return wordFormat
    else:
        usage(12, wordFormat)

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
if(initialObj.formatWordBool):
    if(initialObj.formatWord == "alpha" or initialObj.formatWord == "ALPHA"):
        initialObj.outputAlpha()
    elif(initialObj.formatWord == "roman" or initialObj.formatWord == "ROMAN"):
        initialObj.outputRoman()
    elif(initialObj.formatWord == "arabic"  or initialObj.formatWord == "floating"):
        initialObj.outputQuick()
else:
    initialObj.outputQuick()





