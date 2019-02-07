from views import confirmScreen
import constants

"""
This file controls the confirmation page, used to confirm whether or not the
user truly wishes to quit the system. If they move up, they are returned to
the home page. If they move down, the system shuts down.
"""
def Control(state):
    confirmScreen.Draw(state)
    if state.direction == constants.Direction.UP:
        state.setPage(constants.Page.HOME)
        state.resetDirection()
    elif state.direction == constants.Direction.DOWN:
        state.active = False
