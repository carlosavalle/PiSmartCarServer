import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class ultrasonic:


    def __init__(self):
        self.GPIO_TRIGGER = 21
        self.GPIO_ECHO = 20

        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

        GPIO.output(self.GPIO_TRIGGER, False)

        self.distance = 0

    def measureDistance(self):
        GPIO.output(self.GPIO_TRIGGER, False)
        time.sleep(0.5)
        GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
        start = time.time()
        while GPIO.input(self.GPIO_ECHO) == 0:
            start = time.time()

        while GPIO.input(self.GPIO_ECHO) == 1:
            stop = time.time()

        elapsed = stop - start
        distance = elapsed * 17150
        return distance

    #try:
    #    distance = measureDistance()
    #    while True:
    #        print (distance)
    #        time.sleep(0.1)
    #        distance = measureDistance()
    #except:
    #    time.sleep(1)
    #    GPIO.cleanup()
