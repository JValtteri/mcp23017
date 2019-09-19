import smbus2
import ctypes

class MCP23017():

    def __init__(self, bus=1, i2c_addr = 0x20, ):
        """
        Class for controlling any number of MCP23017 chips
        Works as an interface and an expansion to smbus2.
        Specifically brings support for interrupts
        """
        
        # Init comms
        self.bus = smbus2.SMBus(bus)
        self.write = bus.write_byte_data  # Consider write block..!
        self.read = bus.read_byte_data
        
        ## CONSIDER USING READ BLOCK DATA!
        ## IT MAY READ BOTH A AND B REGISTERS
        ## INVESTIGATE!
        
        self.i2c_addr  = i2c_addr
        
        BANK = 0 << 7 # seaquental adresses
        MIRROR = 1 << 6 # INT pins are internally connected
        SEQOP = 1 << 5 # seaquental mode disabled
        DISSLW = 1 << 4
        HAEN = 1 << 3
        ODR = 0 << 2 # int pin is not open drain output
        INTPOL = 1 << 1 # active high
        
        setup = BANK + MIRROR + SEQOP + DISSLW + HAEN + ODR + INTPOL
        
        # Init chip for unified I/O
        # Warning!
        # The chip IOCON address schanges from 0x05 to 0x0A
        # when BANK is changed.
        # 
        self.write(i2c_addr, 0x05, setup)
        
        self.state_a = 0x00
        self.state_b = 0x00
        
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
        
    
    def interrupt(self, queue):
        
        blocks = Blocks()
        blocks.asByte = self.read(self.i2c_addr, self.INTFA)
        for i in range(15):     # length of block: 16 bits / d_word
            if blocks[i] == 1:  # finds the bit
                index = i       # is this necessary?
                break
        blocks.asByte = self.read(self.i2c_addr, self.OLAT)
        queue.put(blocks[index])   # the index of 1
        
    def readBit(self, index, address = None):
        if address == None:
            address = self.OLAT
        blocks = Blocks()
        blocks.asByte = self.read(self.i2c_addr, self.INTCAPA, address)
        return blocks.index

    #read_word_data(i2c_addr, register, force=None)

    # def write():
    #     pass
    
    # def run():
    #     while True:
    #         time.sleep(10)
            

# Tools to handle bit operations
# from code example from wiki.python.org "BitManipulation"
#
class  Blocs_bits( ctypes.LittleEndianStructure ):
    _fields_ = [
                    ("bit0",  c_uint8, 1),
                    ("bit1",  c_uint8, 1),
                    ("bit2",  c_uint8, 1),
                    ("bit3",  c_uint8, 1),
                    ("bit4",  c_uint8, 1),
                    ("bit5",  c_uint8, 1),
                    ("bit6",  c_uint8, 1),
                    ("bit7",  c_uint8, 1),
                    ]

class Blocks( ctypes.Union ):
    _anonymous_ = ("bit")
    _field_ = [
        ("bit", Blocks_bits),
        ("asByte", c_uint8)
        ]
        

if __name__ == '__main__':
    pass
