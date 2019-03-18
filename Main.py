#from Socket2.SocketServer2  import *
#from GPIO.Motors.Motor import *
from Motor import *
from OCVObject import *
from SocketServer2 import *
from time import sleep
import socket
import sys
import threading

#Socket Server
#Ser = SocketServer2("192.168.43.201",888)
Ser = SocketServer2("192.168.111.10",888)
#Ser = SocketServer2("172.0.0.1",888)
Ss=Ser.Connect2()


#Start Motors

#Motor(IN1,IN2,PWM,STANDBY,(Reverse polarity?))
MotorB = Motor(24,23,18,25,False) #for Motor B 
MotorA = Motor(22,27,17,25,False) #For Motor A
MotorA.standby(True)
MotorB.standby(True)

_direction = 0
_forwardBackward = 0

def forward(speed):
    print("forward")
    MotorA.drive(0)
    MotorB.drive(speed)

def forwardLeft(speed):
    print("forwardLeft")
    MotorA.drive(-100)
    MotorB.drive(speed)

def forwardRight(speed):
    print("forwardRight")
    MotorA.drive(100)
    MotorB.drive(speed)

def backward(speed):
    print("backward")
    MotorA.drive(0)
    MotorB.drive(speed)

def backwardRight(speed):
    print("backwardRight")
    MotorA.drive(-100)
    MotorB.drive(speed)

def backwardLeft(speed):
    print("backwardLeft")
    MotorA.drive(100)
    MotorB.drive(speed)

def ser():
    print ('Socket is now listening')
   # print(ObjectTrack.getPosition())
    while 1:
        conn, addr = Ss.accept()
        # print ('Connect with ' + addr[0] + ':' + str(addr[1]))
        buf = conn.recv(5)
    
        #print (buf.decode()) 
        x = buf.decode()
    
        #middle
        if (int(x[2:7]) >= -1 and int(x[2:7]) <= 1 and _direction !=0):
            _direction = 0          
            MotorA.drive(0)    
        # Turn Right
        if (int(x[2:7]) >= 2 and _direction !=2):
          _direction = 2
          MotorA.drive(100)    
        #Turn Left
        if (int(x[2:7]) <= -2 and _direction !=-2):
           _direction = -2
           MotorA.drive(-100)

        #forward  
    
        if (int(x[0:2]) <= 2 and _forwardBackward !=2):
           _forwardBackward = 2
           MotorB.drive(100)

        if (int(x[0:2]) == 3 and _forwardBackward !=3):
           _forwardBackward = 3
           MotorB.drive(80)

        if (int(x[0:2]) == 4 and _forwardBackward !=4):
           _forwardBackward = 4
           MotorB.drive(60)
    
        if (int(x[0:2]) == 5 and _forwardBackward !=5):
           _forwardBackward = 5
           MotorB.drive(0)

        if (int(x[0:2]) == 6 and _forwardBackward !=6):
           _forwardBackward = 6
           MotorB.drive(0)

        # backward
        if (int(x[0:2]) == 7 and _forwardBackward !=7):
           _forwardBackward = 7
           MotorB.drive(-60)

        if (int(x[0:2]) == 8 and _forwardBackward !=8):
           _forwardBackward = 8
           MotorB.drive(-75)

        if (int(x[0:2]) == 9 and _forwardBackward !=9):
           _forwardBackward = 9
           MotorB.drive(-90)

        if (int(x[0:2]) == 10 and _forwardBackward !=10):
           _forwardBackward = 10
           MotorB.drive(-100)


        #MotorB.drive(int(x[0:2]))

       # print ("X " + x[0:2])    
        #print ("Y " + x[2:7])    

    s.close()








ObjectTrack  = OCVObject()
b = threading.Thread(name='ObjectTracker', target=ObjectTrack.detectObject)


f = threading.Thread(name='SocketServer', target=ser)
b.start()

#f.start()




def forward(speed):
   # print("forward")
    MotorA.drive(0)
    MotorB.drive(speed)

def forwardLeft(speed):
    #print("forwardLeft")
    MotorA.drive(-100)
    MotorB.drive(speed)

def forwardRight(speed):
    #print("forwardRight")
    MotorA.drive(100)
    MotorB.drive(speed)

def backward(speed):
    #print("backward")
    MotorA.drive(0)
    MotorB.drive(speed)

def backwardRight(speed):
    #print("backwardRight")
    MotorA.drive(-100)
    MotorB.drive(speed)

def backwardLeft(speed):
    #print("backwardLeft")
    MotorA.drive(100)
    MotorB.drive(speed)

_presitionForward = 40
_presitionBack = -40


while True:
    n = ObjectTrack.getPosition()
    if n == -1:
        backwardLeft(_presitionBack)
       # print( " %s N/a"%str(n))


    if n in range(0,259):
        backwardRight(_presitionBack)
        #print( " %s is in the Left"%str(n))

    if n in range(260,370):
        forward(_presitionForward)
        #print( " %s is in the Middle"%str(n))

    if n in range(371,637):
        backwardLeft(_presitionBack)
        #print( " %s is in the Right"%str(n))

   

_TestMotor = False

if _TestMotor == True:
    MotorA.drive(-100)
    sleep(0.5)
    MotorA.drive(0)
    sleep(0.5)
    MotorA.drive(100)
    sleep(0.5)
    MotorA.drive(0)
    sleep(0.5)
    MotorB.drive(0)
    sleep(0.5)
    MotorB.drive(50)
    sleep(0.5)
    MotorB.drive(0)
    sleep(0.5)
    MotorB.drive(-50)









#test.drive(100) #Forward 100% dutycycle
#sleep(3)

#test.brake() #Short brake
#sleep(1)
#test.drive(-50) #Backwards 100% dutycycle
#sleep(3)
#test.brake() #Short brake
#sleep(0.1)
#test.clear()

##Enable standby
#test.standby(False) #Disable standby

