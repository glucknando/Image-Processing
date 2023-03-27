import cv2
import cvzone
from FaceMeshModule import FaceMeshDetector #importuju svuj faceMesh detector, ne ten jejich ze cvzone (haze error)
from cvzone.HandTrackingModule import HandDetector
from cvzone.PlotModule import LivePlot

cap=cv2.VideoCapture(0)         #'FaceVideos/Video1.mp4'
detector=FaceMeshDetector(maxFaces=1)
detector2=HandDetector()    #kvuli funcki findDistance z handdetector
plotYL=LivePlot(640,180,[0,50],invert=True)      #arg_sirka,vyska ramecku, delka osy y
plotYR=LivePlot(640,180,[0,50],invert=True)

idList=[22,23,24,26,110,157,158,159,160,161,130,243,256,252,253,254,339,398,384,385,386,387,388,466,362,359]   #id cisla landmark kolem oci do 243 leve, pak prave
ratioListLeft=[]
ratioListRight=[]
blinkCounter=0
counter=0


color=(255,0,255)
while True:
    success,img=cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):         #if na to aby se video spustilo znovu jakmile skonci
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    img, faces=detector.findFaceMesh(img,draw=False)

    if faces:
        face=faces[0]
        for id in idList:
            cv2.circle(img,face[id],5,color,cv2.FILLED)
        #left eye
        leftUp=face[159]
        leftDown=face[23]
        leftLeft=face[130]
        leftRight=face[243]

        lengthVerL,_=detector2.findDistance(leftUp,leftDown)         #detekce vzdalenosti
        lengthHorL,_=detector2.findDistance(leftLeft,leftRight)

        cv2.line(img,leftUp,leftDown,(0,200,0),3)       #vykresleni vzdalenosti
        cv2.line(img,leftLeft,leftRight,(0,200,0),3)
        #print(int(100*(lengthVer/lengthHor)))   #pomer verticalni a horizontalni vzdalenosti tak aby se nam ta hodnota nemenila se vzdálenosti od kamery
        ratioL=100*(lengthVerL/lengthHorL)
        ratioListLeft.append(ratioL)
        if len(ratioListLeft)>4:
            ratioListLeft.pop(0)    #odstrani prvni hodnotu v listu jakmile dosahne v listu 4 hodnot (vzdy 4 hodnot bude)
        ratioAvgLeft=sum(ratioListLeft)/len(ratioListLeft)  #tak abychom meli prumer za vice hodnot (vice smooth to bude)

        #right eye
        rightUp=face[386]
        rightDown=face[253]
        rightLeft=face[362]
        rightRight=face[359]
        lengthVerR,_=detector2.findDistance(rightUp,rightDown)         #detekce vzdalenosti
        lengthHorR,_=detector2.findDistance(rightLeft,rightRight)
        cv2.line(img,rightUp,rightDown,(0,200,0),3)       #vykresleni vzdalenosti
        cv2.line(img,rightLeft,rightRight,(0,200,0),3)


        ratioR=100*(lengthVerR/lengthHorR)

        ratioListRight.append(ratioR)
        if len(ratioListRight)>4:
            ratioListRight.pop(0)    #odstrani prvni hodnotu v listu jakmile dosahne v listu 4 hodnot (vzdy 4 hodnot bude)
        ratioAvgRight=sum(ratioListRight)/len(ratioListRight)  #tak abychom meli prumer za vice hodnot (vice smooth to bude)

        if(ratioAvgLeft<25 or ratioAvgRight<29)and counter==0:
            blinkCounter+=1
            color=(0,255,0)
            counter=1
        if counter!=0:                      #zalezitos s counter je o tom aby to nepricitalo blikny kdyz je to pod hranici ale jen po jednou
            counter+=1
            if counter>15:
                counter=0
                color=(255,0,255)
        cvzone.putTextRect(img,f'Blink Count:{blinkCounter}',(50,80),scale=2,thickness=2,colorR=color)

        img=cv2.resize(img,(640,360))

        imgPlotL=plotYL.update(ratioAvgLeft)
        imgPlotR=plotYR.update(ratioAvgRight)
        imgStackedPlot=cvzone.stackImages([imgPlotR,imgPlotL],1,1)#stackne 2 img vedle sebe
        imgStacked=cvzone.stackImages([img,imgStackedPlot],2,1)
    else:
        img=cv2.resize(img,(640,360))                   #pokud by to nevidelo face
        imgStacked=cvzone.stackImages([img,img],2,1)
    #img=cv2.resize(img,(640,480))
    cv2.imshow("Image",imgStacked)
    cv2.waitKey(1)

