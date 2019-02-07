import numpy as np
import cv2
import collections
import time
import math
import threading
import pickle
import os
from models import *
from views import *
from controllers import *
from enum import Enum
import constants
import startup
from picamera.array import PiRGBArray
from picamera import PiCamera

"""
This is the entry point for our system. It delegates most work to other
functions via multithreading. Once the program has finished, it saves
the updated user data.
"""
def main():
    directory = os.path.dirname(os.path.abspath(__file__)) + "/users"
    state = systemState.SystemState()
    loadThread = threading.Thread(target=loading, args=(state,)) 
    loadThread.start()
    
    while loadThread.isAlive():
        loadController.Control(state)
    loadThread.join()
    motionThread = threading.Thread(target=motionTracking, args=(state,))
    motionThread.start()
    changeData(state)

    motionThread.join()
    
    pickle.dump(state.currentUser, open("users/" + state.currentUser.name, 'wb'))

"""
This function starts the program, calling the startup file to run facial
recognition and return the relevant user object (either the recognized
user or a new one) along with the user list, and then directs the user
to the appropriate page depending on whether or not they're new.
"""    
def loading(state):
    state.currentUser, state.userList, newUser = startup.getUser(state)
    if newUser:
        state.currentPage = constants.Page.ENTERNAME
        state.userList.append(state.currentUser)
    else:
        state.currentPage = constants.Page.HOME

"""
This function initiates the camera, and parses the camera's input for the
color we're trying to track.
"""
def motionTracking(state):
    camera = PiCamera()
    camera.resolution = (912,496)
    camera.framerate = 32
    camera.brightness = 60
    rawCapture = PiRGBArray(camera, size=(912,496))
    time.sleep(2)
    
    currentX = -1
    currentY = -1
    prevX = -1
    prevY = -1
    stopped = True

    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if not state.active:
            break
        frame = image.array
        
        frame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)
        frame = cv2.flip(frame,0) # flips along y-axis
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        thresh = cv2.inRange(hsv, (constants.LOW_H, constants.LOW_S, constants.LOW_V), (constants.HIGH_H, constants.HIGH_S, constants.HIGH_V))
        
        momentData = cv2.moments(thresh)
        moment01 = momentData['m01']
        moment10 = momentData['m10']
        trackedArea = momentData['m00']

        if trackedArea > constants.MIN_SIZE:
            currentX = int(moment10 * 8 / trackedArea)
            currentY = int(moment01 * 8 / trackedArea)
        
        state.addPoint((currentX, currentY))
        prevX = currentX
        prevY = currentY

        trailEnd = state.trailPoints[0]
        dy = trailEnd[1] - currentY
        dx = trailEnd[0] - currentX
        setDirection(dx, dy, state)
        
        cv2.waitKey(1)
        time.sleep(1 / constants.FPS)
        rawCapture.truncate(0)
    
    camera.close()
    cv2.destroyAllWindows()

"""
This funchtion delegates to the appropriate controller based on the
current page.
"""
def changeData(state):
    threadStart = time.time()
    while state.active:
        if state.currentPage == constants.Page.HOME:
            homeController.Control(state)
        elif state.currentPage == constants.Page.GAME:
            gameController.Control(state)
        elif state.currentPage == constants.Page.HISCORE:
            hiscoreController.Control(state)
        elif state.currentPage == constants.Page.HABITS:
            habitsController.Control(state)
        elif state.currentPage == constants.Page.ENTERNAME:
            nameController.Control(state)
        elif state.currentPage == constants.Page.CALIBRATE:
            calibrateController.Control(state)
        elif state.currentPage == constants.Page.CONFIRM:
            confirmController.Control(state)
        elif state.currentPage == constants.Page.LOAD:
            loadController.Control(state)
        elif state.currentPage == constants.Page.ENTERUSER:
            enterUserController.Control(state)
        
        time.sleep(1 / constants.FPS)

"""
This function determines which direction the user is moving the trail in.
Every time a direction is set, a cooldown occurs that no directions can be
set during.
"""
def setDirection(dx, dy, state):
    if time.time() > state.lastSwipe + constants.COOLDOWN:
        lastPoint = state.trailPoints[-1]
        if inRectangle(constants.LEFT_NAV, lastPoint, 200, 200):
            state.lastSwipe = time.time()
            state.direction = constants.Direction.LEFT
            return
            
        if inRectangle(constants.RIGHT_NAV, lastPoint, 200, 200):
            state.lastSwipe = time.time()
            state.direction = constants.Direction.RIGHT
            return
        
        if inRectangle(constants.UP_NAV, lastPoint, 200, 200):
            state.lastSwipe = time.time()
            state.direction = constants.Direction.UP
            return
        
        if inRectangle(constants.DOWN_NAV, lastPoint, 200, 200):
            state.lastSwipe = time.time()
            state.direction = constants.Direction.DOWN
            return

"""
This function determines whether the passed point is in the rectangle
defined by the passed center, height, and width - the rectangle extends
height and width amount of pixels from the center.
"""            
def inRectangle(center, point, height, width):
    return point[0] <= center[0] + width/2 and point[0] > center[0] - width/2 and point[1] <= center[1] + height/2 and point[1] > center[1] - height/2

if __name__ == '__main__': main()
