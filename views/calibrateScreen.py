from tkinter import *
import constants

"""
This screen draws a mouth image which the user is to align with their mouth and calibrate it using the up and down arrows.
Up ⯅ - Move the mouth up
Down ⯆ - Move the mouth down
Left ⯇ - Return to the name screen
Right ⯈ - Finish calibration and go to the home screen

"""

def Draw(state):
    # nav_font = Font(family='Impact', size=30, weight='italic')

    state.canvas.create_polygon(constants.UP_ARROW, fill="white")
    state.canvas.create_polygon(constants.DOWN_ARROW, fill="white")
    state.canvas.create_polygon(constants.RIGHT_ARROW, fill="white")
    state.canvas.create_polygon(constants.LEFT_ARROW, fill="white")

    mouthImage = PhotoImage(file="./images/mouth.gif")   
    mouthbbox = state.currentUser.gamePositionX, state.currentUser.gamePositionY
    state.canvas.create_image(mouthbbox, image=mouthImage)

    state.canvas.create_text(constants.UP_NAV, text="UP", font=constants.FONT, fill="white")
    state.canvas.create_text(constants.DOWN_NAV, text="DOWN", font=constants.FONT, fill="white")
    state.canvas.create_text(constants.LEFT_NAV, text="PREV", anchor="sw", font=constants.FONT, fill="white")
    state.canvas.create_text(constants.RIGHT_NAV, text="DONE", anchor="se", font=constants.FONT, fill="white")


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
