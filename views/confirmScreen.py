from tkinter import *
import constants

"""
This is a screen that draws the text "Are you sure?" which is used for the user to confirm if they wish to quit the program.
Down ⯆ - Yes, exit the program
Up ⯅ - No, return to the home screen

"""
def Draw(state):
	state.canvas.create_text(constants.UP_NAV, text="NO", fill="white", font=constants.FONT)
	state.canvas.create_text(constants.DOWN_NAV, text="YES", fill="white", font=constants.FONT)
	state.canvas.create_polygon(constants.UP_ARROW, fill="white")
	state.canvas.create_polygon(constants.DOWN_ARROW, fill="white")
	
	state.canvas.create_text((constants.SCREEN_WIDTH/2,constants.SCREEN_HEIGHT/2), text="Are you sure?", fill="white", font=constants.FONT)

##	for id in range(len(state.trailPoints) - 1):
##            coords = state.trailPoints[id][0], state.trailPoints[id][1], state.trailPoints[id + 1][0], state.trailPoints[id + 1][1]
##            state.canvas.create_line(coords, fill="white")
	
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
