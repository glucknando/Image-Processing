import cv2
import cvzone
from FaceMeshModule import FaceMeshDetector
#základ je faceDistance file, kdyby bylo neco nejasne
import numpy as np

cap=cv2.VideoCapture(0)
detector=FaceMeshDetector(maxFaces=1)

textList=["Welcome to" ,"David apartment.",
          "Here we will","study process","engineering",
          "if you love ","your life run ","fucking run","bitch"]
sen=20   #higher number is less sensitivity
while True:
    success,img=cap.read()
    imgText=np.zeros_like(img) #zrobí cerne pozadí
    img,faces=detector.findFaceMesh(img,draw=False)

    if faces:
        face=faces[0]
        pointLeft=face[145]
        pointRight=face[374]
        w,_=detector.findDistance(pointLeft,pointRight)
        W=6.3
        f=770
        d=(W*f)/w
        #print(d)
        cvzone.putTextRect(img,f'Depth:{int(d)}cm',(face[10][0]-85,face[10][1]-40),scale=2)

        for i,text in enumerate(textList):       #psani textu do cerneho pozadí/ramecku a zarizeni zvetsovani a zemnosvani
            singleHeight=20+int(int(d/sen)*sen/4)
            scale=0.4+(int(d/sen)*sen)/80
            cv2.putText(imgText,text,(50,50+(i*singleHeight)),cv2.FONT_ITALIC,scale,(250,250,250),2)

    imgStacked=cvzone.stackImages([img,imgText],2,1)
    cv2.imshow("Image",imgStacked)
    cv2.waitKey(1)
