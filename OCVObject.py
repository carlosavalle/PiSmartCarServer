
import cv2
import argparse
import numpy as np
import threading



class OCVObject():
    _position = 0
    _radius=0
    _stream = False
    _imageFollow = None
    
    def __init__(self):
        range_filter ='HSV'
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3,480) #320
        self.camera.set(4,240) #240

    def callback(self, value):
        pass


    def setuptrackbars(self, range_filter):
        cv2.namedWindow("Trackbars", 0)

        for i in ["MIN", "MAX"]:
            v = 0 if i == "MIN" else 255

            for j in range_filter:
                cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, self.callback)




    def gettrackbarvalues(self, range_filter):
        values = []

        for i in ["MIN", "MAX"]:
            for j in range_filter:
                v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
                values.append(v)
        return values

    def getPosition2(self):

            ret, image = self.camera.read()
           
            #image = cv2.flip(image,1)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
          

 
            #loweryellow = np.array([20, 50, 50])
            #upperyellow = np.array([40, 255, 255])
            
            # first
            #loweryellow = np.array([25, 50, 87])
            #upperyellow = np.array([38, 197, 255])
           
            #blue ball
            loweryellow = np.array([85, 120, 98])
            upperyellow = np.array([176, 255, 255])
           

            mask = cv2.inRange(hsv, loweryellow, upperyellow)
            

            
            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
 
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), self._radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                try:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                except:
                    print("center error")
                    self._position = -1
                    return self._position
                # only proceed if the radius meets a minimum size
               # print(self._radius)
                if self._radius > 10:
                    #print(center[0])
                    self._position = center[0]
                   
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(image, (int(x), int(y)), int(self._radius),(0, 255, 255), 2)
                    cv2.circle(image, center, 3, (0, 0, 255), -1)
                    cv2.putText(image,"Ball", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                    cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                else:
                    self._position = -1

            self._imageFollow = image  
            if self.getRadius() < 60:
                return self._position
            else:
                return -2
        
    
    #def detectObject(self):
    #    #t = threading.currentThread()
    #    #print("entro al wile")
    #    #while getattr(t, "do_run", True):
    #     while True:   
          

          
    #        ret, image = self.camera.read()
            
    #        #image = cv2.flip(image,1)
    #        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
          

 
    #        #loweryellow = np.array([20, 50, 50])
    #        #upperyellow = np.array([40, 255, 255])
            
    #        loweryellow = np.array([25, 50, 87])
    #        upperyellow = np.array([38, 197, 255])
           
    #        mask = cv2.inRange(hsv, loweryellow, upperyellow)
            

            
    #        # find contours in the mask and initialize the current
    #        # (x, y) center of the ball
    #        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    #        center = None
 
    #        # only proceed if at least one contour was found
    #        if len(cnts) > 3:
    #            # find the largest contour in the mask, then use
    #            # it to compute the minimum enclosing circle and
    #            # centroid
    #            c = max(cnts, key=cv2.contourArea)
    #            ((x, y), self._radius) = cv2.minEnclosingCircle(c)
    #            M = cv2.moments(c)
    #            try:
    #                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    #            except:
    #                print("center error")
                  
    #            # only proceed if the radius meets a minimum size
    #           # print(self._radius)
    #            if self._radius > 10:
    #                #print(center[0])
    #                self._position = center[0]
                   
    #                # draw the circle and centroid on the frame,
    #                # then update the list of tracked points
    #                cv2.circle(image, (int(x), int(y)), int(self._radius),(0, 255, 255), 2)
    #                cv2.circle(image, center, 3, (0, 0, 255), -1)
    #                cv2.putText(image,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
    #                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
    #            else:
    #                self._position = -1
 
    #        # show the frame to our screen
    #       # cv2.imshow("Original", image)
    #       # cv2.imshow("Thresh", thresh)
    #       # cv2.imshow("Mask", mask)

    #        if cv2.waitKey(1) & 0xFF is ord('q'):
    #            break
    
    def getPosition(self):
        if self.getRadius() < 38:
           return self._position
        else:
            return -2

    def getRadius(self):
        return self._radius
    def startStream(self):
        self._stream = True
    def stopStream(self):
        self._stream = False
    def get_frame(self):
        success, image = self.camera.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    def get_frameFollow(self):
       # success, image = self.camera.read()
        ret, jpeg = cv2.imencode('.jpg', self._imageFollow)
        return jpeg.tobytes()
    def __del__(self):
        self.camera.release()
