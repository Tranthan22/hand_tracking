import cv2 as cv
import mediapipe as mp
import time
import numpy as np

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


current_time = 0
previous_time = 0
fps = 0

fingerid= [4,8,12,16,20]

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    results = hands.process(imgRGB)
    lmlistX = []
    lmlistY = []
    fingers = []
    lmList = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x * w), int(lm.y * h)
                
                lmlistX.append(cx)
                lmlistY.append(cy)
                lmList.append([id,cx,cy])
                if id == 8:
                    cv.circle(img, (cx,cy), 15, (255,0,255), cv.FILLED)
                    #print(cx, cy)
                #print(lmlist)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


            #analyze data here

            #thumb
            #if lmlistX[2-1] < lmlistX[4-1]:
            #    fingers.append(1)
            #else: 
            #    fingers.append(0)
            #index finger
            if lmList[fingerid[0]][1] < lmList[fingerid[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # viết cho 4 ngón dài
            for id in range(1,5):
                if lmList[fingerid[id]][2] < lmList[fingerid[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            print(fingers)
            songontay = fingers.count(1)
            print(songontay)
            cv.putText(img, str(int(songontay)), (30, 80), cv.FONT_HERSHEY_PLAIN, 3, (0,0,0), 3)
            

            

    current_time = time.time()
    fps = 1/ (current_time - previous_time)
    previous_time = current_time
    cv.putText(img, str("fps:" + str(int(fps))), (15, 15), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0), 3)
    
    #print(results.multi_hand_landmarks)

    cv.imshow("image", img)

    if cv.waitKey(5) == ord("a"):
        break


cap.release()
cv.destroyAllWindows()