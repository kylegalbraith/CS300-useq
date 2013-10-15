# Kyle Galbraith - CS300 - useq compliance level 0

# Need sys to pass arguments in
import sys
from sequ_obj import *

# usage will be the initial error handling function so if the initial requirements are not met, print out the correct thing to do.
def usage(errorCode):
    if(errorCode == 1):
        print 'ERROR - sequ requires exactly two integers'
        exit(1)
    elif(errorCode == 2):
        print 'ERROR - sequ CLO only accepts integer types'
        exit(1)

# outputSeq will output the sequence between the integers passed in
def outputSeq(sequObj):
    start = arguments[0]
    end = arguments[1]
    
    # If the start is greater than the end then we just exit
    if start > end:
        exit(1)
    for x in range(start, end + 1):
        print x
    # The program was successful
    exit(0)

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
        arguments[x] = int(arguments[x])
    except ValueError:
        usage(2)

if isinstance(arguments[0], (int, long)) and isinstance(arguments[1], (int, long)):
    outputSeq(arguments)

if(initialObj.passedArgs(arguments) == true):
    outputSeq(initialObj)




