import time
 
from neopixel import *
import numpy as np
import cv2
import argparse
import signal
import sys
import random
def signal_handler(signal, frame):
        sys.exit(0)
 
def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true', help='clear the display on exit')
        args = parser.parse_args()
        if args.c:
                signal.signal(signal.SIGINT, signal_handler)
                
# LED strip configuration:
LED_1_COUNT      = 180      # Number of LED pixels.
LED_1_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_1_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_1_INVERT     = True   # True to invert the signal (when using NPN transistor level shift) 3.3 V to 5 V
LED_1_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_1_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

LED_2_COUNT      = 180      # Number of LED pixels.
LED_2_PIN        = 13      # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA        = 11      # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_2_INVERT     = True   # True to invert the signal (when using NPN transistor level shift) 3.3 V to 5 V
LED_2_CHANNEL    = 1       # 0 or 1
LED_2_STRIP      = ws.WS2811_STRIP_GRB

cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=10,varThreshold=100,detectShadows=False)

#def singlePix(i, color):
#    strip.setPixelColor(i,  color)
#    strip.show()
#    time.sleep(1/1000.0) 
    
if __name__ == '__main__':
        opt_parse()
	strip1 = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL, LED_1_STRIP)
	strip2 = Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL, LED_2_STRIP)
	
	strip1.begin()
	strip2.begin()
	print ('Press Ctrl-C to quit.')
	
while True: 
    ret, frame = cap.read()
    if ret == False:
        print("no reading")
    else:
        k = cv2.waitKey(25) & 0xff 
        if k == 27:
            break
        
        fgmask = fgbg.apply(frame)
        # Flip video stream input horisontally
        fgmask = cv2.flip(fgmask, 1)
        fgmask = fgmask[235:245,0:360]
        # kernel = np.ones((2,2),np.uint8)
        #fgmask = cv2.erode(fgmask,kernel,iterations = 1)
        #fgmask = cv2.dilate(fgmask, kernel, iterations = 1)
        # cv2.rectangle(fgmask,(0,235),(300,245),(0,255,0),3)
        # cv2.imshow('frame', frame)
        cv2.imshow('frame',fgmask)

        h = int(time.time() % 6)
        r = h * 51
        b = 255 - r
        for i in range (0, 120):
            if fgmask[5, i*3] > 5:
                strip1.setPixelColor(i,  Color(r,0,b))
                strip1.show()
                strip2.setPixelColor(i,  Color(r,0,b))
                strip2.show()
                #time.sleep(5/ 1000)
            # else :
                # strip.setPixelColor(i,  Color(0,0,0))
                # strip.show() a
                # singlePix(i, Color(0,0,255))
                #time.sleep(5/ 1000)
            
cap.release()
cv2.destroyAllWindows()



