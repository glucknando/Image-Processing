import cv2
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume    #pycaw library na ovladani zvuku v pocitaci
wCam,hCam=640,480


cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
vol=0
volBar=400
volPer=0
detector=HandDetector(detectionCon=0.8,maxHands=1)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()         #da nam kolik je rozsha volume (hodnoty)
#volume.SetMasterVolumeLevel(-15, None)       #nastavy velikost volume
minVol=volRange[0]
maxVol=volRange[1]
area=0
colorVol=(255,0,0)

while True:
    success,img=cap.read()
    #find hand
    hands,img=detector.findHands(img)

    if hands:
        hand1=hands[0]
        lmList1=hand1["lmList"]
        #filter based on size
        bbox1=hand1["bbox"]
        area=(bbox1[2]*bbox1[1])//100 #bo 3 a 4 hodnota bbox je sirka a vyska
        if 130<area<350:
            #print("yes")
        #find distance between index and thumb
            length, info, img=detector.findDistance(lmList1[4][:2],lmList1[8][:2], img)
            print(length)
        #Convert Volume

            volBar=np.interp(length,[25,160],[400,150])     #dava do meritka volumebar (hodnoty zvoleny)
            volPer=np.interp(length,[25,160],[0,100])
         #reduce resolution to make it smoother
            smoothness=5         #increment jaky to bude davat
            volPer=smoothness*round(volPer/smoothness)

        #checks fingers up
            fingers1=detector.fingersUp(hand1)

        #if piky is down set volume
            if not fingers1[4]:         #if fingers[4]==False
                volume.SetMasterVolumeLevelScalar(volPer/100,None) #misto log to normal, mame obe stupnice normal
                cv2.circle(img,(info[4],info[5]),15,(0,255,0),cv2.FILLED)
                colorVol=(0,255,0)

            else:
                colorVol=(255,0,0)
    #drawings

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'{int(volPer)}%',(40,120),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    #zmeni napis kdyz je volume set, abys vedel kdyz jsi to setnul
    cVol=int(volume.GetMasterVolumeLevelScalar()*100)
    cv2.putText(img,f'Vol set:{int(cVol)}',(350,50),cv2.FONT_HERSHEY_PLAIN,3,colorVol,3)

 #frame rate
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'FPS:{int(fps)}',(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("Img",img)
    cv2.waitKey(1)
