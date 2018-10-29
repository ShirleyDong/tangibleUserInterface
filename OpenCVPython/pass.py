import cv2
from collections import  deque
import numpy as np
import socket
import time
import datetime


UDP_IP = "127.0.0.1"

UDP_PORT = 5065



print("UDP target IP:", UDP_IP)

print("UDP target port:", UDP_PORT)

#print "message:", MESSAGE



sock = socket.socket(socket.AF_INET, # Internet

                     socket.SOCK_DGRAM) # UDP

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
yellowArea = 0.0
blueArea = 0.0
greenArea = 0.0
redArea = 0.0
orangeArea = 0.0
pinkArea = 0.0
x_co = 0
y_co = 0
z_co = 0
knownWidth = 14
#define the range of purple color
purpleLower = np.array([115, 66, 0])
purpleUpper = np.array([179, 150, 194])

file_handle = open('data.txt', mode = 'w')
currentDT = str(datetime.datetime.now())

mybuffer = 64
pts = deque(maxlen=mybuffer)

camera = cv2.VideoCapture(0)
time.sleep(2)

while(1):

    (ret, frame) = cap.read()


    if not ret:

        print ('No Camera')

        break

    yList = []
    bList = []
    gList = []
    rList = []
    oList = []
    pList = []

    #convert rgb to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #define the range of the yellow color
    yellow_lower = np.array([22, 60, 200], np.uint8)
    yellow_upper = np.array([60, 255, 255], np.uint8)

    #define the range of the blue color
    blue_lower = np.array([93, 124, 0], np.uint8)
    blue_upper = np.array([130, 218, 162], np.uint8)

    #define the range of the blue color
    green_lower = np.array([35, 43, 46], np.uint8)
    green_upper = np.array([77, 255, 255], np.uint8)

    #define the range of the orange Color
    red_lower = np.array([0, 182, 162], np.uint8)
    red_upper = np.array([6,236,248], np.uint8)

    #define the range of the orange Color
    pink_lower = np.array([113, 98, 203], np.uint8)
    pink_upper = np.array([179,138,255], np.uint8)

    #define the color of the red color
    orange_lower = np.array([7, 194, 241], np.uint8)
    orange_upper = np.array([18,255,255], np.uint8)


    #find the range of these colors in frame
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)
    green = cv2.inRange(hsv, green_lower, green_upper)
    purple = cv2.inRange(hsv, purpleLower, purpleUpper)
    red = cv2.inRange(hsv, red_lower, red_upper)
    pink = cv2.inRange(hsv, pink_lower, pink_upper)
    orange = cv2.inRange(hsv, orange_lower, orange_upper)

    #Morphological transformation, Dilation
    kernal = np.ones((5,5), "uint8")

    yellow = cv2.dilate(yellow,kernal)
    res = cv2.bitwise_and(frame, frame, mask = yellow)

    blue = cv2.dilate(blue,kernal)
    res = cv2.bitwise_and(frame, frame, mask = blue)

    green = cv2.dilate(green,kernal)
    res = cv2.bitwise_and(frame, frame, mask = green)

    red = cv2.dilate(red,kernal)
    res = cv2.bitwise_and(frame, frame, mask = red)

    pink = cv2.dilate(pink,kernal)
    res = cv2.bitwise_and(frame, frame, mask = pink)

    orange = cv2.dilate(orange,kernal)
    res = cv2.bitwise_and(frame, frame, mask = orange)

    #track the object
    purple = cv2.erode(purple, None, iterations=2)
    purple = cv2.dilate(purple, None, iterations=2)
    cnts = cv2.findContours(purple.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    center = None
    if len(cnts) > 0:
        c = max(cnts, key = cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        if radius > 10:

            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #get the distance
            distance = (knownWidth * 713.57) / int(radius)
            z_co = int(distance)
            #print(z_co)
            cv2.putText(frame,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 255, 255),1)
            x_co = str(center[0])
            y_co = str(center[1])
            pts.appendleft(center)


    #detect the color
    #Tracking the yellow color
    (_, contours, hierarchy) = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        #c = max(contour, key = cv2.contourArea)
        if(area>300):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            cv2.putText(frame, "yellow", (x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255))
            #cv2.drawContours(frame, contour, -1, 255, 3)
            #c = max(contour)
            yList.append(area)
            yellowArea = max(yList)
            #print("red," + str(y_x) + "," + str(y_y))


    #Tracking the blue color
    (_, contours, hierarchy) = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        #c = max(contour, key = cv2.contourArea)
        if(area>300):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(frame, "blue", (x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0))
            #cv2.drawContours(frame, contour, -1, 255, 3)
            #c = max(contour, key = cv2.contourArea)
            bList.append(area)
            blueArea = max(bList)
            #print("red," + str(y_x) + "," + str(y_y))

    #Tracking the green color
    (_, contours, hierarchy) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        #c = max(contour, key = cv2.contourArea)
        if(area>300):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,102,0),2)
            cv2.putText(frame, "green", (x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,102,0))
            #cv2.drawContours(frame, contour, -1, 255, 3)
            #c = max(contour, key = cv2.contourArea)
            gList.append(area)
            greenArea = max(gList)

     #Tracking the pink color
    (_, contours, hierarchy) = cv2.findContours(pink, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        #c = max(contour, key = cv2.contourArea)
        if(area>300):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(153,102,255),2)
            cv2.putText(frame, "pink", (x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(153,102,255))
            #cv2.drawContours(frame, contour, -1, 255, 3)
            #c = max(contour, key = cv2.contourArea)
            pList.append(area)
            pinkArea = max(pList)

    #Tracking the red color
    (_, contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        #c = max(contour, key = cv2.contourArea)
        if(area>300):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(frame, "red", (x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255))
            #cv2.drawContours(frame, contour, -1, 255, 3)
            #c = max(contour, key = cv2.contourArea)
            rList.append(area)
            redArea = max(rList)

    #Tracking the orange color
    (_, contours, hierarchy) = cv2.findContours(orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        #c = max(contour, key = cv2.contourArea)
        if(area>300):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,153,255),2)
            cv2.putText(frame, "orange", (x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,153,255))
            #cv2.drawContours(frame, contour, -1, 255, 3)
            #c = max(contour, key = cv2.contourArea)
            oList.append(area)
            orangeArea = max(oList)

    cv2.imshow("Color Tracking", frame)

    if(yellowArea > 20.0 and blueArea > 20.0 and greenArea and pinkArea and redArea and orangeArea> 20.0):
        if(max(yellowArea, blueArea, greenArea, redArea, orangeArea) == yellowArea):
            #print("yellow,")
            data = "yellow," + str(x_co) + "," + str(y_co) + "," + str(z_co)
            print(data.encode("utf8"))
            sock.sendto(data.encode("utf8") , (UDP_IP, UDP_PORT))

        if(max(yellowArea, blueArea, greenArea, pinkArea, redArea, orangeArea) == blueArea):
            #print("blue")
            data = "blue," + str(x_co) + "," + str(y_co) + "," + str(z_co)
            print(data.encode("utf8"))
            sock.sendto(data.encode("utf8") , (UDP_IP, UDP_PORT))

        if(max(yellowArea, blueArea, greenArea, pinkArea, redArea, orangeArea) == greenArea):
            #print("green")
            data = "green," + str(x_co) + "," + str(y_co) + "," + str(z_co)
            print(data.encode("utf8"))
            sock.sendto(data.encode("utf8") , (UDP_IP, UDP_PORT))

        if(max(yellowArea, blueArea, greenArea, pinkArea, redArea, orangeArea) == pinkArea):
            #print("pink")
            data = "pink," + str(x_co) + "," + str(y_co) + "," + str(z_co)
            print(data.encode("utf8"))
            sock.sendto(data.encode("utf8") , (UDP_IP, UDP_PORT))

        if(max(yellowArea, blueArea, greenArea, pinkArea, redArea, orangeArea) == redArea):
            #print("red")
            data = "red," + str(x_co) + "," + str(y_co) + "," + str(z_co)
            print(data.encode("utf8"))
            file_handle.write(currentDT + ":" + data + "\n")
            sock.sendto(data.encode("utf8") , (UDP_IP, UDP_PORT))

        if(max(yellowArea, blueArea, greenArea, pinkArea, redArea, orangeArea) == orangeArea):
            #print("orange")
            data = "orange," + str(x_co) + "," + str(y_co) + "," + str(z_co)
            print(data.encode("utf8"))
            sock.sendto(data.encode("utf8") , (UDP_IP, UDP_PORT))

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.s=destoryAllWindows()
        break

            
    
