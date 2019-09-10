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

