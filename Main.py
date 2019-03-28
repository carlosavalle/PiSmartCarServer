#from Socket2.SocketServer2  import *
#from GPIO.Motors.Motor import *
from Motor import *
from ultrasonic import *
from OCVObject import *
from SocketServer2 import *
from time import sleep
import socket
import sys
import threading

from flask import Flask, render_template, Response
from camarausb import Camera
from multiprocessing import Process

#Socket Server
#Ser = SocketServer2("192.168.156.47",888)
#Ser = SocketServer2("192.168.111.10",888)
#Ser = SocketServer2("172.0.0.1",888)
#Ss=Ser.Connect2()
image = None

#Start Motors

#Motor(IN1,IN2,PWM,STANDBY,(Reverse polarity?))


MotorB = Motor(22,27,17,25,False) #for Motor B 
MotorA = Motor(24,23,18,25,False) #For Motor A
MotorA.standby(True)
MotorB.standby(True)

_presitionForward = 80
_presitionBack = -50


app = Flask(__name__)


while False:
     distance = ultrasonic()
     print (distance.measureDistance())

@app.route('/')
def index():
    
    return render_template('index.html')


def gen(camera):
 
   
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
def genFollow(pimage):
    ObjectTrack = OCVObject()
    print("FollowObject")
  
    while True:
           
        # print(ObjectTrack.getPosition2())
        n = ObjectTrack.getPosition2()
        print(n)
        if n == -2:
            forward(0)
        if n == -1:
            forward(0)
            # print( " %s N/a"%str(n))


        if n in range(1,125):  #1,160
            forwardLeft(_presitionForward)
            #print( " %s is in the Left"%str(n))

        if n in range(126,290): #161,490
            forward(_presitionForward)
            #print( " %s is in the Middle"%str(n))

        if n in range(291,425): #491,637
            forwardRight(_presitionForward)
            #print( " %s is in the Right"%str(n))
        frame =   image = ObjectTrack.get_frameFollow()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
      
   
    


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(OCVObject()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_follow')
def videoFollow_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(genFollow(image),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




def ser():
    Ser = SocketServer2("192.168.153.142",888)
    #Ser = SocketServer2("192.168.111.10",888)
    #Ser = SocketServer2("172.0.0.1",888)
    Ss=Ser.Connect2()
    _direction = 0
    _forwardBackward = 0
    print ('Socket is now listening')
   # print(ObjectTrack.getPosition())
    _followObj =None
    while True:
        try:
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
            print(int(x[0:2])) 
            #from follow it
            #if (int(x[0:2]) ==  51):
            #    print("Open Follow It")
            #    #_followObj = threading.Thread(name='FollowObject', target=FollowObject)
            #    #_followObj.start()
            #if (int(x[0:2]) ==  50):
            #    print("Close Follow It")
            #    #_followObj.do_run = False
            #    #_followObj.join()
  


           
        except Exception as e: 
            print(e)
             
            #MotorB.drive(int(x[0:2]))

           # print ("X " + x[0:2])    
            #print ("Y " + x[2:7])    

       # s.close()
     
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


#ObjectTrack  = OCVObject()
#b = None

def FollowObject():
        t = threading.currentThread()
        ObjectTrack = OCVObject()
        print("FollowObject")
  
        while getattr(t, "do_run", True):
           
           # print(ObjectTrack.getPosition2())
            n = ObjectTrack.getPosition2()
            if n == -2:
                forward(0)
            if n == -1:
               forward(0)
               # print( " %s N/a"%str(n))


            if n in range(1,125):  #1,160
                forwardLeft(_presitionForward)
                #print( " %s is in the Left"%str(n))

            if n in range(126,290): #161,490
                forward(_presitionForward)
                #print( " %s is in the Middle"%str(n))

            if n in range(291,425): #491,637
                forwardRight(_presitionForward)
                #print( " %s is in the Right"%str(n))
            image = ObjectTrack.get_frameFollow()
def test():
   print("hola")


def WebCam():

      print("entro a webcam???")
      #h = threading.Thread(name='ObjectTracker', target=test)
      #h.start()
      
      # lo pase al servidor web
      s = threading.Thread(name='ObjectTracker', target=ser)
      s.start()
      
      #h.do_run = False
      #h.join()
      b = threading.Thread(name='ObjectTracker', target=app.run(host='0.0.0.0', debug=True, threaded=True))
      b.start()
      print("???")



   #while True:
        
   #     print("entro en test")
    
   #     b = threading.Thread(name='ObjectTracker', target=ObjectTrack.detectObject, args=("task",))
   #     b.start()
   #     sleep(2)
   #     b.do_run = False
   #     b.join()
   #     sleep(5)
   #     b = threading.Thread(name='ObjectTracker', target=ObjectTrack.detectObject, args=("task",))
   #     b.start()
   #     sleep(10)
   #     b.do_run = False
   #     b.join()
   # #while getattr(test1, "do_run", True):
          
   




#b = threading.Thread(name='ObjectTracker', target=ObjectTrack.detectObject, args=("task",))
#b.start()
#sleep(2)


#f = threading.Thread(name='SocketServer', target=ser)

#test1 = threading.Thread(name='Hola', target=test)

#test1.start()

WebCam()




#sleep(5)
#b.do_run = False
#b.join()
#test1.do_run = False
#test1.join()


#f.start()













#   def forward(speed):
#    print("forward")
#    MotorA.drive(0)
#    MotorB.drive(speed)

#def forwardLeft(speed):
#    print("forwardLeft")
#    MotorA.drive(-100)
#    MotorB.drive(speed)

#def forwardRight(speed):
#    print("forwardRight")
#    MotorA.drive(100)
#    MotorB.drive(speed)

#def backward(speed):
#    print("backward")
#    MotorA.drive(0)
#    MotorB.drive(speed)

#def backwardRight(speed):
#    print("backwardRight")
#    MotorA.drive(-100)
#    MotorB.drive(speed)

#def backwardLeft(speed):
#    print("backwardLeft")
#    MotorA.drive(100)
#    MotorB.drive(speed)


   
#def FollowObject():
#        while False:
#            print(ObjectTrack.getPosition())
#            n = ObjectTrack.getPosition()
#            if n == -2:
#                forward(0)
#            if n == -1:
#               forward(0)
#               # print( " %s N/a"%str(n))


#            if n in range(1,125):  #1,160
#                forwardLeft(_presitionForward)
#                #print( " %s is in the Left"%str(n))

#            if n in range(126,290): #161,490
#                forward(_presitionForward)
#                #print( " %s is in the Middle"%str(n))

#            if n in range(291,425): #491,637
#                forwardRight(_presitionForward)
#                #print( " %s is in the Right"%str(n))

   

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
    MotorB.drive(_presitionForward)
    sleep(0.5)
    MotorB.drive(0)
    sleep(0.5)
    MotorB.drive(_presitionBack)
    sleep(0.5)
    MotorB.drive(0)





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

