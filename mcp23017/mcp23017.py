#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 10.09.2019
# mcp23017

#   MCP23017 PINOUT
#
#  GPB0 - \_/ - GPA7
#  GPB1 -     - GPA6
#  GPB2 -     - GPA5
#  GPB3 -     - GPA4
#  GPB4 -     - GPA3
#  GPB5 -     - GPA2
#  GPB6 -     - GPA1
#  GPB7 -     - GPA0
# + VDD -     - INTA
# - VSS -     - INTB
#    NC -     - RESET
#   SCL -     - A2
#   SDA -     - A1
#    NC - ___ - A0


import smbus2
# from RPi import GPIO as RGPIO
# import ctypes

cdef class MCP23017():

    """
    Class for controlling any number of MCP23017 chips
    Works as an interface and an expansion to smbus2.
    Specifically brings support for interrupts
    """

    cdef int IODIRA = 0x00   # I/O mode (def 0xFF
    cdef int IODIRB = 0x01   # I/O mode (def 0xFF
    cdef int IPOLA = 0x02    # Input polarity
    cdef int IPOLB = 0x03
    cdef int GPINTENA = 0x04 # Interrupt on change
    cdef int GPINTENB = 0x05
    cdef int IOCON = 0x0A    # BANK SEQOP DISSW HEAN ODR INTPOL
    cdef int GPPU = 0x0C     # Pull-up mode
    cdef int INTFA = 0x0E    # Interrupt activated flag
    cdef int INTFB = 0x0F    # Interrupt activated flag
    cdef int INTCAPA = 0x10  # Interrupt capture register (resets when read)
    cdef int INTCAPB = 0x11  # Interrupt capture register (resets when read)

    cdef int GPIO_REG = 0x12 # Input status
    cdef int OLAT = 0x14 # output status

    cdef int PUD_DOWN = 21
    cdef int PUD_UP = 22

    cdef int IN = 1
    cdef int OUT = 0

    cdef object bus
    cdef int i2c_addr
    cdef object write_byte
    cdef object read_byte
    cdef object write_word
    cdef object read_word

    cdef __cinit__(self, int bus_addr=1, int i2c_addr = 0x20):        # Rev 1 Pi uses bus=0, Rev 2 Pi uses bus=1
                                                            # i2c_addr is set with pins A0-A2

        # Init comms
        self.bus = smbus2.SMBus(bus_addr)
        self.i2c_addr = i2c_addr
        self.write_byte = self.bus.write_byte_data  # Consider write block..!
        self.read_byte = self.bus.read_byte_data
        self.write_word = self.bus.write_word_data  # Consider write block..!
        self.read_word = self.bus.read_word_data

        # Input state memory
        # state is updated ....... sometimes
        # self.state_a = 0x00
        # self.state_b = 0x00

        #self.setmode()

    cdef setmode(self, char arg=' '):
        # Init chip for unified I/O
        # Warning!
        # The chip IOCON address schanges from 0x05 to 0x0A
        # when BANK is changed.
        #
        cdef int BANK   = 0 << 7 # seaquental adresses
        cdef int MIRROR = 1 << 6 # INT pins are internally connected
        cdef int SEQOP  = 0 << 5 # seaquental mode disabled
        cdef int DISSLW = 0 << 4 # slew rate controll
        cdef int HAEN   = 1 << 3 # hardware adress controll enable (A0-A2)
        cdef int ODR    = 0 << 2 # int pin is not open drain output
        cdef int INTPOL = 0 << 1 # active high
        #
        # Write the configuration
        cdef int setup = BANK + MIRROR + SEQOP + DISSLW + HAEN + ODR + INTPOL
        try:
            self.write_word(self.i2c_addr, 0x05, setup)
        except OSError:
            return False
        else:
            return True

    cdef setup(self, int pin_index, int mode=1, int pull_up=PUD_UP):
        # pin_index is the input pin (address)
        # mode is "in or out"
        # pull_up is internal pull_up resistor

        # SET MODE
        cdef int word = self.read_word(self.i2c_addr, MCP23017.IODIRA)
        # INPUT
        if mode ==  1:
            word = setBit(word, pin_index)

        # OUTPUT
        elif mode == 0:
            word = clearBit(word, pin_index)

        if mode in [1, 0]:
            self.write_word(self.i2c_addr, MCP23017.IODIRA, word)
        else:
            raise ValueError("invalid mode")

        # SET PULL-UP MODE
        word = self.read_word(self.i2c_addr, MCP23017.GPPU)
        # PULL-UP
        if pull_up == 22:
            word = setBit(word, pin_index)

        # PULL-DOWN
        elif pull_up == 21:
            word = clearBit(word, pin_index)

        if pull_up in [22, 21]:
            self.write_word(self.i2c_addr, MCP23017.GPPU, word)
        else:
            raise ValueError("invalid pull-up mode")

    cdef input(self, int pin_index):
        cdef int word = self.read_word(self.i2c_addr, MCP23017.GPIO_REG)
        cdef int state = testBit(word, pin_index)
        return state

    cdef readBit(self, int index, int address = GPIO_REG):
        cdef int word = self.read_word(self.i2c_addr, address)
        return testBit(word, index)

    def cleanup(self):
        for pin_index in range(16):
            self.setup(pin_index, MCP23017.IN, MCP23017.PUD_UP)

    def writeBit(self, bit, index, address = OLAT):
        word = self.read_word(self.i2c_addr, address)
        pass

    def readAll(self):
        for byte_addr in range(0x00, 0x1B):
            word = self.read_word(self.i2c_addr, byte_addr)
            # print(hex(byte_addr), bin(word))        #debug

    # def interrupt(self, queue):
    #     # blocks = Blocs()                              #
    #     word = self.read(self.i2c_addr, self.INTFA)     # Reads the Interrup register: two bytes of data

    #     for bank in [0,1]:                              # Iterate the two banks of bytes
    #         blocks.asByte = word[bank]
    #         for bit in range(7):                        # length of block is two bytes, a word
    #             if block[bit] == 1:                     # when the bit is found
    #                 index = (bank, bit)                 # its location is stored as index    # is this necessary?
    #                 break                               # and the search stops.
    #     word = self.read(self.i2c_addr, self.OLAT)      # Reads the Input Register: two bytes of data

    #     blocks.asByte = word[index[0]]
    #     queue.put(block.index[1])                       # the index of the 1-bit


# from code example from https://wiki.python.org/moin/BitManipulation
# "Single bits"

# testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.

def testBit(int_type, offset):
    mask = 1 << offset
    if (int_type & mask) != 0:
        return 1
    else:
        return 0

# setBit() returns an integer with the bit at 'offset' set to 1.

def setBit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)

# clearBit() returns an integer with the bit at 'offset' cleared.

def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return(int_type & mask)

# toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.

def toggleBit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)

