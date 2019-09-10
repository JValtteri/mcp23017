#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 10.09.2019
# GPIOmultiplexer

import MCP23017
from RPi import GPIO

'''
Intended to function as a wrapper for mcp23017 and RPi.GPIO 
so thay may be called as one.
That is, the program using both, may call all inputs on 
Raspberry Pi with a unified input pin address namespace. 

multiplexer automatically diverts the function call to the 
right module.
'''

def setmode(mode):
    GPIO.setmode(mode)
    
def setup(channel, mode, pull_up):
    if channel < 100:
        GPIO.setup(channel, mode, pull_up)
    else:
        pass    # TBD
    
def input(channel):
    if channel < 100:
        GPIO.input(channel)
    else:
        pass    # read channel
    
def cleanup():
    GPIO.cleanup()
    
    
