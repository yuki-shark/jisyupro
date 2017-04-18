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
    port.write(bytearray.fromhex("FF FF 03 05 03 1E 96 02 3E"))
    port.write(bytearray.fromhex("FF FF 01 05 03 1E 6A 01 6D"))
    #right
    port.write(bytearray.fromhex("FF FF 05 05 03 1E 6A 01 69"))
    port.write(bytearray.fromhex("FF FF 02 05 03 1E 96 02 3F"))
    time.sleep(0.5)
    
    #left
    port.write(bytearray.fromhex("FF FF 03 05 03 1E 6A 01 6B"))
    port.write(bytearray.fromhex("FF FF 01 05 03 1E 96 02 40"))
    #right
    port.write(bytearray.fromhex("FF FF 05 05 03 1E 96 02 3C"))
    port.write(bytearray.fromhex("FF FF 02 05 03 1E 6A 01 6C"))
    time.sleep(0.5)
    
