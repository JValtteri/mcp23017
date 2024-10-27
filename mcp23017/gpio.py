#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 10.09.2019
# GPIO

from RPi import GPIO as RGPIO
import mcp23017

"""
#############################################
#                                           #
#  Wrapper class for RPi.GPIO and MCP23017  #
#                                           #
#############################################
"""


class GPIO():
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
    second expander is 2XX, etc.

    multiplexer automatically diverts the function call to the 
    right module.
    '''

    PUD_DOWN = 21
    PUD_UP = 22
    
    IN = 1
    OUT = 0

    HIGH = 1
    LOW = 0

    BCM = RGPIO.BCM

    @staticmethod
    def setmode(mode=BCM):

        found = None
        GPIO.expanders = []
        for i2c_addr in range(0x20, 0x28):
            try:
                expander = mcp23017.MCP23017(bus_addr=1, i2c_addr=i2c_addr)
                expander.read_byte(i2c_addr, 0x00)
                GPIO.expanders.append(expander)
                found = i2c_addr
            except OSError:
                pass
        if found:
            print("Found i2c address %s" % found )

        RGPIO.setmode(mode)

        for expander in GPIO.expanders:
            expander.setmode(mode)


    @staticmethod
    def setup(channel, mode, pull_up_down):

        try:
            # INTEGRATED GPIO
            if channel < 100:
                RGPIO.setup(channel, mode, pull_up_down=GPIO.PUD_UP)

            # EXPANDER 0
            elif channel < 200:
                GPIO.expanders[0].setup(channel-100, mode, pull_up_down)

            # EXPANDER 1
            elif channel < 300:
                GPIO.expanders[1].setup(channel-200, mode, pull_up_down)

            # EXPANDER 2
            elif channel < 400:
                GPIO.expanders[1].setup(channel-300, mode, pull_up_down)

        except IndexError:
            raise IndexError("GPIO index out of range")

        except AttributeError:
            raise AttributeError("No expanders set up. First set input mode: setmode()")


    @staticmethod
    def input(channel):

        try:
            if channel < 100:
                return RGPIO.input(channel)

            # EXPANDER 0
            elif channel < 200:
                return GPIO.expanders[0].input(channel-100)

            # EXPANDER 1
            elif channel < 300:
                return GPIO.expanders[1].input(channel-200)

            # EXPANDER 2
            elif channel < 400:
                return GPIO.expanders[2].input(channel-300)

        except IndexError:
                raise IndexError("GPIO index out of range")

    @staticmethod
    def cleanup():
        RGPIO.cleanup()
        for expander in GPIO.expanders:
            expander.cleanup()
