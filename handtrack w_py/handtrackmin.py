


import time

from cv2 import imshow, waitKey, FONT_HERSHEY_PLAIN, putText, cvtColor, COLOR_BGR2RGB, FILLED, circle, VideoCapture
import mediapipe as mp

cap = VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

ptime = 0
ctime = 0
while True:
    success, img = cap.read()
    imgRGB = cvtColor(img, COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id , cx, cy)
                if id==4:
                    circle(img, (cx, cy), 15, (255, 0, 255), FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)



    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    putText(img, str(int(fps)), (10, 70), FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)


    imshow("Image", img)
    waitKey(1)


