import numpy as np
import cv2
import collections
import time
import math
import threading
import constants
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

BG_COLOR = 0 # the background color of the game
TRAIL_COLOR = (255,0,0) # the color of the trail following the tracked object
FPS = 60 # the FPS the game runs at
POINT_LIMIT = FPS / 4;
JITTER_POINT = 1 # the pixel difference needed to actually draw a new line segment (I'm not sure if this really works as-is)
MIN_SWIPE = 50 # the minimum number of pixels the distance a swipe has to move before it is registered
COOLDOWN = 1 # the number of seconds swipes are not tracked after a swipe occurs
X = 0
Y = 1

trailPoints = collections.deque()

def changeLowH(x):
    global lowH
    lowH = x
def changeHighH(x):
    global highH
    highH = x
def changeLowS(x):
    global lowS
    lowS = x
def changeHighS(x):
    global highS
    highS = x
def changeLowV(x):
    global lowV
    lowV = x
def changeHighV(x):
    global highV
    highV = x
# adds points to the trail, pops off oldest point if past length limit and effectively removes the line by redrawing it as background
def addPoint(x):
    global trailPoints
    trailPoints.append(x)
    if len(trailPoints) > POINT_LIMIT:
        remove = trailPoints.popleft()
        cv2.line(game, remove, trailPoints[0], BG_COLOR)

        

frame_width = 1824
frame_height = 984

game = np.zeros((frame_height, frame_width,3), np.uint8) # initializes game screen as fully black
cv2.namedWindow('Control')

# the HSV color values that are tracked
lowH = constants.LOW_H
highH = constants.HIGH_H

lowS = constants.LOW_S
highS = constants.HIGH_S

lowV = constants.LOW_V
highV = constants.HIGH_V

cv2.createTrackbar("LowH", "Control", lowH, 255, changeLowH)
cv2.createTrackbar("HighH", "Control", highH, 255, changeHighH)

cv2.createTrackbar("LowS", "Control", lowS, 255, changeLowS)
cv2.createTrackbar("HighS", "Control", highS, 255, changeHighS)

cv2.createTrackbar("LowV", "Control", lowV, 255, changeLowV)
cv2.createTrackbar("HighV", "Control", highV, 255, changeHighV)

direction = ""

camera = PiCamera()
camera.resolution = (1824,984)
camera.framerate = 32
camera.brightness = 60
rawCapture = PiRGBArray(camera, size=(1824, 984))
time.sleep(0.1)

currentX = -1
currentY = -1
prevX = -1
prevY = -1
lastSwipe = 0
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Capture frame-by-frame
    frame = image.array
    frame = cv2.resize(frame, (0, 0), fx = 0.125, fy = 0.125)
    frame = cv2.flip(frame,0) # flips along y-axis
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    thresh2 = cv2.inRange(hsv, (lowH, lowS, lowV), (highH, highS, highV))
    cv2.imshow('Before mod',frame) # just shows actual camera output, shown only for debugging
    
    #morphological opening (removes small objects from the foreground)
    #thresh3 = cv2.erode(thresh2, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))
    #thresh3 = cv2.dilate(thresh3, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))
    cv2.imshow('Thresholded',thresh2) # shown only for debugging
    
    momentData = cv2.moments(thresh2)
    moment01 = momentData['m01']
    moment10 = momentData['m10']
    trackedArea = momentData['m00']

    if trackedArea > 10000:
        currentX = int(moment10 * 8 / trackedArea)
        currentY = int(moment01 * 8 / trackedArea)       
    
    if prevX >= 0 and prevY >= 0 and currentX >= 0 and currentY >= 0 and abs(currentX - prevX) > JITTER_POINT and abs(currentY - prevY) > JITTER_POINT:
        cv2.line(game, (currentX, currentY), (prevX, prevY), TRAIL_COLOR)
    
    addPoint((currentX, currentY))
    prevX = currentX
    prevY = currentY

    trailEnd = trailPoints[0]
    dy = trailEnd[Y] - currentY
    dx = trailEnd[X] - currentX
    length = math.hypot(dx, dy)
    if length > MIN_SWIPE and time.time() > lastSwipe + COOLDOWN:
        lastSwipe = time.time()
        if dx != 0:
            slope = dy / dx
        else:
            slope = 50 # placeholder - any value >1 works
            
        if dy >= 0 and dx > 0:
            quadrant = 1
        elif dy >= 0 and dx <= 0:
            quadrant = 2
        elif dy < 0 and dx <= 0:
            quadrant = 3
        else:
            quadrant = 4
            
        if abs(slope) <= 1:
            if quadrant == 1 or quadrant == 4: # L/R might seem unintuitive, but recall screen is flipped along y-axis
                direction = "Left"
            else:
                direction = "Right"
        else:
            if quadrant == 1 or quadrant == 2:
                direction = "Up"
            else:
                direction = "Down"

    cv2.imshow("BrushSmart", game)
    #cv2.putText(game, direction, (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, TRAIL_COLOR)
    #print(direction)
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'): # quit with q
        break
    time.sleep(1/FPS)
#clean-up after quitting
camera.close()
cv2.destroyAllWindows()