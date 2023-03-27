import cv2
import time
import mediapipe as mp
import FaceMeshModule as fm

#cap=cv2.VideoCapture("FaceVideos/Video1.mp4")
cap=cv2.VideoCapture(0)

pTime=0

detector=fm.FaceMeshDetector()
    
while True:
    success,img=cap.read()
    detector.findFaceMesh(img)
    
    
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(20,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)

    cv2.imshow("image",img)
    cv2.waitKey(1)
