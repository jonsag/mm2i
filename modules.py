#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import configparser, os, sys

config = configparser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

# read variables from config file
factor = float(config.get('conversion', 'factor').strip())
resolution = int(config.get('conversion', 'resolution').strip())

# handle errors
def onError(errorCode, extra):
    print("\nError:")
    if errorCode in(1, 2): # print error information, print usage and exit
        print(extra)
        usage(errorCode)
    elif errorCode == 3: # print error information and exit
        print(extra)
        sys.exit(errorCode)
    elif errorCode == 4: # print error information and return running program
        print(extra)
        return
        
# print usage information        
def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    print("%s " % sys.argv[0])
    
    print("\n -v")
    print("    Verbose output")
    
    print("\n -h")
    print("    Show help")

    sys.exit(exitCode)

def print_fraction(deviation, inch_floor, no_of_fractions, resolution,verbose):
    if verbose:
        print("\n----------------------------")
        print("Whole part: {}".format(inch_floor))
        print("No of fractions: {}".format(no_of_fractions))
        print("Resolution: {}".format(resolution))
        
    if deviation == 0 and no_of_fractions == 0:
        return no_of_fractions, resolution
        
    if no_of_fractions == 0:
        return no_of_fractions, resolution
        
    new_no_of_fractions = no_of_fractions
    new_base = resolution
    
    while True:
        
        if (new_no_of_fractions % 2) == 0:
            if verbose:
                print("{0} is Even".format(new_no_of_fractions))
            new_no_of_fractions = int(new_no_of_fractions / 2)
            new_base = int(new_base /2)
            
            if verbose:
                print("{}/{} is the same as {}/{}".format(no_of_fractions, resolution, new_no_of_fractions, new_base))
        else:
            if verbose:
                print("{0} is Odd".format(new_no_of_fractions))
            break

    if verbose:
        print("----------------------------")
        
    return new_no_of_fractions, new_base