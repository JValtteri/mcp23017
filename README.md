# MCP23017
## a RPI GPIO expansion

So you ran out of GPIO on your Raspberry Pi? 
And you have a ton of code using the RPi.GPIO?

With this library you can easily expand your GPIO with up to eight MCP23017 expansion chips.

### Purpose of this module

An easy to use module to:
 - read single bits*
 - write single bits*
 - read interrupts of single bits*
 
 *) from/to both local GPIO as well as multiple MCP23017 expansion chips.

Desired properties:
 - easy to use and understand
 - simple to implement
 - high performance**
 
 **) as high as can be achieved with Python3 without 
    endangering the former two.

The module has been desined for the primary purpose of easily expanding the GPIO of projects using RPi.GPIO on Raspberry Pi. This module adds support for MCP23017 expansion chips and a wrapper to enable calling both: RPi.GPIO and MCP23017 as one. This means that no other code changes are required than changeing the import statement from ```from RPi.GPIO import GPIO``` to ```from MCP23017 import GPIO```

### Current support:

 - ```RPI.setmode()``` (mandatory)
 - ```RPI.setup()```
 - ```RPI.input()```
 - ```RPI.cleanup()```

### Planned features:

 - Interrupts
 - Cashe the state of inputs to speed up read requests
 - Proper support for outputs

