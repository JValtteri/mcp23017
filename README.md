# RPi-MCP23017-Lite
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

The module has been desined for the primary purpose of easily expanding the GPIO of projects using `RPi.GPIO` on Raspberry Pi. This module adds support for **MCP23017** expansion chips and a wrapper to enable calling both: `RPi.GPIO` and `MCP23017` as one. This means that no other code changes are required than changeing the import statement from ```from RPi.GPIO import GPIO``` to ```from mcp23017 import GPIO```. 
**THE SYNTAX STAYS THE SAME.**

The internal GPIO pin numbers stay the same. The first expander's GPIO pins are *100..116*, second's *200..216* and so forth. This is to make implementation as simple as possible.

#### THIS LIBRARY ***DOES NOT*** PROVIDE COMPLETE ACCESS TO ALL THE FEATURES OF THE MCP23017 CHIP.
For complete access refer to other libraries, such as [***smbus2***](https://pypi.org/project/smbus2/) or [***RPi-MCP23017***](https://pypi.org/project/RPi-MCP23017/). 

### Use:

example:
```python3
from mcp23017 import GPIO

gpio_pin = 116

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, GPIO.PUD_UP)
value = GPIO.input(gpio_pin)
print(value)
GPIO.cleanup()
```


#### Currentlu supported functions:

 - ```GPIO.setmode()``` *(mandatory)*
 - ```GPIO.setup()```
 - ```GPIO.input()```
 - ```GPIO.cleanup()```

Internally the module works exclusively in *word* or *two byte* *(16 bit)* mode.

### Planned features:

 - Interrupts
 - Cashe the state of inputs to speed up read requests
 - Proper support for outputs
