#!usr/bin/python

import RPi.GPIO as GRIO
import time
GPIO.setmode(GPIO.BCM)
LED = 2
GPIO.setup(LED, GPIO.OUT)
for i in range(10):
    GPIO.output(LED, GPIO.HIGH)
    print 'LED HIGH'
    time.sleep(1)
    GPIO.output(LED, GPIO.LOW)
    print 'LED LOW'
    time.sleep(1)
GPIO.cleanup()
