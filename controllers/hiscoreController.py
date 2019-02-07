from views import hiscoreScreen
import constants

"""
This file controls the High Score page, which displays the high scores of
each user stored in the system. When the user moves down, they return to
the home page.
"""
def Control(state):
    hiscoreScreen.Draw(state)
    if state.direction == constants.Direction.DOWN:
        state.setPage(constants.Page.HOME)
        state.resetDirection()
