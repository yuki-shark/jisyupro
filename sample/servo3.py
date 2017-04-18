import serial
import time
import RPi.GPIO as GPIO

port = serial.Serial("/dev/ttyAMA0", baudrate=1000000, timeout=3.0)

#while True:
#    port.write(bytearray.fromhex("FF FF 03 05 03 1E 32 03 A1"))
#    time.sleep(3)
#    port.write(bytearray.fromhex("FF FF 03 05 03 1E CD 00 09"))
#    time.sleep(3)
port.write(bytearray.fromhex("FF FF 03 05 03 1E 0c 02 c8"))
