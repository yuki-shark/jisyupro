import serial
import time
import RPi.GPIO as GPIO

port = serial.Serial("/dev/ttyAMA0", baudrate=1000000, timeout=3.0)

#left
port.write(bytearray.fromhex("FF FF 03 05 03 1E 00 02 D4"))
port.write(bytearray.fromhex("FF FF 01 05 03 1E 00 02 D6"))
#right
port.write(bytearray.fromhex("FF FF 05 05 03 1E 00 02 D2"))
port.write(bytearray.fromhex("FF FF 02 05 03 1E 00 02 D5"))
