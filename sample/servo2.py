import serial
import time
import RPi.GPIO as GPIO

port = serial.Serial("/dev/ttyAMA0", baudrate=1000000, timeout=3.0)

while True:
    port.write(bytearray.fromhex("FF FF 02 05 03 1E 32 03 A2"))
    time.sleep(3)
    port.write(bytearray.fromhex("FF FF 02 05 03 1E CD 00 0A"))
    time.sleep(3)
    #port.write(bytearray.fromhex("FF FF 02 05 03 1E 00 02 D5"))
    #time.sleep(3)
         
                    
