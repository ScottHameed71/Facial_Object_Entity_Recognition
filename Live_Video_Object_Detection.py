import face_recognition    #face recognition library using dlib' recognition system
import cv2    #The cv2 version of the OpenCV library whiich includes the NumPy support
import numpy as np    #Library for advancced n-dimensional array object and related math functions
import mysql.connector    #Python native MySQL connector
import cvlib as cv
from cvlib.object_detection import draw_bbox
import sys

video_capture = cv2.VideoCapture(0) #intiates the first webcam for video capture
process_this_frame = True

while True:
   ret, frame = video_capture.read()    #read the video frame


   if process_this_frame:     #converting the frame size and then determining the location & encoding values
       small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # reduces the size to 25% of the original
       rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)  # code added to create compatibility for Mac

       # rgb_small_frame = small_frame[:, :, ::-1] #code previously in the Ubuntu sysem and worked perfectly but has been replaced with line immediately above for Mac compatbility



       bbox, label, conf = cv.detect_common_objects(rgb_small_frame)  #OBJECT
       varshow = draw_bbox(rgb_small_frame, bbox, label, conf) #OBJECT


   cv2.imshow('Video', varshow)



   if cv2.waitKey(1) & 0xFF == ord('q'):
       break


video_capture.release()
cv2.destroyAllWindows()