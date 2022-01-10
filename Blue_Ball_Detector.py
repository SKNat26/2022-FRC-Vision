import cv2 as cv
import numpy as np

#accessing camera
camera = cv.VideoCapture(0)


#color detection
def isBlue(pixels):    
    if pixels > 0:
        return True
    else:
        return False

def isCircle(cnt):
    approx = cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), True)
    
    if len(approx) > 9:
        return True
    
    return False
    
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
            cv.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 2)

while True:
    ret, frame = camera.read()
    modify_frame = frame
    modify_frame = cv.GaussianBlur(modify_frame, (9, 9), None)
    modify_frame = cv.erode(modify_frame, None)
    modify_frame = cv.dilate(modify_frame, None)
    hsv = cv.cvtColor(modify_frame, cv.COLOR_BGR2HSV)
    
    #mask1 for blue
    lower1 = np.array([100,150,0])
    upper1 = np.array([140,255,255])
    mask1 = cv.inRange(hsv, lower1, upper1)
    
    #mask2 for blue 
    lower2 = np.array([94, 80, 2])
    upper2 = np.array([120, 255, 255])
    mask2 =  cv.inRange(hsv, lower2, upper2)
    
    #join 2 masks for blue
    mask_blue = mask1 + mask2
    cv.bitwise_and(modify_frame, modify_frame, mask=mask_blue)
    pixels_blue = np.sum(mask_blue)
        
    if isBlue(pixels_blue):    
        drawRect(mask_blue)
    
    cv.imshow("camera", frame)
    cv.imshow("mask", mask_blue)
    
    key = cv.waitKey(1)
    if key == 27:
        break

    


#quit processes
camera.release()
cv.destroyAllWindows()
