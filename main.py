#! /usr/bin/env python
# -*- coding: utf-8  -*-
import sys
import os
import platform
from scripts import utilities
from scripts.replacement import *

ALGORITHM_CODES = ['fifo', 'second', 'lru']
CLASS_CODES = ['FIFO', 'Second_Chance', 'LRU']

def detect_system():
    if platform.system() == 'Windows':
        print "WARNING: ANSI color may not work on Windows Command Prompt.\n\
You may see meta-escaping characters instead of color output."

def get_arguments():
    """Get command-line arguments"""
    usage = "python main.py <algorithm_code> <memory_size> <access_file>"
    algorithm_code = 0
    memory_size = 1
    if len(sys.argv) < 4:
        utilities.output.error("Insufficient arguments or wrong usage.")
        print usage
        sys.exit(1)

    if sys.argv[1] not in ['0', '1', '2']:
        utilities.output.error("Invalid algorithm code \"%s\". Please use 0, 1, or 2." 
                               % sys.argv[1] )
        sys.exit(1)

    algorithm_code = int(sys.argv[1])

    try:
        memory_size = int(sys.argv[2])
        if memory_size <= 0:
            raise
    except:
        utilities.output.error("Invalid memory size \"%s\". Please use a positive integer."
                               % sys.argv[2])
        sys.exit(1)

    input_file = sys.argv[3]
    return algorithm_code, memory_size, input_file

def check_path(input_file):
    """Check validity of path of the input file"""
    abs_path = os.path.abspath(input_file)  # absolute path of input file

    if os.path.isfile(abs_path):
        pass
    else:
        if os.path.exists(abs_path):
            if os.path.isdir:
                utilities.output.error("Input file \"%s\" is a directory, not a file." 
                                       % abs_path)
                sys.exit(1)
        else:
            utilities.output.error("Input file \"%s\" does not exist." % abs_path)
            sys.exit(1)
            
    dir_name = os.path.dirname(abs_path)
    base_name = os.path.basename(abs_path)
    return dir_name, base_name

def read_input(input_file):
    f = None
    text = ""
    try:
        f = open(input_file, "r")
        text = f.read()
        f.close()
    except:
        utilities.output.error("Cannot open the file \"%s\"" % input_file)
        sys.exit(1)
    finally:
        f.close()
    return text

def split_input(text):
    s = text.split()
    return s

def write_output(output_file, output):
    f = None
    try:
        f = open(output_file, "w")
        f.write(output)
        f.close()
    except:
        utilities.output.error("Cannot write output to file \"%s\"." %output_file)
        sys.exit(1) 

def start(algorithm_code, memory_size, input_file, output_file):
    text = read_input(input_file)
    s = split_input(text)
    if len(s) == 0:
        utilities.output.error("The input file is empty.")
        sys.exit(1)
    access = []
    try:
        access = map(int, s)
    except:
        utilities.output.error("There appears to be syntax errors in the input file.")
        utilities.output.error("Make sure each element is an integer.")
        sys.exit(1)
    expression = "%s(%d, access)" % (CLASS_CODES[algorithm_code], memory_size)
    obj = eval(expression)
    obj.start()
    output = obj.get_output()
    print output
    write_output(output_file, output)

def main():
    detect_system()
    algorithm_code, memory_size, input_file = get_arguments()
    dir_name, base_name = check_path(input_file)
    file_name, ext_name = os.path.splitext(base_name)
    output_file = dir_name + '/' + file_name + '.' \
                + ALGORITHM_CODES[algorithm_code] + ext_name
    #print output_file
    start(algorithm_code, memory_size, input_file, output_file)

if __name__ == "__main__":
    main()