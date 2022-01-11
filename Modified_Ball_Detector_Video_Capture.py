import cv2 as cv
import numpy as np

#accessing camera
camera = cv.VideoCapture(0)


def isCircle(cnt, contours):
    approx = cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), True)
    
    for contour in contours:
        (x, y), radius = cv.minEnclosingCircle(contour)
        center = (int(x),int(y))
        area_bounding_circle = (radius**2) * (22/7)
        area_contour = cv.contourArea(contour)
        if 20 >= area_bounding_circle - area_contour >= 0 and len(approx) >= 11:
            return True
            
    
    return False

def drawRect(mask, img, color):
    #color dictionary
    colors = {"red": (0, 0, 255), "blue": (255, 0, 0)}
    
    colored_box = colors[color]
    
    #Get contours on the mask
    contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) == 2:
        contours = contours[0]
        
    else:
        contours = contours[1]
        
    for contour in contours:
        if isCircle(contour, contours):
            x, y, w, h = cv.boundingRect(contour)
            aspect_ratio = w/h
            area = w * h
            if .8 <= aspect_ratio <= 1.1 and area > 1000:
                cv.rectangle(frame, (x, y), (x + w, y + h), colored_box, 2)
                cv.putText(img, color.upper() + " BALL", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, colored_box, 2)
    #Draw rectangle with specific color using aspect ratio and area tests
    
          

def editImage(img):
    #blur, erode, and dilate frame
    img = cv.GaussianBlur(img, (9, 9), None)
    img = cv.erode(img, None)
    img = cv.dilate(img, None)
    
    return img


def createBlueMask(img):
    global mask_blue
    #blue values 
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower_blue_1 = np.array([100,150,0])
    upper_blue_1 = np.array([140,255,255])
    mask_blue_1 = cv.inRange(hsv, lower_blue_1, upper_blue_1)
    
    lower_blue_2 = np.array([94,80,2])
    upper_blue_2 = np.array([120,255,255])
    mask_blue_2 = cv.inRange(hsv, lower_blue_2, upper_blue_2)
    
    mask_blue = mask_blue_1 + mask_blue_2
    
    
    return mask_blue

def createRedMask(img):
    global mask_red
    #red values
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    lower_red_1 = np.array([0, 100, 100])
    upper_red_1 = np.array([10, 255, 255])
    mask_red_1 = cv.inRange(hsv, lower_red_1, upper_red_1)

    lower_red_2 = np.array([160, 100, 100])
    upper_red_2 = np.array([179, 255, 255])
    mask_red_2 = cv.inRange(hsv, lower_red_2, upper_red_2)
    mask_red = mask_red_1 + mask_red_2 

    return mask_red

#infinite loop to process live feed
while True:
    ret, frame = camera.read()
    copy_frame = frame
    
    #call on functions
    drawRect(createRedMask(editImage(frame)), frame, "red")
    drawRect(createBlueMask(editImage(copy_frame)), frame, "blue")

    #show windows
    cv.imshow("blue mask", mask_blue)
    cv.imshow("red mask", mask_red)
    cv.imshow("frame", frame)
    
    #break loop if key pressed
    key = cv.waitKey(1)
    
    if key == 27:
        break

    
camera.release()
cv.destroyAllWindows()

