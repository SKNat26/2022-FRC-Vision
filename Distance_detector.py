import cv2 as cv
import numpy as np



def getDist(Focal_Length, real_face_width, face_width_in_frame):
    if face_width_in_frame > 0:
        distance = (real_face_width * Focal_Length)/face_width_in_frame
        return distance
    return 0        

