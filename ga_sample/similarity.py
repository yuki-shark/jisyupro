#!/usr/bin/env python

#import serial
import time
import random
import copy
#import RPi.GPIO as GPIO

#global variable
parents_info = [[0 for i in range(80)] for j in range(20)]
#distance = [[i,0] for i in range(20)]

#start messages
print 'input generation (calculate similarity)'
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
            
        parents_info[int(line_number)] = copy.deepcopy(numbers)
        
        line_number += 1
        
    same_number = 0
    total_number = 0
    #calcurate similarity
    for i in range(0,20):
        for j in range(i+1,20):
            for k in range(0,80):
                if parents_info[i][k] == parents_info[j][k] :
                    same_number += 1
                total_number += 1
    similarity = same_number * 100.0 / total_number
    print 'Similarity : %lf' % similarity
    
    #add similarity file
    similarity_file = open('similarity.dat', 'a')
    generation_info = 'Generation : %d\n' % generation
    similarity_file.write(str(generation_info))
    info = 'Similarity : %lf \n' % similarity
    similarity_file.write(str(info))
    similarity_file.write('\n')
    similarity_file.close()
    
    print 'finish'
    
else:
    print 'cancel'
    
