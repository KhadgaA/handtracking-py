import cv2
import time
import handtrackmodule as htm


wCam, hCam = 720, 720
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
ptime=0


detector = htm.handDetector(detectionCon=0.75)

htips=[4,8,12,16,20]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img=detector.findHands(img)
    lmlist= detector.findPosition(img)
    fcount = []
    if len(lmlist)!= 0 :

        if lmlist[htips[0]][1] < lmlist[htips[0]-1][1]:
            fcount.append(1)
        else:
            fcount.append(0)

        for i in range(1,5):
            if lmlist[htips[i]][2] < lmlist[htips[i]-2][2]:
                fcount.append(1)
            else:
                fcount.append(0)
        count = fcount.count(1)
        print(fcount)
        cv2.rectangle(img, (50,325), (150, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{str(count)}', (50, 430), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 5)



    ctime= time.time()
    fps= 1/(ctime-ptime)
    ptime = ctime

    cv2.putText(img, f'FPS:{int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,0,0), 1)

    cv2.imshow("Img", img)
    cv2.waitKey(2)

