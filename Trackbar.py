import cv2 as cv
import numpy as np

#create trackbar
#process image
image = cv.imread(input("Enter image file"))
LENGTH, WIDTH = 640, 480
resized_image = cv.resize(image, (LENGTH, WIDTH))

#blur, dilate, erode
resized_image = cv.GaussianBlur(resized_image, (7, 7), 0)
resized_image = cv.erode(resized_image, None)
resized_image = cv.dilate(resized_image, None)



def testing(x):
    pass

cv.namedWindow("Testing")
cv.createTrackbar("Hue Low", "Testing", 0, 255, testing)
cv.createTrackbar("Hue High", "Testing", 255, 255, testing)
cv.createTrackbar("Sat Low", "Testing", 0, 255, testing)
cv.createTrackbar("Sat High", "Testing", 255, 255, testing)
cv.createTrackbar("Val Low", "Testing", 0, 255, testing)
cv.createTrackbar("Val High", "Testing", 255, 255, testing)
    
while True:
    hsv = cv.cvtColor(resized_image, cv.COLOR_BGR2HSV)
    
    hue_low = cv.getTrackbarPos("Hue Low", "Testing")
    saturation_low = cv.getTrackbarPos("Sat Low", "Testing")
    value_low = cv.getTrackbarPos("Val Low", "Testing")
    
    hue_high = cv.getTrackbarPos("Hue High", "Testing")
    saturation_high = cv.getTrackbarPos("Sat High", "Testing")
    value_high = cv.getTrackbarPos("Val High", "Testing")
    
    lower = np.array([hue_low, saturation_low, value_low])
    upper = np.array([hue_high, saturation_high, value_high])

    mask = cv.inRange(hsv, lower, upper)
    mask_in_action = cv.bitwise_and(resized_image, resized_image, mask = mask)
    #display image

    cv.imshow("resized image", resized_image)
    cv.imshow("masking", mask_in_action)
    
    key = cv.waitKey(1)
    if key == 27:
        break
    
cv.destroyAllWindows()  

    
