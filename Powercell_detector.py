import cv2 as cv
import numpy as np

#accessing camera
camera = cv.VideoCapture(0)


#color detection
def isYellow(pixels):    
    if pixels > 0:
        return True
    else:
        return False
    
def isCircle(cnt):
    approx = cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), True)
    
    if len(approx) > 12:
        return True
    
    return False;
    
def drawRect(mask):
    contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) == 2:
        contours = contours[0]
        
    else:
        contours = contours[1]
        
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        aspect_ratio = w/h
        area = w * h
        if .8 <= aspect_ratio <= 1.1 and area > 1000 and isCircle(contour):
            cv.rectangle(frame, (x, y), (x + w, y + h), (36,255,12), 2)

while True:
    ret, frame = camera.read()
    modify_frame = frame
    modify_frame = cv.GaussianBlur(modify_frame, (9, 9), None)
    modify_frame = cv.erode(modify_frame, None)
    modify_frame = cv.dilate(modify_frame, None)
    hsv = cv.cvtColor(modify_frame, cv.COLOR_BGR2HSV)
    lower = np.array([100,150,0])
    upper = np.array([140,255,255])
    mask = cv.inRange(hsv, lower, upper)
    cv2.bitwise_and(modify_frame, modify_frame, mask=mask)
    pixels = np.sum(mask)
    
    if isYellow(pixels):    
        drawRect(mask)
        
    
    
    
    
    
    cv.imshow("camera", frame)
    cv.imshow("mask", mask)
    if cv.waitKey(1) and 0xFF == ord('q'):
        break

    


#quit processes
camera.release()
cv.destroyAllWindows()
