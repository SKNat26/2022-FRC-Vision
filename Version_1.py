import cv2 as cv
import numpy as np
import json

f = open("vision_data.json")
data = json.load(f)

#Image Path
img = cv.imread(r"C:\Users\laks\am-4600.jpg")

#Distance function
def getDistance(focal_length, real_width, width_in_frame):
    distance = (real_width * focal_length) / width_in_frame
    
    return distance
    
#Draw circle if contour is a circle
def isCircle(contour, color):
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
    
    (coord_x, coord_y), radius = cv.minEnclosingCircle(contour)
    center = (int(coord_x), int(coord_y))
    
    contour_area = cv.contourArea(contour) 
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = w/h
    
    if  1.0 >= contour_area / (radius**2 * 3.14) >= .8 and 1.1 >= aspect_ratio >= .8:
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

    lower_blue_1 = np.array([100,150,0])
    upper_blue_1 = np.array([140,255,255])
    mask_blue_1 = cv.inRange(hsv, lower_blue_1, upper_blue_1)

    lower_blue_2 = np.array([94, 80, 2])
    upper_blue_2 = np.array([120, 255, 255])
    mask_blue_2 = cv.inRange(hsv, lower_blue_2, upper_blue_2)

    mask_blue = mask_blue_1 + mask_blue_2
    
    return mask_blue
        

#Call functions 
for contour in getContours(img, createBlueMask(img)):
    isCircle(contour, "blue")
    
#show windows
cv.imshow("Detected Balls", img)
    
#break loop if key pressed
cv.waitKey(0)
  
cv.destroyAllWindows()
