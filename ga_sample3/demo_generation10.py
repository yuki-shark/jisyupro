#!/usr/bin/env python

#list
#3152315231523152
#moving time : 10 seconds (80)
#number of 1 geberaton : 20
#immigration span : 10

#0: 512 - 120 = 392 : 392
#1: 512 + 120 = 632 : 392 + 1*240

import serial
import time
import random
import copy
import RPi.GPIO as GPIO

def calc_checksum (num_1, num_2, num_3, num_4, num_5, num_6):
    ans = num_1 + num_2 + num_3 + num_4 + num_5 + num_6
    if ans > 255:
        ans = ans - 256
    return 255 - ans

port = serial.Serial("/dev/ttyAMA0", baudrate=1000000, timeout=3.0)

line = '1 1 1 1 1 0 1 0 0 1 1 0 0 1 1 1 0 0 1 0 1 0 0 0 0 1 0 1 1 1 0 1 0 0 0 0 1 0 1 1 0 0 1 0 0 0 1 1 1 0 1 0 0 1 0 0 1 0 1 0 1 1 0 1 0 0 0 0 0 0 0 0 1 1 1 0 0 1 1 0'

itemList = line.split()
numbers = []

for item in itemList:
    numbers.append( int(item) )
    
servo3 = ['' for i in range(20)]
servo1 = ['' for i in range(20)]
servo5 = ['' for i in range(20)]
servo2 = ['' for i in range(20)]

#make sirial command
for i in range(0, 80):
    val = 392 + 240 * numbers[i]
    if i%4 == 0 : #servo3
        x7 = val % 256
        x8 = val / 256
        x9 = calc_checksum(03, 05, 03, 30, x7, x8)
        servo3[i/4] = 'FF FF 03 05 03 1E %02X %02X %02X' % (x7, x8, x9)
    elif i%4 == 1 : #servo1
        x7 = val % 256
        x8 = val / 256
        x9 = calc_checksum(01, 05, 03, 30, x7, x8)
        servo1[i/4] = 'FF FF 01 05 03 1E %02X %02X %02X' % (x7, x8, x9)
    elif i%4 == 2 : #servo5
        x7 = val % 256
        x8 = val / 256
        x9 = calc_checksum(05, 05, 03, 30, x7, x8)
        servo5[i/4] = 'FF FF 05 05 03 1E %02X %02X %02X' % (x7, x8, x9)
    else : #servo2
        x7 = val % 256
        x8 = val / 256
        x9 = calc_checksum(02, 05, 03, 30, x7, x8)
        servo2[i/4] = 'FF FF 02 05 03 1E %02X %02X %02X' % (x7, x8, x9)
        
#send sirial command
for i in range(0, 20):
    port.write(bytearray.fromhex(servo3[i]))
    port.write(bytearray.fromhex(servo1[i]))
    port.write(bytearray.fromhex(servo5[i]))
    port.write(bytearray.fromhex(servo2[i]))
    print (i+1)
    time.sleep(0.5)
    
print 'finish'
                            
