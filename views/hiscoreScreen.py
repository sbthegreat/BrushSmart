import numpy as np
import cv2
import constants
import numbers
import operator
from tkinter import PhotoImage

"""
This screen lists a single high score from each user in the system
Down ⯆ - Return to the home screen

"""

def Draw(state):
    congratsImage = PhotoImage(file="./images/congrats.gif")
    state.canvas.create_text(constants.DOWN_NAV, text="HOME", font=constants.FONT, fill="white")
    
    state.canvas.create_polygon(constants.DOWN_ARROW, fill="white")
    
    if state.newHighScore:
        state.canvas.create_image((constants.SCREEN_WIDTH/4, constants.SCREEN_HEIGHT/2), image=congratsImage)
    
    scoreList = {}
    for storedUser in state.userList:
        scoreList[storedUser.name] = storedUser.highScore
    
    state.canvas.create_text((constants.SCREEN_WIDTH/2, 100), text="High Scores", font=constants.FONT, fill="white")
    scoreList = sorted(scoreList.items(), key = operator.itemgetter(1), reverse = True)
    counter = 1
    for pair in scoreList:
        state.canvas.create_text((constants.SCREEN_WIDTH/2 - 120, 100 + counter * 75), text=str(counter) + ". " + pair[0] + ": " + str(pair[1]), font=constants.FONT, fill="white",anchor="sw")
        counter += 1
    
	
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