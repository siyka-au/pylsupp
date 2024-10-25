from serial import PARITY_EVEN, Serial, SerialException

from pylsupp import LumasensePyrometer

serial = Serial(baudrate=38400, parity=PARITY_EVEN)

pyro = LumasensePyrometer(serial)
pyro.