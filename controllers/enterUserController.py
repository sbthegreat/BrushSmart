from views import enterUserScreen
import constants
import datetime

"""
This file controls the page where users enter which user they want to see
the brushing habits of. Moving the trail to the right scrolls to the next
user stored in the system, while moving to the left goes to the previous one.
Going to the ends of the list causes it to wrap around. Moving the trail
down returns the user to the home page, while moving up transports them to
to the habits page for the user they had selected.
"""
def Control(state):
    enterUserScreen.Draw(state)
    if state.direction == constants.Direction.RIGHT:
        state.selectedUser = (state.selectedUser + 1) % len(state.userList)
        state.resetDirection()
    elif state.direction == constants.Direction.LEFT:
        state.selectedUser = (state.selectedUser - 1) % len(state.userList)
        state.resetDirection()
    elif state.direction == constants.Direction.UP:
        state.setPage(constants.Page.HABITS)
        state.resetDirection()
    elif state.direction == constants.Direction.DOWN:
        state.setPage(constants.Page.HOME)
        state.resetDirection()
