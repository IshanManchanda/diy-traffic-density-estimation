import numpy as np
import cv2 
cap=cv2.VideoCapture('/home/divyansh/Downloads/trafficvideo.mp4')
ret,frame1 =cap.read()

while cap.isOpened():
    
    ret,frame2 =cap.read()
    gray1=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    gray2=cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    diff=cv2.absdiff(frame1,frame2)
    imgray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(imgray,(5,5),0)
    ret, thres=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    kernel=np.ones((5,5),np.uint8)
    dilated=cv2.dilate(thres,kernel,iterations=1)
    polygons=np.array([
    [(980,240),(1300,240),(1570,1080),(60,1080)]   
    ])
    mask=np.zeros(frame1.shape[:2],dtype="uint8")
    cv2.fillPoly(mask,polygons,255)
    masked=cv2.bitwise_and(dilated,dilated,mask=mask)
    contours, hierarchy=cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for i,cntr in enumerate(contours):
        x,y,w,h=cv2.boundingRect(cntr)
        if((cv2.contourArea(cntr)<700)|((x<=650)|(x+w>=1500))|(y+h<=340)):
            continue
        cv2.rectangle(frame2,(x,y),(x+w,y+h),(0,0,255),2)
    
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',masked)
    cv2.namedWindow('vehicle', cv2.WINDOW_NORMAL)
    cv2.imshow('vehicle',frame2)
    if cv2.waitKey(40)==27:
        break
    
cv2.destroyAllWindows()
cap.release()    
