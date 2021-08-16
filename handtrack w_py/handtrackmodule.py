import time

import cv2
import mediapipe as mp


class handDetector():
    def __init__(self,mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon )
        self.mpDraw = mp.solutions.drawing_utils
        self.htips=[4,8,12,16,20]

    def findHands(self,img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
               if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw = False):
        self.lmlist= []
        if self.results.multi_hand_landmarks:
           myHand= self.results.multi_hand_landmarks[handNo]
           for id, lm in enumerate(myHand.landmark):
               # print(id,lm)
               h, w, c = img.shape
               cx, cy = int(lm.x * w), int(lm.y * h)
               self.lmlist.append([id,cx,cy])
               if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return  self.lmlist

    def fingersUp(self):
        fcount = []
        if  self.lmlist[ self.htips[0]][1] <  self.lmlist[ self.htips[0]-1][1]:
            fcount.append(1)
        else:
            fcount.append(0)

        for i in range(1,5):
            if  self.lmlist[ self.htips[i]][2] <  self.lmlist[ self.htips[i]-2][2]:
                fcount.append(1)
            else:
                fcount.append(0)
        return fcount




if __name__=="__main__":
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector= handDetector()

    while True:
        success, img = cap.read()
        img= detector.findHands(img)
        lmlist= detector.findPosition(img)
        if len(lmlist) !=0:
            print(lmlist[4])
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
