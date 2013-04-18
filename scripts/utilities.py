# -*- coding: utf-8  -*-
import sys
import decimal

class output(object):
    """
    ANSI console colored output:
        * error (red)
        * warning (yellow)
        * debug (green)
    """
    
    RED     = 1
    GREEN   = 2
    YELLOW  = 3
    ERROR   = 4
    DEBUG   = 5
    WARNING = 6
    @staticmethod
    def __out(type, msg):
        if type == output.ERROR:
            sys.stderr.write("\033[%dm [%s] %s\033[m\n" % (30 + output.RED, "Error", msg))
        if type == output.DEBUG:
            sys.stdout.write("\033[%dm [%s] %s\033[m\n" % (30 + output.GREEN, "Debug", msg))
        if type == output.WARNING:
            sys.stdout.write("\033[%dm [%s] %s\033[m\n" % (30 + output.YELLOW, "Warning", msg))
    @staticmethod
    def error(msg):
        output.__out(output.ERROR, msg)
    @staticmethod    
    def debug(msg):
        output.__out(output.DEBUG, msg)
    @staticmethod   
    def warning(msg):
        output.__out(output.WARNING, msg)

def check_version(): 
    version = sys.version_info
    if version[0] == 2:
        if version[1] < 7:
            output.error("Python 2.%d detected. This program requires Python 2.7."%(version[1]))
            output.warning("Please try using 'python2.7' command if your system has Python 2.7 installed.")
            sys.exit(1)
    if version[0] == 3:
            output.error("Python 3.%d detected. This program requires Python 2.7. Please try using 'python2.7' command. "%(version[1]))
            output.warning("Please try using 'python2.7' command if your system has Python 2.7 installed.")
            sys.exit(1)

def roundup_2(number):
    """
    Round up a floating number
    """
    return decimal.Decimal(str(number)).quantize(decimal.Decimal('.01'), 
                                            rounding=decimal.ROUND_HALF_UP)
            
if __name__ == '__main__':
    utilities.output.warning("Please run main.py script from project's directory.")  