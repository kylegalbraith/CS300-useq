class sequ_obj(object):
    import sys
    """description of class"""
    startValue = 0
    endValue = 0

    def passedArgs(e, arguments):
        print 'In The sequObj'
        if isinstance(arguments[0], (int, long)) and isinstance(arguments[1], (int, long)):
            e.startValue = arguments[0]
            e.endValue = arguments[1]
            return true
        else:
            return false


