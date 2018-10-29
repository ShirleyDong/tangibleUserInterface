from collections import  deque

import numpy as np

#import imutils

import cv2

import socket
import time


UDP_IP = "127.0.0.1"

UDP_PORT = 5065



print("UDP target IP:", UDP_IP)

print("UDP target port:", UDP_PORT)

#print "message:", MESSAGE



sock = socket.socket(socket.AF_INET, # Internet

                     socket.SOCK_DGRAM) # UDP

def nothing(x):
    pass

mybuffer = 64

pts = deque(maxlen=mybuffer)


camera = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")
 
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

time.sleep(2)


while True:


    (ret, frame) = camera.read()


    if not ret:

        print ('No Camera')

        break

    #frame = imutils.resize(frame, width=600)


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
 
    redLower = np.array([l_h, l_s, l_v])
    redUpper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, redLower, redUpper)


    mask = cv2.erode(mask, None, iterations=2)


    mask = cv2.dilate(mask, None, iterations=2)


    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]


    center = None


    if len(cnts) > 0:


        c = max(cnts, key = cv2.contourArea)


        ((x, y), radius) = cv2.minEnclosingCircle(c)


        M = cv2.moments(c)

        x_co = int(M["m10"]/M["m00"])
        y_co = int(M["m01"]/M["m00"])
        center = (x_co, y_co)


        if radius > 10:

            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            print(str(x_co).encode("utf8"))
            sock.sendto(str(x_co).encode("utf8") , (UDP_IP, UDP_PORT))

            cv2.putText(frame,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
            cv2.putText(frame,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
            pts.appendleft(center)


            
    for i in range(1, len(pts)):

        if pts[i - 1] is None or pts[i] is None:

            continue


        thickness = int(np.sqrt(mybuffer / float(i + 1)) * 2.5)


        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    #res = cv2.bitwise_and(frame, frame, mask=mask)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Frame', frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    k = cv2.waitKey(5)&0xFF

    if k == 27:

        break


camera.release()


cv2.destroyAllWindows()

