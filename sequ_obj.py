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
        self.leftDecimal = 0
        self.rightDecimal = 0

    def outputQuick(self):
        start = self.startValue
        end = self.endValue
        step = self.step
        negativeStep = self.negativeStep
        sep = self.separator.decode("string_escape")
        if(negativeStep):
            while start >= end:
                if(start != end):
                    sys.stdout.write(self.formatOption % start + sep)
                else:
                    sys.stdout.write(self.formatOption % start)
                start += step
        else:
            while start <= end:
                if(start != end):
                    sys.stdout.write(self.formatOption % start + sep)
                else:
                    sys.stdout.write(self.formatOption % start + '\n')
                start += step    
        
        # The program was successful
        exit(0)

    def outputSlow(self):
        print 'something'





