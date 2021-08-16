import cv2
import numpy as np
import handtrackmodule as htm
import time
import os

folderpath = "header images"
myList = os.listdir(folderpath)
overlayList=[]
for imPath in myList:
    image = cv2.imread(f'{folderpath}/{imPath}')
    overlayList.append(image)
header = overlayList[0]
#################################
drawcolor= (0,255,0)
brushSize = 15
eraserSize = 25
hcam,wcam = 1280,720

imgCanvas = np.zeros((720,1280,3), np.uint8)
################################

cap = cv2.VideoCapture(0)
cap.set(3,hcam)
cap.set(4,wcam)

detector = htm.handDetector(detectionCon=0.85)
xp,yp= 0, 0
while True:

    #import image
    success, img = cap.read()
    img= cv2.flip(img,1)
    #find Hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        #print(lmList)
        # tip of index finger
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

    #check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        #Selection mode- Two fingers up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            cv2.rectangle(img, (x1, y1-25), (x2, y2+25), drawcolor, cv2.FILLED)
            #print("Selection Mode")
            #checking wich part of header is selected
            if y1<125:
                if 0<x1<210:
                    header = overlayList[0]
                    drawcolor = (0, 255, 0)
                elif 210<x1<420:
                    header = overlayList[1]
                    drawcolor = (0, 0, 255)
                elif 420<x1<640:
                    header = overlayList[2]
                    drawcolor = (255,191 , 0)
                elif 640<x1<870:
                    header = overlayList[3]
                    drawcolor = (80,127,255)
                elif 870<x1<1280:
                    header = overlayList[4]
                    drawcolor = (0, 0, 0)
        # drawing mode - index finger only up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1, y1 ), 20, drawcolor, cv2.FILLED)
            if xp==0 and yp ==0:
                xp,yp=x1,y1
            if drawcolor == (0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawcolor, eraserSize)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawcolor, eraserSize)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawcolor, brushSize)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawcolor, brushSize)
               # print("Drawing Mode")
            xp, yp = x1, y1

    #adding both the images of drawing and webcam
    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img= cv2.bitwise_or(img,imgCanvas)


    #setting the header image
    img[0:125, 0:1280] = header
    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image",img)
    #cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)