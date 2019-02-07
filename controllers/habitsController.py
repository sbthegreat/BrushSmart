from views import habitsScreen
import constants
import datetime

"""
This file controls the habits page. It displays a calendar view to show
the user the habits of the user they selected. Moving to the right goes to
the next month, while moving left goes to the previous month. If scrolling
past January or December, it wraps around to the other end of the same year.
Moving the trail down takes the user back to the home page.
"""
def Control(state):
    habitsScreen.Draw(state)
    if state.direction == constants.Direction.RIGHT:
        state.selectedMonth = (state.selectedMonth % 12) + 1
        state.resetDirection()
    elif state.direction == constants.Direction.LEFT:
        state.selectedMonth = ((state.selectedMonth - 2) % 12) + 1
        state.resetDirection()
    elif state.direction == constants.Direction.DOWN:
        state.setPage(constants.Page.HOME)
        state.resetDirection()
