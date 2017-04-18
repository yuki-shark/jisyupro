import random

file = open('generation1.dat', 'w')
for i in range(0, 20):
    for j in range(0, 80):
        file.write(str(random.randint(0,300) + 362))
        if j < 79 :
            file.write('\t')
    if i < 19 :
        file.write('\n')
        
file.close()
