import cv2
from cvzone.HandTrackingModule import HandDetector

print(eval("2**3"))
#trida button
class Button:
    def __init__(self,pos,width,height,value):
        self.pos=pos        #pro tuto instanci do promene pos dej to co ti zada user
        self.width=width       #inicilaizace
        self.value=value
        self.height=height

    def draw(self,img):
        cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(225,225,225),cv2.FILLED)
        cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
        cv2.putText(img,self.value,(self.pos[0]+40,self.pos[1]+60),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50),2)

    def checkClick(self,x,y):
        if self.pos[0]<x<self.pos[0]+self.width:
            if self.pos[1]<y<self.pos[1]+self.height:
                cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(250,250,250),cv2.FILLED)
                cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
                cv2.putText(img,self.value,(self.pos[0]+25,self.pos[1]+80),cv2.FONT_HERSHEY_PLAIN,5,(0,0,0),5)
                return True
        else:
            return False

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=HandDetector(detectionCon=0.8,maxHands=1)

#creating button
buttonListValues=[['7','8','9','*'],
                  ['4','5','6','-'],
                  ['1','2','3','+'],
                  ['0','/','.','='],
                  ['c','(',')','**']]
#print(buttonListValues[4][2])

buttonList=[]
for x in range(4):
    for y in range(5):
        xpos=x*80+800
        ypos=y*80+100
        buttonList.append(Button((xpos,ypos),80,80,buttonListValues[y][x]))

#variables
myEquation=''
delayCounter=0

#loop
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    #Hand detection
    hands,img=detector.findHands(img,flipType=False)

    #draw all buttons
    cv2.rectangle(img,(800,20),(800+320,50+100),(225,225,225),cv2.FILLED)
    cv2.rectangle(img,(800,20),(800+320,50+100),(50,50,50),3)
    for button in buttonList:
        button.draw(img)


    #check for hand
    if hands:
        lmList=hands[0]['lmList']
        length,_,img=detector.findDistance(lmList[8],lmList[12],img)
        #print(length)
        x,y=lmList[8]
        if length<50:
            for i,button in enumerate(buttonList):

                if button.checkClick(x,y) and delayCounter==0:
                    myValue=buttonListValues[int(i%5)][i//5] #exact value which is used

                    if myValue=="=":
                        myEquation=str(eval(myEquation))
                    elif myValue=='c':
                        myEquation=''
                    else:
                        myEquation+=myValue
                    delayCounter=1

    print(delayCounter)#To avoid duplicate
    if delayCounter!=0:
        delayCounter+=1
        if delayCounter>20:
            delayCounter=0


    #display results/equation
    cv2.putText(img,myEquation,(810,70),cv2.FONT_HERSHEY_PLAIN,3,(50,50,50),3)


    #display image
    cv2.imshow("Image",img)
    key=cv2.waitKey(1)
    #clear calculation
    if key==ord('c'):
        myEquation=''
