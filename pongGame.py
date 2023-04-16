import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

#importing all images

imgBackground=cv2.imread("PongResources/Background.png")
imgGameOver=cv2.imread("PongResources/gameOver.png")
imgBall=cv2.imread("PongResources/Ball.png",cv2.IMREAD_UNCHANGED)   #give parameter which sayes to do not channe in the imag nic
imgBat1=cv2.imread("PongResources/bat1.png",cv2.IMREAD_UNCHANGED)
imgBat2=cv2.imread("PongResources/bat2.png",cv2.IMREAD_UNCHANGED)

#hand detector
detector=HandDetector(detectionCon=0.8,maxHands=2)

#variables
ballPos=[100,100]
speedX=15
speedY=15
gameOver=False
score=[0,0]
#speedChange=0
while True:
    _,img=cap.read()

    img=cv2.flip(img,1)
    imgRaw=img.copy()#flip obraz aby to bylo zrcadlove
    hands, img = detector.findHands(img,flipType=False)
    #overlaying the backgorund on camera
    img=cv2.addWeighted(img,0.2,imgBackground,0.8,0) #druha a ctvrta hodnota musi byt doplnek

    #check for hands
    if hands:
        for hand in hands:
            x,y,w,h=hand['bbox']
            h1,w1,_=imgBat1.shape
            y1=y-h1//2
            y1=np.clip(y1,20,415)       #omezi hodnoty takze kdyz se donstanes mimo interval tak to zustane ta hodnoda na hranici intervalu
            if hand['type']=="Left":
                img=cvzone.overlayPNG(img,imgBat1,(59,y1))
                if 59<ballPos[0]<59+w1 and y1<ballPos[1]<y1+h1:
                    speedX=-speedX
                    ballPos[0]+=30  #odstrani bouncing
                    score[0]+=1
                    # if score[0]%2==0: #na zvyseni obtiznosti po urcite dobe, ale od urcite rychlosti to haze error kvuli overlayPNG line84
                    #     speedX+=int(5 * math.copysign(1, speedX))
                    #     speedY+=int(5 * math.copysign(1, speedY))
                    #

            if hand['type']=="Right":
                img=cvzone.overlayPNG(img,imgBat2,(1195,y1))
                if 1195-50<ballPos[0]<1195 and y1<ballPos[1]<y1+h1:
                    speedX=-speedX
                    ballPos[0]-=30
                    score[1]+=1
                    # if score[1]%2==0:
                    #     speedX+=int(5 * math.copysign(1, speedX))
                    #     speedY+=int(5 * math.copysign(1, speedY))


    #check game over
    if ballPos[0]<40 or ballPos[0]>1200:
        gameOver=True

    if gameOver:
        img=imgGameOver
        cv2.putText(img,str(score[1]+score[0]).zfill(2),(585,360),cv2.FONT_HERSHEY_COMPLEX,2.5,(200,0,200),5)
    #if game not over move the ball
    else:
        #move the ball
        if ballPos[1]>=500 or ballPos[1]<=10:
            speedY=-speedY  #change the ball direction v y ose kdyz narazi na hranici

        ballPos[0]+=speedX
        ballPos[1]+=speedY

         #draw the ball
        img=cvzone.overlayPNG(img,imgBall,ballPos)

        cv2.putText(img,str(score[0]),(300,650),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),5)
        cv2.putText(img,str(score[1]),(900,650),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),5)


    img[580:700,20:233]=cv2.resize(imgRaw,(213,120))

    cv2.imshow("Image",img)
    key= cv2.waitKey(1)
    if key==ord('r'):
        ballPos=[100,100]
        speedX=15
        speedY=15
        gameOver=False
        score=[0,0]
        imgGameOver=cv2.imread("PongResources/gameOver.png")
