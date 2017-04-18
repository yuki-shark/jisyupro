import random

file = open('generation3_1.dat', 'w')
#numbers = []
for i in range(0, 20):
        #numbers = []
    for j in range(0, 80):
        #numbers.appnd(random.randint(0,300))
        file.write(str(random.randint(0,1)))
        if j < 79 :
            file.write('\t')
    if i < 19 :
        file.write('\n')
        
file.close()
