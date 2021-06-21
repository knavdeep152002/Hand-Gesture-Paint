import cv2
import handtrackingmodule as htm
import time
import numpy as np
import math
import random

cam = cv2.VideoCapture(0)
detector = htm.Handdetector(detectionconf=0.75)
paint = np.zeros((int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)) ,int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)) ),np.uint8)
paint = cv2.cvtColor(paint,cv2.COLOR_BGR2RGB)

while(cam.isOpened()):
    _,img = cam.read()
    img = cv2.flip(img,1)
    
    img = detector.findhands(img)
    lmlist = detector.findposition(img,draw=False)
    c = 0
    for i in range(8,21,4):
        try:
            if lmlist[i][2]<lmlist[i-1][2] or lmlist[i][2]<lmlist[i-2][2]:
                c+=1
        except:
            pass
    try:
        if lmlist[4][1] < lmlist[3][1]:
            c+=1
        if c==1:
            # cv2.putText(paint,f"({lmlist[4][2]},{lmlist[8][1]})",(50,50),cv2.FONT_HERSHEY_TRIPLEX,2,(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),2)
            # cv2.rectangle(paint,(50,50),(100,100),((0,255,0)),-1)
            cv2.circle(paint,(lmlist[8][1],lmlist[8][2]),10,(255,0,255),-1)
        if c==3:
            cv2.circle(paint,(lmlist[8][1],lmlist[8][2]),20,(0,0,0),-1)
    except:
        pass
    cv2.putText(img,f"fingesr = {c}",(10,70),cv2.FONT_ITALIC,2,(0,0,0),2) 
    # img = cv2.addWeighted(img,0.5,paint,0.5,0)
    imgray = cv2.cvtColor(paint,cv2.COLOR_RGB2GRAY)
    _,imginv = cv2.threshold(imgray,50,255,cv2.THRESH_BINARY_INV)
    imginv = cv2.cvtColor(imginv,cv2.COLOR_GRAY2RGB)
    img = cv2.bitwise_and(img,imginv)
    img = cv2.bitwise_or(img,paint)
    cv2.imshow('w',img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
# print(m1,m2)

cam.release()
cv2.destroyAllWindows()