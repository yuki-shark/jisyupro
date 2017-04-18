import serial
import time
import RPi.GPIO as GPIO

port = serial.Serial("/dev/ttyAMA0", baudrate=1000000, timeout=3.0)

#servo1,servo3

#left
port.write(bytearray.fromhex("FF FF 03 05 03 1E 00 02 D4"))
port.write(bytearray.fromhex("FF FF 01 05 03 1E 00 02 D6"))
#right
port.write(bytearray.fromhex("FF FF 05 05 03 1E 00 02 D2"))
port.write(bytearray.fromhex("FF FF 02 05 03 1E 00 02 D5"))
time.sleep(1)

while True:
    #left
    port.write(bytearray.fromhex("FF FF 03 05 03 1E 64 02 70"))
    port.write(bytearray.fromhex("FF FF 01 05 03 1E 9C 01 3B"))
    #right
    port.write(bytearray.fromhex("FF FF 05 05 03 1E 9C 01 37"))
    port.write(bytearray.fromhex("FF FF 02 05 03 1E 64 02 71"))
    time.sleep(1)
    
    #left
    port.write(bytearray.fromhex("FF FF 03 05 03 1E 9C 01 39"))
    port.write(bytearray.fromhex("FF FF 01 05 03 1E 64 02 72"))
    #right
    port.write(bytearray.fromhex("FF FF 05 05 03 1E 64 02 6E"))
    port.write(bytearray.fromhex("FF FF 02 05 03 1E 9C 01 3A"))
    time.sleep(1)
    
