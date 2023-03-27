import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random
#cvzone 1.5.3 je good na 0.8 a zaroven to dava cisla s tracking jaky chuc
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector=HandDetector(detectionCon=0.7,maxHands=1)

timer=0
stateResults=False
startGame=False
scores=[0,0] #[AI,player]
imgAI=None

while True:
    imgBG=cv2.imread("Resources/RPS/BG.png")    #davame dovnitr cyklu protoze budeme chtit menit pokazde ikonu u AI
    success,img=cap.read()

    #potreba scaled it down to 420 vyska a pak crop it to 400 sirka
    imgScaled=cv2.resize(img,(0,0),None,0.875,0.875)        #420/480=0.875 to je nas resize koef.
    imgScaled=imgScaled[:,80:480]                                 #680*0,875-400=160    160/2=80, croply jsem to aby to bylo vycentrovane


    #Find hands
    hands,img=detector.findHands(imgScaled)

    imgBG[234:654,795:1195]=imgScaled            #[hegiht,width] tohle narve (overlay) do imgBG imgScaled (nase webka)

    #Find hands
    hands,img=detector.findHands(imgScaled)

    if startGame:           #if stratgem je true check to co bude v ifu
        if stateResults is False:
            timer=time.time()-intialTime
            cv2.putText(imgBG,str(int(timer)),(605,435),cv2.FONT_HERSHEY_PLAIN,6,(255,0,255),4)

            if timer>3:     #jakmile dosahnem nad 3s pak to prestane ukazovat čas
                stateResults=True
                timer=0
                if hands:
                    playermove=None
                    hand=hands[0]
                    fingers=detector.fingersUp(hand)
                    print(fingers)
                    if fingers==[0,0,0,0,0]or fingers==[1,0,0,0,0]:       #pridal jsem i palec hore bo to spatne bere #podminky na rock paper scisciors a zapsani do promene playermove
                        playermove=1                #cast pro hrace
                    if fingers==[1,1,1,1,1]:
                        playermove=2
                    if fingers==[0,1,1,0,0]:
                        playermove=3

                    randomNumber=random.randint(1,3)
                    imgAI=cv2.imread(f'Resources/RPS/{randomNumber}.png',cv2.IMREAD_UNCHANGED)    #unchanged kvuli overlay funkci jinak se prepise to png
                    imgBG=cvzone.overlayPNG(imgBG,imgAI,(149,310))      #funkce backgroun, front, pozice

                    #rozhodnuti kdo vyhral
                    #player wins
                    if (playermove==1 and randomNumber==3) or (playermove==2 and randomNumber==1) or (playermove==3 and randomNumber==2):
                        scores[1]+=1
                    #AI wins
                    if (playermove==3 and randomNumber==1) or (playermove==1 and randomNumber==2) or (playermove==2 and randomNumber==3):
                        scores[0]+=1

                    print(playermove)


    if stateResults:
        imgBG=cvzone.overlayPNG(imgBG,imgAI,(149,310))  #hodime to mimo if do hlavniho loop aby nam to tam zustalo


    cv2.putText(imgBG,str(scores[0]),(410,215),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)        #tisk skore do obrazku
    cv2.putText(imgBG,str(scores[1]),(1112,215),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)
    #cv2.imshow("Img",img)
    cv2.imshow("BG",imgBG)
    #cv2.imshow("Scaled",imgScaled)
    key=cv2.waitKey(1)
    if key==ord('s'):       #startgame true kdyz zmacknu s
        startGame=True
        intialTime=time.time()  #zpusti intial timer
        stateResults=False
