import numpy as np
import cv2
import constants

"""
This is main navigation screen. Users can enter habits, high score, game, and exit the program from here. 
Up ⯅ - Go to the high score screen
Down ⯆ - Go to the quit confirmation screen
Left ⯇ - Go to the user selection screen for habits
Right ⯈ - Go to the game screen

"""

def Draw(state):
    
    state.canvas.create_polygon(constants.UP_ARROW, fill="white")
    state.canvas.create_polygon(constants.DOWN_ARROW, fill="white")
    state.canvas.create_polygon(constants.RIGHT_ARROW, fill="white")
    state.canvas.create_polygon(constants.LEFT_ARROW, fill="white")

    state.canvas.create_text(constants.UP_NAV, text="HIGH SCORES", fill="white", font=constants.FONT)
    state.canvas.create_text(constants.DOWN_NAV, text="QUIT", fill="white", font=constants.FONT)
    state.canvas.create_text(constants.RIGHT_NAV, text="GAME", fill="white", font=constants.FONT, anchor="se")
    state.canvas.create_text(constants.LEFT_NAV, text="HABITS", fill="white", font=constants.FONT, anchor="sw")

    state.canvas.create_text((constants.SCREEN_WIDTH/2,constants.SCREEN_HEIGHT/2), text="Welcome, " + state.currentUser.name, fill="white", font=constants.FONT)

    	
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