#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 10.09.2019
# GPIOmultiplexer

import MCP23017
from RPi import GPIO

'''
Intended to function as a wrapper for mcp23017 and RPi.GPIO, 
so thay may be called as one.
That is, all inputs, GPIO and MCP expander, may be call on 
Raspberry Pi with a unified input pin address space and
functions. 

Intended to work as drop-in replacement for GPIO-only.

Use:
From MCP23017 import GPIO

no other code changes required.
Normal RPi GPIO is pins are XX, 
first expander is 1XX, and
second expander is 2XX

multiplexer automatically diverts the function call to the 
right module.
'''

from RPi import GPIO as RGPIO
from mcp23017 import MCP23017

class GPIO():

    def __init__(self):
        self.PUD_DOWN = 0
        self.PUD_UP = 1
        
        self.IN = 0
        self.OUT = 1
    
    def setmode(self, mode):
        RGPIO.setmode(mode)
        MCP23017.setmode(mode)
    
    def setup(self, channel, mode, pull_up):
        if channel < 100:
            if pull_up == self.PUD_DOWN:
                pull_up = RGPIO.PUD_DOWN
            elif pull_up == self.PUD_UP:
                pull_up = RGPUO.PUD_UP
            
            if mode == self.IN:
                mode = RGPIO.IN
            elif mode == self.OUT:
                mode = RGPIO.OUT
                
            RGPIO.setup(channel, mode, pull_up_down=pull_up)
            
        else # elif channel >= 100:
            MCP23017.setup(channel, mode, pull_up)
            
    def input(self, channel):
        if channel < 100:
            return RGPIO.input(channel)
        else:
            return MCP23017.input(channel)    # read channel

    def cleanup():
        GPIO.cleanup()
        MCP23017.cleanup()
