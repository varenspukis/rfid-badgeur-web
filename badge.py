from serial import *

def readBadge(serial_port):
    if serial_port.isOpen():
        serial_port.write("BONJOUR\n".encode('ascii'))
        return int(serial_port.readline().decode('ascii'))
