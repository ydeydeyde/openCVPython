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
LED_COUNT      = 180      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN_2      = 17      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN_3      = 16      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN_4      = 22      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering



cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=10,varThreshold=100,detectShadows=False)

def singlePix(i, color):
    strip.setPixelColor(i,  color)
    strip.show()
    time.sleep(1/1000.0) 
    
if __name__ == '__main__':
        opt_parse()
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	strip.begin()
	#strip_2 = Adafruit_NeoPixel(LED_COUNT, LED_PIN_2, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	#strip_2.begin()
	#strip_3 = Adafruit_NeoPixel(LED_COUNT, LED_PIN_3, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	#strip_3.begin()
	#strip_4 = Adafruit_NeoPixel(LED_COUNT, LED_PIN_4, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	#strip_4.begin()
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
                strip.setPixelColor(i,  Color(r,0,b))
                strip.show()
                #singlePix(i, Color(255,0,0))
                #time.sleep(5/ 1000)
            # else :
                # strip.setPixelColor(i,  Color(0,0,0))
                # strip.show() a
                # singlePix(i, Color(0,0,255))
                #time.sleep(5/ 1000)
            
cap.release()
cv2.destroyAllWindows()


