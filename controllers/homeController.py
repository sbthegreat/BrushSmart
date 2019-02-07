from views import homeScreen
import constants
import time
import random

"""
This file controls the home page, the central hub of operations for our
system. Moving the trail up takes the user to the High Score page, and
moving the trail right lets the user start playing the game. It also
resets any game-related variables stored in the system state. Moving left
takes the user to the habits page, while moving down initiates closing
the system down.
"""
def Control(state):
    homeScreen.Draw(state)
    if state.direction == constants.Direction.UP:
        state.setPage(constants.Page.HISCORE)
        state.resetDirection()
    elif state.direction == constants.Direction.RIGHT:
        state.gameStart = time.time()
        state.lastGermCheck = time.time()
        state.germList = []
        state.gameScore = 0
        state.curId = 0
        random.shuffle(state.quadrantOrder)
        state.currentQuadrant = 0
        state.setPage(constants.Page.GAME)
        state.resetDirection()
    elif state.direction == constants.Direction.LEFT:
        state.selectedUser = 0
        state.setPage(constants.Page.ENTERUSER)
        state.resetDirection()
    elif state.direction == constants.Direction.DOWN:
        state.setPage(constants.Page.CONFIRM)
        state.resetDirection()
