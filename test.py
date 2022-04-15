#!python

from spectramax import Spectramax
import sys

if len(sys.argv) != 2:
    print(
        """
        test.py - test communiction and print instrument errros
        Usage:
            ./test.py TTY
        TTY - serial device, for example, /dev/tty.usbserial-10
    """
    )
    exit(-1)

s = Spectramax(sys.argv[1])

for e in s.errors():
    print(e)
