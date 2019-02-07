from views import calibrateScreen
import constants
from models import user

"""
This file controls the calibration page, where the user can change the
position of the game screen by moving the trail up and down. Each motion
up or down moves the screen a fixed number of pixels, defined in constants
as GAME_INCREMENT. Moving to the right advances to the home page.
"""
def Control(state):
    calibrateScreen.Draw(state)
    if state.direction == constants.Direction.UP:
        state.currentUser.gamePositionY -= constants.GAME_INCREMENT
        state.resetDirection()
    elif state.direction == constants.Direction.RIGHT:
        state.setPage(constants.Page.HOME)
        state.resetDirection()
    elif state.direction == constants.Direction.LEFT:
        state.setPage(constants.Page.ENTERNAME)
        state.resetDirection()
    elif state.direction == constants.Direction.DOWN:
        state.currentUser.gamePositionY += constants.GAME_INCREMENT
        state.resetDirection()
