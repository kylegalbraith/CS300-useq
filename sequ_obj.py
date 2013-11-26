#/usr/bin/env python
# Copyright (C) 2013 by Kyle Galbraith
import sys
class sequ_obj:
    """description of class"""
    # set a global constant for default value of format
    # Constructor for sequ_obj
    def __init__(self):
        self.startValue = 1
        self.endValue = 0
        self.separator = '\n'
        self.formatOption = "%g"
        self.equalWidth = False
        self.step = 1
        self.negativeStep = False
        self.padChar = "0"
        self.formatWord = "floating"
        self.leftDecimal = 0
        self.rightDecimal = 0

    def replaceZero(self, outputArray):
        formattedOutput = []
        for output in outputArray:
            # this is a good start but turns out bad results with -w -1.001 11
            count = 0
            dIndex = output.find('.')
            
            if(dIndex == -1):
                dIndex = len(output)
            dIndex = dIndex - 1
        
            for char in output:
                if(char == "0" and count < dIndex):
                    output = output.replace(char, self.padChar, 1)
                    count = count + 1
                    continue
                elif(char == "-"):
                    dIndex = dIndex - 1
                    continue
                else:
                    break

            formattedOutput.append(output)
                
        return formattedOutput
    
    def finalOutput(self, formattedOutput):
        loopCount = 0
        for output in formattedOutput:
            if(loopCount < len(formattedOutput) - 1):
                sys.stdout.write(output + self.separator)
                loopCount = loopCount + 1
            else:
                sys.stdout.write(output + '\n') 
          
    # Should factor outputSlow into this function so they are both in the same place
    def outputQuick(self):
        start = self.startValue
        end = self.endValue
        step = self.step
        negativeStep = self.negativeStep
        outputArray = []
        if(negativeStep):
            while start >= end:
                if(start != end):
                    outputArray.append(self.formatOption % + start)
                else:
                    outputArray.append(self.formatOption % + start)
                start += step
        else:
            while start <= end:
                if(start != end):
                    outputArray.append(self.formatOption % + start)
                else:
                    outputArray.append(self.formatOption % + start)
                start += step
             
        if(self.padChar != "0"):
            formattedOutput = self.replaceZero(outputArray)
            self.finalOutput(formattedOutput)
        else:
            self.finalOutput(outputArray)            
        
        # The program was successful
        exit(0)

