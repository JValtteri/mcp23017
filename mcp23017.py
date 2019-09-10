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
        self.i2c_addr  = i2c_addr
        self.write = bus.write_byte_data  # Consider write block..!
        self.read = bus.read_word_data
        
        # Init chip for unified I/O
        # Warning!
        # The chip IOCON address schanges from 0x05 to 0x0A
        # when BANK is changed.
        # 
        BANK = 0 << 7 # seaquental adresses
        MIRROR = 1 << 6 # INT pins are internally connected
        SEQOP = 1 << 5 # seaquental mode disabled
        DISSLW = 1 << 4
        HAEN = 1 << 3
        ODR = 0 << 2 # int pin is not open drain output
        INTPOL = 1 << 1 # active high
        #
        # Write the configuration
        setup = BANK + MIRROR + SEQOP + DISSLW + HAEN + ODR + INTPOL
        bus.write_byte_data(i2c_addr, 0x05, setup)
        
        self.IODIRA = 0x00 # I/O mode (def 0xFF
        self.IODIRB = 0x01 # I/O mode (def 0xFF
        self.IPOLA = 0x02 # Input polarity
        self.IPOLB = 0x03
        self.GPINTENA = 0x04 # Interrupt on change
        self.GPINTENB = 0x05
        self.IOCON = 0A  # BANK SEQOP DISSW HEAN ODR INTPOL
        
        self.INTFA = 0E # Interrupt activated flag
        self.INTFB = 0F # Interrupt activated flag
        self.INTCAPA = 10 #Interrupt capture register (resets when read)
        self.INTCAPB = 11 #Interrupt capture register (resets when read)
        
        self.GPIO = # Input status
        self.OLAT = # output status
        
        # Input state memory
        # state is updated ....... sometimes
        self.state_a = 0x00
        self.state_b = 0x00

    
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
    
        blocks = Blocs()
        blocks.asByte = self.read(self.i2c_addr, self.INTCAPA, address)
        return blocks.index

    def write():
    
    def run():
        
        
        
        while True:
            time.sleep(10)
            

# from code example from wiki.python.org "BitManipulation"

class  Blocs_bits( ctypes.LittleEndianStructure ):
    _fields_ = [
                    ("bit0",    c_uint8, 1),
                    ("bit1",    c_uint8, 1),
                    ("bit2",    c_uint8, 1),
                    ("bit3",    c_uint8, 1),
                    ("bit4",    c_uint8, 1),
                    ("bit5",    c_uint8, 1),
                    ("bit6",    c_uint8, 1),
                    ("bit7",    c_uint8, 1),
                    ]
        
class Blocks( ctypes.Union ):
    _anonymous_ = ("bit")
    _field_ = [
        ("bit", Blocks_bits),
        ("asByte", c_uint8)
        ]
        
#
