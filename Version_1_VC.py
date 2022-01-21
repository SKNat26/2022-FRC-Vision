import cv2 as cv
import numpy as np
import json

f = open("vision_data.json")
data = json.load(f)

#Image Path
camera = cv.VideoCapture(0)

#Distance function
def getDistance(focal_length, real_width, width_in_frame):
    distance = (real_width * focal_length) / width_in_frame
    
    return distance
    
#Draw circle if contour is a circle
def isCircle(img, contour, color):
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
    
    (coord_x, coord_y), radius = cv.minEnclosingCircle(contour)
    center = (int(coord_x), int(coord_y))
    
    contour_area = cv.contourArea(contour) 
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = w/h
    
    if  1.0 >= contour_area / (radius**2 * 3.14) >= .7 and 1.1 >= aspect_ratio >= .8 and contour_area > 1000:
        distance = getDistance(390, 24, int(w))
        distance = int(distance)    
        cv.circle(img, center, int(radius), (0, 255, 0), 5)
        cv.putText(img, color.upper() + " BALL " + str(distance) + " CM", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return True
    
    return False
    
def getContours(img, mask):
    global contours
    contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) == 2:
        contours = contours[0]
        
    else:
        contours = contours[1]
    
    return contours 
    
    

def createBlueMask(img):
    global mask_blue
    #blue values 
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower_blue = np.array(data["hsv_blue"]["lower"])
    upper_blue = np.array(data["hsv_blue"]["upper"])
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    
    return mask_blue
        

#Call functions and process feed
while True:
    ret, frame = camera.read()
    
    for contour in getContours(frame, createBlueMask(frame)):
        isCircle(frame, contour, "blue")
    
        #show windows
    cv.imshow("mask blue", mask_blue)
    cv.imshow("Detected Balls", frame)
    
        #break loop if key pressed
    key = cv.waitKey(1)
    if key == 27:
        break
       
  
camera.release()  
cv.destroyAllWindows()
