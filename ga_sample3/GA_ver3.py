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

def init():
    #left
    port.write(bytearray.fromhex("FF FF 03 05 03 1E 00 02 D4"))
    port.write(bytearray.fromhex("FF FF 01 05 03 1E 00 02 D6"))
    time.sleep(0.2)
    #right
    port.write(bytearray.fromhex("FF FF 05 05 03 1E 00 02 D2"))
    port.write(bytearray.fromhex("FF FF 02 05 03 1E 00 02 D5"))

port = serial.Serial("/dev/ttyAMA0", baudrate=1000000, timeout=3.0)

#global variable
parents_info = [[[0 for i in range(80)] for j in range(5)] for k in range(4)]
distance = [[[i,0] for i in range(5)] for k in range(4)]

#start messages
print 'input generation'
generation = input('> ')
print u'generation %d : ok?(y or n)' % generation
message = raw_input('> ')

if message == 'y':
    
    #read parents_file
    parents_filename = 'generation3_%d.dat' % generation
    
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
        time.sleep(2)
        init()
        print 'Please input character'
        enter = raw_input('> ')
                                
        for i in range(0, 20):
            port.write(bytearray.fromhex(servo3[i]))
            port.write(bytearray.fromhex(servo1[i]))
            port.write(bytearray.fromhex(servo5[i]))
            port.write(bytearray.fromhex(servo2[i]))
            print (i+1)
            time.sleep(0.5)
            
        print 'Island : %d  Number : %d' % (int(line_number/5), int(line_number%5 + 1))
        print 'enter distance X[mm] (%d/20)' % int(line_number + 1)
        distance[int(line_number/5)][int(line_number%5)][1] = input('> ')
        parents_info[int(line_number/5)][int(line_number%5)] = copy.deepcopy(numbers)
        
        line_number += 1
        
    ranking = [[[0,0] for i in range(5)] for k in range(4)]
    for i in range(0,4):
        ranking[i] = sorted(distance[i], key=lambda x: int(x[1]), reverse=True)
        
    children_info = [[[0 for i in range(80)] for j in range(5)] for k in range(4)]
    
    #make child (Ver3)
    for i in range(0,20):
        if i%5 == 0:
            if ranking[i/5][i%5][1] > 0:
                children_info[i/5][i%5] = copy.deepcopy(parents_info[i/5][ranking[i/5][i%5][0]])
            else:
                children_info[i/5][i%5] = [random.randint(0,1) for j in range(80)]
        else:
            if ranking[i/5][i%5-1][1] > 0:
                children_info[i/5][i%5] = copy.deepcopy(parents_info[i/5][ranking[i/5][i%5-1][0]])
            else:
                children_info[i/5][i%5] = [random.randint(0,1) for j in range(80)]
                
    #keep elite (1st for each)
    #crossing    
    for i in range(0,4):
        for j in range(1,3):
            sep_line = random.randint(1,78)
            tmp = copy.deepcopy(children_info[i][j*2-1][sep_line:])
            children_info[i][j*2-1][sep_line:] = copy.deepcopy(children_info[i][j*2][sep_line:])
            children_info[i][j*2][sep_line:] = copy.deepcopy(tmp)
            
    #mutation
    for i in range (0,4):
        for j in range(0,20):
            #biont
            x = random.randint(1,4)
            #place
            y = random.randint(0,79)
            #reverse
            children_info[i][x][y] = 1 - children_info[i][x][y]
            
    #immigration
    if generation%10 == 0:
        case = random.randint(0,8)
        immigrate = [[0,0] for i in range(4)]
        if case == 0:
            immigrate[0][0] = 1
            immigrate[1][0] = 2
            immigrate[2][0] = 3
            immigrate[3][0] = 0
        elif case == 1:
            immigrate[0][0] = 3
            immigrate[1][0] = 0
            immigrate[2][0] = 1
            immigrate[3][0] = 2
        elif case == 2:
            immigrate[0][0] = 2
            immigrate[1][0] = 3
            immigrate[2][0] = 1
            immigrate[3][0] = 0
        elif case == 3:
            immigrate[0][0] = 3
            immigrate[1][0] = 2
            immigrate[2][0] = 0
            immigrate[3][0] = 1
        elif case == 4:
            immigrate[0][0] = 2
            immigrate[1][0] = 0
            immigrate[2][0] = 3
            immigrate[3][0] = 1
        elif case == 5:
            immigrate[0][0] = 1
            immigrate[1][0] = 3
            immigrate[2][0] = 0
            immigrate[3][0] = 2
        elif case == 6:
            immigrate[0][0] = 2
            immigrate[1][0] = 3
            immigrate[2][0] = 0
            immigrate[3][0] = 1
        elif case == 7:
            immigrate[0][0] = 1
            immigrate[1][0] = 0
            immigrate[2][0] = 3
            immigrate[3][0] = 2
        else:
            immigrate[0][0] = 3
            immigrate[1][0] = 2
            immigrate[2][0] = 1
            immigrate[3][0] = 0

        #elite remain island    
        for i in range(0,4):
            immigrate[i][1] = random.randint(1,4)
            
        immigrant = [[0 for i in range(80)] for j in range(4)]
        for i in range(0,4):
            immigrant[i] = copy.deepcopy(children_info[i][immigrate[i][1]])
            
        for i in range(0,4):
            children_info[immigrate[i][0]][immigrate[immigrate[i][0]][1]] = copy.deepcopy(immigrant[i])
            
    #add result
    result_file = open('result3.dat', 'a')
    generation_info = 'Generation : %d\n' % generation
    result_file.write(str(generation_info))
    whole_average = 0
    for i in range(0,4):
        info_island = '\tIsland : %d\n' % i
        result_file.write(info_island)
        average = 0
        for j in range(0,5):
            average += ranking[i][j][1]
            info = '\t%d' % ranking[i][j][1]
            result_file.write(str(info))
        result_file.write('\n')
        whole_average += average
        average *= 0.20
        average_info = '\t\tAverage : %f\n' %average
        result_file.write(average_info)
    whole_average *= 0.05
    whole_average_info = 'Whole Average : %f\n' % whole_average
    result_file.write(whole_average_info)
    result_file.write('\n')
    #immigration info
    if generation%10 == 0:
        immi_number = generation / 10
        immigration_info = 'Immigration : %d\n' % immi_number
        result_file.write(str(immigration_info))
        immi_0 = '\tImmigrant_0 (0,%d) --> Island_%d\n' % (immigrate[0][1], immigrate[0][0])
        immi_1 = '\tImmigrant_1 (1,%d) --> Island_%d\n' % (immigrate[1][1], immigrate[1][0])
        immi_2 = '\tImmigrant_2 (2,%d) --> Island_%d\n' % (immigrate[2][1], immigrate[2][0])
        immi_3 = '\tImmigrant_3 (3,%d) --> Island_%d\n' % (immigrate[3][1], immigrate[3][0])
        result_file.write(str(immi_0))
        result_file.write(str(immi_1))
        result_file.write(str(immi_2))
        result_file.write(str(immi_3))
        result_file.write('\n')
    result_file.close()
            
    #write children_file
    generation += 1
    children_filename = 'generation3_%d.dat' % generation
    children_file = open(children_filename, 'w')
    for i in range(0,20):
        for j in range(0,80):
            children_file.write(str(children_info[i/5][i%5][j]))
            if j < 79:
                children_file.write('\t')
        if i < 19:
            children_file.write('\n')
            
    print u'made %s' % children_file
    children_file.close()

    time.sleep(2)
    init()
    print 'finish'
    
else:
    print 'cancel'
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
