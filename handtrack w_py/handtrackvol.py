import cv2
import time
import numpy as np
import handtrackmodule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

############################
wCam, hCam = 720, 720
############################
#pycaw to control volume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
vol=volume.GetMasterVolumeLevel()
volRange= volume.GetVolumeRange()


volBar=400
minVol= volRange[0]
maxVol= volRange[1]

###########################################################
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
ptime=0

detector = htm.handDetector(detectionCon=0.75)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img=detector.findHands(img)

    lmlist= detector.findPosition(img)
    if len(lmlist) !=0:
        #print(lmlist[4])

        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1,y1),10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 2)
       # cv2.circle(img, (cx,cy), 10, (255, 0, 255), cv2.FILLED)
        length= math.hypot(x2-x1, y2-y1)
        #print(length)

        #our hand range is from 50-250 convert to -65 - 0

        vol = np.interp(length, [50,170],[minVol,maxVol])
        volBar = np.interp(length, [50, 170], [400, 200])
        volPer = np.interp(length, [50,170],[0,100])
        volSet = volume.SetMasterVolumeLevel(vol, None)
        #print(vol)

        dynColor= (0, np.interp(length,[50,170],[255,0]), np.interp(length,[50,170],[0,255]))   #dynamic Color
        cv2.circle(img, (cx, cy), 10, dynColor, cv2.FILLED)
        #changing the color of circl dynamically

        #showing the volume bar
        cv2.rectangle(img, (50,200), (85, 400), (0, 255, 0), 2)
        cv2.rectangle(img, (50,int(volBar)),(85,400), dynColor ,cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 0.7, dynColor, 1)
        #volume Percrentage
    ctime= time.time()
    fps= 1/(ctime-ptime)
    ptime = ctime

    cv2.putText(img, f'FPS:{int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,0,0), 1)

    cv2.imshow("Img", img)
    cv2.waitKey(2)