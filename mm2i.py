#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

# import modules
import sys, getopt

from math import floor

import pyperclip, subprocess

# import modules from file modules.py
from modules import onError, usage

from modules import factor, resolution

from modules import print_fraction

# handle options and arguments passed to script
try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 'i:r:vh',
                                 ['in=', 'resolution=', 'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))

# if no options passed, then exit
if len(sys.argv) == 1:  # no options passed
    onError(2, "No options given")
    
verbose = False
    
# interpret options and arguments
for option, argument in myopts:
    if option in ('-i', '--in'):
        mm = float(argument.replace(",", "."))
    elif option in ('-r', '--resolution'):
        resolution = int(argument)
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)

print ("\nConverting {} mm to inches, ".format(mm))
print ("with a max resolution of 1/{} inch ...".format(resolution))

decimal_inch = mm / factor

print ("\nDecimal: {}".format(decimal_inch))

inch_floor = floor(decimal_inch)
inch_remain =   decimal_inch - inch_floor              

no_of_fractions = floor(inch_remain / (1 / resolution))

if verbose:
    print ("\nFloor: {}".format(inch_floor))
    print ("Remain: {}".format(inch_remain))
    print ("No of 1/{} fractions: {}".format(resolution, no_of_fractions))
    
if verbose:
    print("\nCalculating deviation of input, {} mm, and {} {}/{}".format(mm, inch_floor, no_of_fractions, resolution))

low_value = (inch_floor + no_of_fractions/resolution) * factor

if verbose:
    print("Low value: {}".format(low_value))
    
low_deviation = mm - low_value

if verbose:
    print("Low deviation: {}".format(low_deviation))
    
########## Exact ##########
if low_deviation == 0:

    new_no_of_fractions, new_base = print_fraction(low_deviation, inch_floor, floor(no_of_fractions), verbose)

    if inch_floor == 0:
        print ("\nLow: {}/{}".format(new_no_of_fractions, new_base))
    else:
        if new_no_of_fractions == 0:
            print ("\nLow:   {}in".format(inch_floor))
        else:
            print ("\nLow:   {}in {}/{}".format(inch_floor, new_no_of_fractions, new_base))

    print ("Deviation: {} mm".format(low_deviation))

    if inch_floor == 0:
        print ("{}/{} = {} mm".format(new_no_of_fractions, new_base, (inch_floor + new_no_of_fractions / new_base) * factor))
    else:
        if new_no_of_fractions == 0:
            print ("{} = {} mm".format(inch_floor, (inch_floor + new_no_of_fractions / new_base) * factor))
        else:
            print ("{}+{}/{} = {} mm".format(inch_floor, new_no_of_fractions, new_base, (inch_floor + new_no_of_fractions / new_base) * factor))

    pyperclip.copy(low_value)
    print("---> Exact, and copied to your clipboard!\n")

    exit(0)
    
if verbose:
    print("\nCalculating deviation of input, {} mm, and {} {}/{}".format(mm, inch_floor, no_of_fractions + 1, resolution))
        
high_value = (inch_floor + (no_of_fractions + 1)/resolution) * factor

if verbose:
    print("High value: {}".format(high_value))

high_deviation = -(mm - high_value)

if verbose:
    print("High deviation: {}".format(high_deviation))

########## Low value ##########
new_no_of_fractions, new_base = print_fraction(low_deviation, inch_floor, floor(no_of_fractions), verbose)

if inch_floor == 0:
    print ("\nLow: {}/{}".format(new_no_of_fractions, new_base))
else:
    if new_no_of_fractions == 0:
        print ("\nLow:   {}in".format(inch_floor))
    else:
        print ("\nLow:   {}in {}/{}".format(inch_floor, new_no_of_fractions, new_base))

print ("Deviation: -{} mm".format(low_deviation))

if inch_floor == 0:
    print ("{}/{} = {} mm".format(new_no_of_fractions, new_base, (inch_floor + new_no_of_fractions / new_base) * factor))
else:
    if new_no_of_fractions == 0:
        print ("{} = {} mm".format(inch_floor, (inch_floor + new_no_of_fractions / new_base) * factor))
    else:
        print ("{}+{}/{} = {} mm".format(inch_floor, new_no_of_fractions, new_base, (inch_floor + new_no_of_fractions / new_base) * factor))

if low_deviation < high_deviation:
    pyperclip.copy(low_value)
    #subprocess.run("pbcopy", text=True, input=low_value)
    print("---> Closest, and copied to your clipboard!")

########## High value ##########
new_no_of_fractions, new_base = print_fraction(high_deviation, inch_floor, floor(no_of_fractions + 1), verbose)

if new_no_of_fractions / new_base == 1:
    inch_floor = inch_floor + 1
    new_no_of_fractions = 0
        
if inch_floor == 0:
    print ("\nHigh:  {}/{}".format(new_no_of_fractions, new_base))
else:
    if new_no_of_fractions == 0:
        print ("\nHigh:  {}in".format(inch_floor))
    else:
        print ("\nHigh:  {}in {}/{}".format(inch_floor, new_no_of_fractions, new_base))

print ("Deviation: +{} mm".format(high_deviation))

if inch_floor == 0:
    print ("{}/{} = {} mm".format(new_no_of_fractions, new_base, (inch_floor + new_no_of_fractions / new_base) * factor))
else:
    if new_no_of_fractions == 0:
        print ("{} = {} mm".format(inch_floor, (inch_floor + new_no_of_fractions / new_base) * factor))
    else:
        print ("{}+{}/{} = {} mm".format(inch_floor, new_no_of_fractions, new_base, (inch_floor + new_no_of_fractions / new_base) * factor))

if high_deviation < low_deviation:
    pyperclip.copy(high_value)
    #subprocess.run("pbcopy", text=True, input=high_value)
    print("---> Closest, and copied to your clipboard!")
    
print()
