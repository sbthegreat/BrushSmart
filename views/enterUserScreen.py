import numpy as np
import cv2
import constants

"""
This screen presents question "Which user do you want to check on?", which allows the user to check the habits of whoever is in the system.
Up ⯅ - View the selected user's habits
Down ⯆ - Return to the home screen
Left ⯇ - Previous user in the list
Right ⯈ - Next user in the list 

"""

def Draw(state):
    state.canvas.create_text(constants.UP_NAV, text="HABITS", font=constants.FONT, fill="white")
    state.canvas.create_text(constants.DOWN_NAV, text="HOME", font=constants.FONT, fill="white")
    state.canvas.create_text(constants.LEFT_NAV, text="PREV", anchor="sw", font=constants.FONT, fill="white")
    state.canvas.create_text(constants.RIGHT_NAV, text="NEXT", anchor="se", font=constants.FONT, fill="white")
    
    state.canvas.create_polygon(constants.UP_ARROW, fill="white")
    state.canvas.create_polygon(constants.DOWN_ARROW, fill="white")
    state.canvas.create_polygon(constants.RIGHT_ARROW, fill="white")
    state.canvas.create_polygon(constants.LEFT_ARROW, fill="white")
    
    state.canvas.create_text((constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 - 100), text="Which user do you want to check on?", fill="white", font=constants.FONT)
    state.canvas.create_text((constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2), text=state.userList[state.selectedUser].name, font=constants.FONT, fill="white")
	
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
