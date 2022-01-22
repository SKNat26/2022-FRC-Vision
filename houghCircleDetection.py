from tkinter import Frame
from turtle import circle
import cv2 as cv
from cv2 import dilate
from cv2 import MORPH_ERODE
from cv2 import bitwise_and
import numpy as np
import json

f = open("values.json")
data = json.load(f)

def findContours(bw):
    canny = cv.Canny(bw, 125,175)    
    contours, hierarchies = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return contours

def blue_mask(image, source):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    lower = np.array(data["bluehsv"]["lower"])
    upper = np.array(data["bluehsv"]["upper"])
    mask = cv.inRange(hsv, lower, upper)
    final = cv.bitwise_and(frame, frame, mask=mask)
    return final

def red_mask(image, source):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    lower = np.array(data["redhsv"]["lower"])
    upper = np.array(data["redhsv"]["upper"])
    mask = cv.inRange(hsv, lower,upper)
    final = cv.bitwise_and(frame, frame, mask=mask)
    return final

def findCircles(image, src):
    circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT,dp=dp,minDist=mindist,param1=param1,param2=param2,minRadius=minRad,maxRadius=maxRad)

    if np.any(circles) != None:
        print("circle found")
        circles = np.uint16(np.around(circles))
        # Draw the circles
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(src, center, 1, (136,100,90), 3)
            # circle outline
            radius = i[2]
            cv.circle(src, center, radius, (136,100,90), 3)
    return image


def testing(x):
    pass

cv.namedWindow("Testing")
cv.createTrackbar("dp", "Testing", 1, 100 , testing)
cv.createTrackbar("mindist", "Testing", 1, 100, testing)
cv.createTrackbar("param1", "Testing", 1, 200, testing)
cv.createTrackbar("param2", "Testing", 1, 200, testing)
cv.createTrackbar("minRad", "Testing", 1, 100, testing)
cv.createTrackbar("maxRad", "Testing", 1,100 , testing)

cap = cv.VideoCapture(0, cv.CAP_DSHOW) 

while(True):
    isTrue,frame = cap.read()

    dp = cv.getTrackbarPos("dp","Testing")
    mindist = cv.getTrackbarPos("mindist","Testing")
    param1 = cv.getTrackbarPos("param1","Testing")
    param2 = cv.getTrackbarPos("param2","Testing")
    minRad = cv.getTrackbarPos("minRad","Testing")
    maxRad = cv.getTrackbarPos("maxRad","Testing")

    blur = cv.GaussianBlur(frame, (7,7), cv.BORDER_DEFAULT)

    frameblue = blue_mask(blur,blur)
    framered = red_mask(blur,blur)
    
    contoursblue = findContours(frameblue)
    contoursred = findContours(framered)

    blank_imageblue = np.zeros(frame.shape, dtype='uint8')
    blank_imagered = np.zeros(frame.shape, dtype = 'uint8')

    cv.drawContours(blank_imageblue, contoursblue, -1, (255,0,0), 2)
    cv.drawContours(blank_imagered, contoursred, -1, (0,0,255), 2)

    blank_imageblue_gray = cv.cvtColor(blank_imageblue, cv.COLOR_BGR2GRAY) 
    blank_imagered_gray = cv.cvtColor(blank_imagered, cv.COLOR_BGR2GRAY)
    
    blank_imageblue_gray_blur = cv.GaussianBlur(blank_imageblue_gray, (5,5), cv.BORDER_DEFAULT)
    blank_imagered_gray_blur = cv.GaussianBlur(blank_imagered_gray, (5,5), cv.BORDER_DEFAULT)
    
    dilateblue = cv.dilate(blank_imageblue_gray_blur, (7,7), iterations = 3)
    dilatered = cv.dilate(blank_imagered_gray_blur, (7,7), iterations = 3)
    #morphblue = cv.morphologyEx(blank_imageblue_gray, cv.MORPH_CLOSE, (17,17))
    #morphred =  cv.morphologyEx(blank_imagered_gray, cv.MORPH_CLOSE, (17,17))

    circleblue = findCircles(dilateblue, frame)
    circlered = findCircles(dilatered, frame)
    
    cv.imshow('circleblue', circleblue)
    cv.imshow('circlered', circlered)
    cv.imshow('original', frame)
    if cv.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv.destroyAllWindows()
