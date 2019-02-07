from tkinter import *
import constants

"""
This screen first draws "Loading..." then "Detecting face..".

"""

def Draw(state):

    if state.faceTracking:
        state.canvas.create_text((constants.SCREEN_WIDTH/2,constants.SCREEN_HEIGHT/2), text="Detecting face...", fill="white", font=constants.FONT)
    else:
        state.canvas.create_text((constants.SCREEN_WIDTH/2,constants.SCREEN_HEIGHT/2), text="Loading...", fill="white", font=constants.FONT)
        
    state.canvas.update()
    state.canvas.delete("all")

