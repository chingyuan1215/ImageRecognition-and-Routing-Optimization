# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 23:27:37 2020

@author: user
"""
from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

import matplotlib.pyplot as plt
from skimage.transform import resize

import cv2 # importing cv2 liberary

cam = cv2.VideoCapture(0)
count = 0
file='C:/Users/7chia/Desktop/Image/'

while True:
     ret, img = cam.read()

     cv2.imshow("Test", img)

     if not ret:
        break

     k=cv2.waitKey(1)

     if k%256==27:
        #For Esc key
        print("Close")
        break
     elif k%256==32:
        #For Space key

        print("Image "+str(count)+"saved")
        file_path=file+str(count)+'.jpg'
        cv2.imwrite(file_path, img)
        count +=1
        
        
       
        cv2.imshow("Output",img)
        cv2.waitKey(1)


     #else:
       # count==1
        #break
       
cam.release
cv2.destroyAllWindows#鏡頭關步調



    

#preds=recognize_food(file_path,model)

#result = str(preds) 

