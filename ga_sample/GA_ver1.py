#!/usr/bin/env python

#list
#3152315231523152
#moving time : 10 seconds (80)
#number of 1 geberaton : 20

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


def init():
    #left
    port.write(bytearray.fromhex("FF FF 03 05 03 1E 00 02 D4"))
    port.write(bytearray.fromhex("FF FF 01 05 03 1E 00 02 D6"))
    #right
    port.write(bytearray.fromhex("FF FF 05 05 03 1E 00 02 D2"))
    port.write(bytearray.fromhex("FF FF 02 05 03 1E 00 02 D5"))
    

port = serial.Serial("/dev/ttyAMA0", baudrate=1000000, timeout=3.0)

#global variable
parents_info = [[0 for i in range(80)] for j in range(20)]
distance = [[i,0] for i in range(20)]

#start messages
print 'input generation'
generation = input('> ')
print u'generation %d : ok?(y or n)' % generation
message = raw_input('> ')

if message == 'y':
    
    #read parents_file
    parents_filename = 'generation%d.dat' % generation
    
    line_number = 0
    
    for line in open(parents_filename, 'r'):
        itemList = line.split('\t')
        numbers = []
        
        for item in itemList:
            numbers.append( int(item) )
            
        servo3 = ['' for i in range(20)]
        servo1 = ['' for i in range(20)]
        servo5 = ['' for i in range(20)]
        servo2 = ['' for i in range(20)]
        
        #make sirial command
        for i in range(0, 80):
            if i%4 == 0 : #servo3
                x7 = numbers[i] % 256
                x8 = numbers[i] / 256
                x9 = calc_checksum(03, 05, 03, 30, x7, x8)
                servo3[i/4] = 'FF FF 03 05 03 1E %02X %02X %02X' % (x7, x8, x9)
            elif i%4 == 1 : #servo1
                x7 = numbers[i] % 256
                x8 = numbers[i] / 256
                x9 = calc_checksum(01, 05, 03, 30, x7, x8)
                servo1[i/4] = 'FF FF 01 05 03 1E %02X %02X %02X' % (x7, x8, x9)
            elif i%4 == 2 : #servo5
                x7 = numbers[i] % 256
                x8 = numbers[i] / 256
                x9 = calc_checksum(05, 05, 03, 30, x7, x8)
                servo5[i/4] = 'FF FF 05 05 03 1E %02X %02X %02X' % (x7, x8, x9)
            else : #servo2
                x7 = numbers[i] % 256
                x8 = numbers[i] / 256
                x9 = calc_checksum(02, 05, 03, 30, x7, x8)
                servo2[i/4] = 'FF FF 02 05 03 1E %02X %02X %02X' % (x7, x8, x9)
                
        #send sirial command
        time.sleep(2)
        init()
        print 'Please input character'
        enter = raw_input('> ')
        for i in range(0, 20):
            port.write(bytearray.fromhex(servo3[i]))
            port.write(bytearray.fromhex(servo1[i]))
            port.write(bytearray.fromhex(servo5[i]))
            port.write(bytearray.fromhex(servo2[i]))
            print i
            time.sleep(0.5)
            
        print 'enter distance X[mm] (%d/20)' % int(line_number + 1)
        distance[int(line_number)][1] = input('> ')
        parents_info[int(line_number)] = copy.deepcopy(numbers)
        
        line_number += 1
        
    ranking = sorted(distance, key=lambda x: int(x[1]), reverse=True)

    children_info = [[0 for i in range(80)] for j in range(20)]
    
    #make child
    for i in range(0,4):
        if ranking[i/2][1] > 0:
            children_info[i] = copy.deepcopy(parents_info[ranking[i/2][0]])
        else:
            children_info[i] = [random.randint(0,300) + 362 for j in range(80)]
            
    #swap info
    #before 1 1 2 2 3 4 5 ...
    #after  1 2 1 2 3 4 5 ...
    tmp_info = copy.deepcopy(children_info[1])
    children_info[1] = copy.deepcopy(children_info[2])
    children_info[2] = copy.deepcopy(tmp_info)
    
    for i in range(4,20):
        if ranking[i-2][1] > 0:
            children_info[i] = copy.deepcopy(parents_info[ranking[i-2][0]])
        else:
            children_info[i] = [random.randint(0,300) + 362 for j in range(80)]
            
    #keep elite (1st, 2nd)
    #crossing
    
    for i in range(1,10):
        sep_line = random.randint(1,78)
        tmp = copy.deepcopy(children_info[i*2][sep_line:])
        children_info[i*2][sep_line:] = copy.deepcopy(children_info[i*2+1][sep_line:])
        children_info[i*2+1][sep_line:] = copy.deepcopy(tmp)
        
    #mutation
    for i in range(0,70):
        #biont
        x = random.randint(2,19)
        #place
        y = random.randint(0,79)
        #value
        value = random.randint(0,300) + 362
        #print u'x:%d y:%d value:%d' % (x, y, value)
        children_info[x][y] = value
        
    #add result
    result_file = open('result.dat', 'a')
    generation_info = 'Generation : %d\n' % generation
    result_file.write(str(generation_info))
    average = 0
    for i in range(0,20):
        average += ranking[i][1]
        info = '%d\t' % ranking[i][1]
        result_file.write(str(info))
    result_file.write('\n')
    average = average * 1.0
    average = average / 20
    average_info = 'Average : %f' % average
    result_file.write(average_info)
    result_file.write('\n')
    result_file.write('\n')
    result_file.close()
        
    #write children_file
    generation += 1
    children_filename = 'generation%d.dat' % generation
    children_file = open(children_filename, 'w')
    for i in range(0,20):
        for j in range(0,80):
            children_file.write(str(children_info[i][j]))
            if j < 79:
                children_file.write('\t')
        if i < 19:
            children_file.write('\n')

    print u'made %s' % children_file
    children_file.close()

    print 'finish'
    
else:
    print 'cancel'
