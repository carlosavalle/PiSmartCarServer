# python dynamic_color_tracking.py --filter HSV --webcam

import cv2
import argparse
import numpy as np
import threading



class OCVObject:
    _position = 0
    
   # def __init__(self):
       # self.main()

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


    def detectObject(self):
        range_filter ='HSV'
        camera = cv2.VideoCapture(0)
        self.setuptrackbars(range_filter)
        while True:

            ret, image = camera.read()
            #image = cv2.flip(image,1)
            
            frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            #v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)
            v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = self.gettrackbarvalues(range_filter)
            #v2_min = 87
            #lenovo cam
            #v1_min = 22
            #v2_min = 107
            #v3_min = 95
            #v1_max = 67
            #v2_max = 255
            #v3_max = 255

            #logitec cam
            v1_min = 24
            v2_min = 34
            v3_min = 42
            v1_max = 60
            v2_max = 115
            v3_max = 248
            
            thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

            kernel = np.ones((5,5),np.uint8)
            mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
 
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
                # only proceed if the radius meets a minimum size
                if radius > 10:
                    #print(center[0])
                    self._position = center[0]
                   
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(image, center, 3, (0, 0, 255), -1)
                    cv2.putText(image,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                    cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                else:
                    self._position = -1
 
            # show the frame to our screen
            cv2.imshow("Original", image)
           # cv2.imshow("Thresh", thresh)
            #cv2.imshow("Mask", mask)

            if cv2.waitKey(1) & 0xFF is ord('q'):
                break
    def getPosition(self):
        return self._position
