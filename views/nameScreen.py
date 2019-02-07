import numpy as np
import cv2
import constants

"""
This screen presents a carousel of letters which the user will select the letters for their name.
Up ⯅ - Accept the letter
Down ⯆ - Accept the name
Left ⯇ - Previous letter
Right ⯈ - Next letter

"""

def Draw(state):    
    state.canvas.create_polygon(constants.UP_ARROW, fill="white")
    state.canvas.create_polygon(constants.DOWN_ARROW, fill="white")
    state.canvas.create_polygon(constants.RIGHT_ARROW, fill="white")
    state.canvas.create_polygon(constants.LEFT_ARROW, fill="white")
    
    	
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
        

    state.canvas.create_text(constants.LEFT_NAV, text="PREV", anchor="sw", font=constants.FONT, fill="white")
    state.canvas.create_text(constants.RIGHT_NAV, text="NEXT", anchor="se", font=constants.FONT, fill="white")
    state.canvas.create_text(constants.UP_NAV, text="Accept Letter", fill="white", font=constants.FONT)
    state.canvas.create_text(constants.DOWN_NAV, text="Accept Name", fill="white", font=constants.FONT)
    
    state.canvas.create_text((constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 - 100), text="I don't recognize you. What's your name?", fill="white", font=constants.FONT)
    # prev letter
    state.canvas.create_text((constants.SCREEN_WIDTH/2 - 100, constants.SCREEN_HEIGHT/2), text=constants.ALPHABET[state.alphabetIndex - 1], fill="white", font=constants.FONT)
    # current letter
    state.canvas.create_text((constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2), text=constants.ALPHABET[state.alphabetIndex], fill="white", font=constants.FONT)
    # next letter
    state.canvas.create_text((constants.SCREEN_WIDTH/2 + 100,constants.SCREEN_HEIGHT/2), text=constants.ALPHABET[(state.alphabetIndex + 1) % constants.ALPHA_SIZE], fill="white", font=constants.FONT)
    state.canvas.create_text((constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 + 100), text=state.currentUser.name, fill="white", font=constants.FONT)
    
    state.canvas.update()
    state.canvas.delete("all")