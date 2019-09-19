#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 10.09.2019
# mcp23017

import smbus2
import ctypes

class MCP23017():

    def __init__(self, bus=1, i2c_addr = 0x20, ):           # Rev 1 Pi uses bus=0, Rev 2 Pi uses bus=1
                                                            # i2c_addr is set with pins A0-A2
        """                                                 
        Class for controlling any number of MCP23017 chips
        Works as an interface and an expansion to smbus2.
        Specifically brings support for interrupts
        """
        
        # Init comms
        self.bus = smbus2.SMBus(bus)
        self.i2c_addr = i2c_addr
        self.write_byte = bus.write_byte_data  # Consider write block..!
        self.read_byte = bus.read_byte_data
        self.write_word = bus.write_word_data  # Consider write block..!
        self.read_word = bus.read_word_data
        

        self.IODIRA = 0x00 # I/O mode (def 0xFF
        self.IODIRB = 0x01 # I/O mode (def 0xFF
        self.IPOLA = 0x02 # Input polarity
        self.IPOLB = 0x03
        self.GPINTENA = 0x04 # Interrupt on change
        self.GPINTENB = 0x05
        self.IOCON = 0x0A  # BANK SEQOP DISSW HEAN ODR INTPOL
        
        self.INTFA = 0x0E # Interrupt activated flag
        self.INTFB = 0x0F # Interrupt activated flag
        self.INTCAPA = 0x10 #Interrupt capture register (resets when read)
        self.INTCAPB = 0x11 #Interrupt capture register (resets when read)
        
        self.GPIO = 0x12 # Input status
        self.OLAT = 0x14 # output status
        
        # Input state memory
        # state is updated ....... sometimes
        self.state_a = 0x00
        self.state_b = 0x00

    def setmode(arg=''):
        # Init chip for unified I/O
        # Warning!
        # The chip IOCON address schanges from 0x05 to 0x0A
        # when BANK is changed.
        # 
        BANK   = 0 << 7 # seaquental adresses
        MIRROR = 1 << 6 # INT pins are internally connected
        SEQOP  = 1 << 5 # seaquental mode disabled
        DISSLW = 1 << 4 # 
        HAEN   = 1 << 3 # 
        ODR    = 0 << 2 # int pin is not open drain output
        INTPOL = 1 << 1 # active high
        #
        # Write the configuration
        setup = BANK + MIRROR + SEQOP + DISSLW + HAEN + ODR + INTPOL
        bus.write_word_data(i2c_addr, 0x05, setup)
    
    def interrupt(self, queue):
        blocks = Blocs()                                # 
        word = self.read(self.i2c_addr, self.INTFA)     # Reads the Interrup register: two bytes of data

        for bank in [0,1]:                              # Iterate the two banks of bytes
            blocks.asByte = word[bank]                  
            for bit in range(7):                        # length of block is two bytes, a word
                if block[bit] == 1:                     # when the bit is found
                    index = (bank, bit)                 # its location is stored as index    # is this necessary?
                    break                               # and the search stops.
        word = self.read(self.i2c_addr, self.OLAT)      # Reads the Input Register: two bytes of data
        
        blocks.asByte = word[index[0]]
        queue.put(block.index[1])                       # the index of the 1-bit
        
    def readBit(self, index, address = self.OLAT):
        word = self.read_word(self.i2c_addr, address)
        return testBit(word, index)
        
        #blocks = Blocs()
        #blocks.asByte = self.read(self.i2c_addr, self.INTCAPA, address)
        #return blocks.index
        
    def writeBit(self, bit, index, address = self.OLAT):
            
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



# from code example from https://wiki.python.org/moin/BitManipulation 
# "Bit fields, e.g. for communication protocols"

# c_uint8 = ctypes.c_uint8
# 
# class  Blocs_bits( ctypes.LittleEndianStructure ):
#     _fields_ = [
#                     ("bit0",    c_uint8, 1),
#                     ("bit1",    c_uint8, 1),
#                     ("bit2",    c_uint8, 1),
#                     ("bit3",    c_uint8, 1),
#                     ("bit4",    c_uint8, 1),
#                     ("bit5",    c_uint8, 1),
#                     ("bit6",    c_uint8, 1),
#                     ("bit7",    c_uint8, 1),
#                     ]
#         
# class Blocks( ctypes.Union ):
#     _anonymous_ = ("bit")
#     _field_ = [
#         ("bit", Blocks_bits),
#         ("asByte", c_uint8)
#         ]
#     
## Example:
# blocks = Blocks()
# blocks.asByte = 0x2

        

if __name__ == '__main__':
    pass
