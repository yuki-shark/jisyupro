import serial
import time
import RPi.GPIO as GPIO

port = serial.Serial("/dev/ttyAMA0", baudrate=1000000, timeout=3.0)

#servo1,servo3

while True:
    #left
    port.write(bytearray.fromhex("FF FF 03 05 03 1E 32 03 A1"))
    port.write(bytearray.fromhex("FF FF 01 05 03 1E 32 03 A3"))
    #right
    port.write(bytearray.fromhex("FF FF 02 05 03 1E CD 00 0A"))
    port.write(bytearray.fromhex("FF FF 05 05 03 1E CD 00 07"))
    time.sleep(1)

    #left
    port.write(bytearray.fromhex("FF FF 03 05 03 1E CD 00 09"))
    port.write(bytearray.fromhex("FF FF 01 05 03 1E CD 00 0b"))
    #right
    port.write(bytearray.fromhex("FF FF 02 05 03 1E 32 03 A2"))
    port.write(bytearray.fromhex("FF FF 05 05 03 1E 32 03 9F"))
    time.sleep(1)            
