# Written with help from Andreas Baum

import numpy as np
import cv2
#from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=50,detectShadows=True)

white1 = []
white2 = []
for a in range(300):
    ret, frame = cap.read()
    
    fgmask = fgbg.apply(frame)
    
    cv2.imshow('frame',fgmask)
    if (fgmask[320:380, 400] > 1).any():        #could also be .all()
        white1.append(True)
    else:
        white1.append(False)
    if (fgmask[0:10,12] > 1).any():        #could also be .all()
        white2.append(True)
    else:
        white2.append(False)
        
white1 = np.array(white1)   # to convert list into numpy array
white2 = np.array(white2)   # to convert list into numpy array

cap.release()
cv2.destroyAllWindows()
