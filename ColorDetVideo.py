# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 10:43:15 2022

@author: VAMSHI KRISHNA
"""

import pandas as pd
import cv2
import imutils
import numpy as np
import pyttsx3
engine = pyttsx3.init()

camera = cv2.VideoCapture(0)
# address = "https://192.168.0.11:8080/video"
# camera.open(address)

r = g = b = xpos = ypos = 0
clicked = False

index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv('colors.csv', names = index, header = None)

def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, "color_name"]
    # engine.say(cname)
    # engine.runAndWait()
    return cname


def identify_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
    	global b, g, r, xpos, ypos, clicked
    	xpos = x
    	ypos = y
    	b, g, r = frame[y,x]
    	b = int(b)
    	g = int(g)
    	r = int(r)


cv2.namedWindow('Open CV Color Detection')
cv2.setMouseCallback('Open CV Color Detection', identify_color)

while True:
    (grabbed, frame) = camera.read()
    frame = imutils.resize(frame, width=750)
    kernal = np.ones((5, 5), "uint8")
    
    cv2.rectangle(frame, (20,20), (600, 70),(b,g,r), -1)
    color = get_color_name(r,g,b)
    text = color + '   R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
    cv2.putText(frame,text, (50,50),2, 0.8, (255,255,255),2,cv2.LINE_AA)
    
    
    if(r+g+b >= 600):
        cv2.putText(frame,text,(50,50), 2, 0.8, (0,0,0),2,cv2.LINE_AA)   
        
    cv2.imshow('Open CV Color Detection',frame)
    
    if cv2.waitKey(20) & 0xFF == 27:
        break
    
camera.release()
cv2.destroyAllWindows()