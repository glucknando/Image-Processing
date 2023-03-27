import cv2
import mediapipe as mp
import time



class poseDetector():
    def __init__(self,mode=False,complexity=1,smoothlm=True, enable=False, smoothsg=True, detectionCon=0.5,trackCon=0.5):
        #static_image_mode=False,
        #model_complexity=1,
        #smooth_landmarks=True,
        #enable_segmentation=False,
        #smooth_segmentation=True,
        #min_detection_confidence=0.5,
        #min_tracking_confidence=0.5):
        self.mode=mode                  #self dela ze to vytvari promenou v ramci te tridy (nejak tak
        self.complexity=complexity
        self.smoothlm=smoothlm
        self.enable=enable
        self.smoothsg=smoothsg
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpPose=mp.solutions.pose
        self.mpDraw=mp.solutions.drawing_utils
        self.pose=self.mpPose.Pose(self.mode,self.complexity,self.smoothlm,self.enable,
                                   self.smoothsg, self.detectionCon,self.trackCon)

    def findPose(self,img,draw=True):

        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #predelani z brg to rgb
        self.results=self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)   #kresli landmarks (cervene body, conection mezi nema)
        return img
    def findPosition(self,img,draw=True):
        lmList=[]
        if self.results.pose_landmarks:

            for id,lm in enumerate(self.results.pose_landmarks.landmark):    #priradi nam cisla k nasim landmarks
                h,w,c=img.shape
                #print(id,lm)
                cx,cy=int(lm.x*w), int(lm.y*h)  #prepocita hodnotu x, y na pixely
                lmList.append([id,cx,cy])   #do lmlist pridavame id,cx,cy
                if draw:
                    cv2.circle(img, (cx,cy),5,(255,0,0), cv2.FILLED)
        return lmList




def main():
    cap=cv2.VideoCapture('PoseVideos/3.mp4')
    pTime=0
    detector=poseDetector()
    while True:
        success,img =cap.read()
        detector.findPose(img)
        lmList=detector.findPosition(img,draw=False)
        if len(lmList)!=0:

            print(lmList)
            #print(lmList[14])
            #cv2.circle(img, (lmList[14][1],lmList[14][2]),15,(255,0,0), cv2.FILLED)    #tracking jednoho bodu (elbow)
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)


        cv2.imshow("Image",img)
        cv2.waitKey(1)


if __name__=="__main__":        #neco s volanim main funkce
    main()
