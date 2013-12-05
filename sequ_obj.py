#/usr/bin/env python
# Copyright (C) 2013 by Kyle Galbraith
import sys
# num2word is a python module that converts numbers to actual strings, it can be found here: https://pypi.python.org/pypi/num2words
sys.path.append('python_num_to_word/')
import num2word

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
        self.formatWord = ""
        self.formatWordBool = False
        self.numberLines = False
        self.numberLinesFile = []
        self.leftDecimal = 0
        self.rightDecimal = 0

    def replaceZero(self, outputArray):
        formattedOutput = []
        for output in outputArray:
            zeroReplaced = self.replaceZeroSingleLine(output)
            formattedOutput.append(zeroReplaced)
                
        return formattedOutput

    def replaceZeroSingleLine(self, string):
        count = 0
        returnString = ""
        dIndex = string.find('.')
        if(dIndex == -1):
            dIndex = len(string)
        dIndex = dIndex - 1

        for char in string:
            if(char == "0" and count < dIndex):
                string = string.replace(char, self.padChar, 1)
                count = count + 1
                continue
            elif(char == "-"):
                dIndex = dIndex - 1
                continue
            else:
                break
        returnString = string
        return returnString

    def finalOutput(self, formattedOutput):
        loopCount = 0
        for output in formattedOutput:
            if(loopCount < len(formattedOutput) - 1):
                sys.stdout.write(output + self.separator)
                loopCount = loopCount + 1
            else:
                sys.stdout.write(output + '\n')
        #program was successful        
        exit(0) 
 
    # readFile() is used when --number-lines/-n is used where we read in a file from stdin and then output each line preceeded with a line number
    # that we create using sequ.    
    def readFile(self):
        start = self.startValue
        step = self.step
        fileArray = self.numberLinesFile

        if(not self.formatWordBool):
            for line in fileArray:
                lineNumber = self.formatOption % + start
                if(self.padChar != "0"):
                    paddedNonZeroLineNumber = self.replaceZeroSingleLine(lineNumber)
                    sys.stdout.write(str(paddedNonZeroLineNumber) + self.separator + line)
                else:
                    sys.stdout.write(str(lineNumber) + self.separator + line)
                start += step
        else:
            lineNumber = ""
            isAlpha = (self.formatWord.lower() == "alpha")
            isRoman = (self.formatWord.lower() == "roman")
            isArabic = (self.formatWord == "arabic")
            isFloat = (self.formatWord == "floating")

            if(isAlpha):
                for line in sys.stdin:
                    lineNumber = self.numberToWord(start)
                    sys.stdout.write(lineNumber + self.separator + line)
                    start += step
            elif(isRoman):
                for line in sys.stdin:
                    lineNumber = self.numberToRoman(start)
                    sys.stdout.write(lineNumber + self.separator + line)
                    start += step
            elif(isArabic or isFloat):
                for line in sys.stdin:
                    sys.stdout.write(str(start) + self.separator + line)
                    start += step
                
        #program was successful
        exit(0)
              
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
            if(not self.numberLines):
                while start <= end:
                    if(start != end):
                        outputArray.append(self.formatOption % + start)
                    else:
                        outputArray.append(self.formatOption % + start)
                    start += step
            else:
                self.readFile()
             
        if(self.padChar != "0"):
            formattedOutput = self.replaceZero(outputArray)
            self.finalOutput(formattedOutput)
        else:
            self.finalOutput(outputArray)            
        
    def outputAlpha(self):
        start = self.startValue
        step = self.step
        end = self.endValue
        negativeStep = self.negativeStep
        outputArray = []

        if(not self.numberLines):
            while start <= end:
                convert = self.numberToWord(start)
                if(start != end):
                    outputArray.append(convert)
                else:
                    outputArray.append(convert)
                start += step      
            self.finalOutput(outputArray)
        else:
                self.readFile()


    def outputRoman(self):
        start = self.startValue
        step = self.step
        end = self.endValue
        negativeStep = self.negativeStep
        outputArray = []

        if(negativeStep):
            while start >= end:
                convert = self.numberToRoman(start)
                if(start != end):
                    outputArray.append(convert)
                else:
                    outputArray.append(convert)
                start += step
            self.finalOutput(outputArray)
        else:
            if(not self.numberLines):
                while start <= end:
                    convert = self.numberToRoman(start)
                    if(start != end):
                        outputArray.append(convert)
                    else:
                        outputArray.append(convert)
                    start += step
                self.finalOutput(outputArray)
            else:
                self.readFile()
    
    # Use num2word to convert a number to a word representation.
    def numberToWord(self, number):
        convertedWord = num2word.to_card(number)
        if(self.formatWord == "ALPHA"):
            return convertedWord.upper()
        else:
            return convertedWord

    # Integer to roman numeral conversion. 
    def numberToRoman(self, number):
        integer = number
        returnString = ''
        table = [
            ['M',1000],['CM',900],['D',500],['CD',400],['C',100],['XC',90],['L',50],['XL',40],['X',10],['IX',9],['V',5],['IV',4],['I',1],
            ['m',1000],['cm',900],['d',500],['cd',400],['c',100],['xc',90],['l',50],['xl',40],['x',10],['ix',9],['v',5],['iv',4],['i',1]  
        ]    
    
        for pair in table:
            if pair not in table:
                print 'not a valid roman numeral'
            while integer - pair[1] >= 0:
                integer -= pair[1]
                returnString += pair[0]

        if(self.formatWord == "ROMAN"):
            return returnString.upper()
        else:
            return returnString.lower()

