import numpy as np
import cv2
import time
import constants
from tkinter import PhotoImage

"""
The mouth image is created with the time and score in the top left. New germs populate the mouth by quadrants. 

"""

def Draw(state):
    pinkGermImage = PhotoImage(file="./images/pinkGerm.gif")
    blueGermImage = PhotoImage(file="./images/blueGerm.gif")
    greenGermImage = PhotoImage(file="./images/greenGerm.gif")

    timeLeft = int(constants.GAME_LENGTH - (time.time() - state.gameStart))
    state.canvas.create_text((450,200), text="Time: " + str(timeLeft), font=constants.FONT, fill="white", anchor="w")
    state.canvas.create_text((450,250), text="Score: " + str(state.gameScore), font=constants.FONT, fill="white", anchor="w")
    bbox = state.currentUser.gamePositionX - constants.GAME_SIZE, state.currentUser.gamePositionY - constants.GAME_SIZE, state.currentUser.gamePositionX + constants.GAME_SIZE, state.currentUser.gamePositionY + constants.GAME_SIZE
    
    mouthImage = PhotoImage(file="./images/mouth.gif")
    mouthbbox = state.currentUser.gamePositionX, state.currentUser.gamePositionY
    state.canvas.create_image(mouthbbox, image=mouthImage)
    
    mod = (time.time() - state.gameStart) % constants.SECTION_LENGTH
    if mod >= 0.2 and mod <= 2:
        state.canvas.create_arc(bbox, start=float(state.currentQuadrant), extent=90.0, outline="red", style="arc")
        
    for currentGerm in state.germList:
        gamebbox = currentGerm.xPos - currentGerm.size, currentGerm.yPos - currentGerm.size
        if currentGerm.size == 10:
            state.canvas.create_image(gamebbox, image=pinkGermImage)
        elif currentGerm.size == 15:
            state.canvas.create_image(gamebbox, image=blueGermImage)
        else:
            state.canvas.create_image(gamebbox, image=greenGermImage)

    for id in range(len(state.trailPoints) - 1):
        if id == 0: # earliest - darkest
            color = "#006600"
        elif id == 1:
            color = "#009900"
        elif id == 2:
            color = "#00CC00"
        elif id == 3:
            color = "#00FF00"
        coords = state.trailPoints[id][0], state.trailPoints[id][1], state.trailPoints[id + 1][0], state.trailPoints[id + 1][1]
        state.canvas.create_line(coords, fill=color, width=10.0)
    state.canvas.update()
    state.canvas.delete("all")