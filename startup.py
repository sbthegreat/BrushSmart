# -*- coding: utf-8 -*-

import face_recognition
import cv2
import os
import pickle
from models import user

"""
Retrieves the stored user files and compares their faces against the user
currently using the system. If recognized, logs that user in. Otherwise,
a new user is created. Returns the list of users, the current user
object, and a boolean value indicating whether or not that user is new.
"""
def getUser(state):
    directory = os.path.dirname(os.path.abspath(__file__)) + "/users"
    userFiles = next(os.walk(directory))[2] # list of user files
    userList = []
    loadedEncodings = []

    for userFile in userFiles:
        file = open("users/" + userFile,'rb')
        loadedUser = pickle.load(file)
        file.close()
        
        userList.append(loadedUser)
        loadedImage = loadedUser.image
        loadedEncodings.append(face_recognition.face_encodings(loadedImage)[0])

    onScreenFaces = []
    onScreenEncodings = []
    processing = True
    
    camera = PiCamera()
    camera.resolution = (800,800)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(800,800))
    time.sleep(0.1)
    state.faceTracking = True
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = image.array
        frame = cv2.flip(frame,0) # flips along x-axis due to how our camera is positioned

        small_frame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)

        # only process every other frame of video to save time
        if processing:
            onScreenFaces = face_recognition.face_locations(small_frame)
            onScreenEncodings = face_recognition.face_encodings(small_frame, onScreenFaces)

            if len(onScreenFaces) != 0:
                for encoding in onScreenEncodings:
                    match = face_recognition.compare_faces(loadedEncodings, encoding)
                    
                    for id in range(len(loadedEncodings)):
                        if match[id].any(): # if any of the faces on screen match the loaded user's
                            camera.close()
                            return userList[id], userList, False
                camera.close()
                newUser = user.User(frame) # only reached if face on screen was not recognized
                return newUser, userList, True
        processing = not processing
        rawCapture.truncate(0)
