from views import nameScreen
import constants

"""
This file controls the page where new users enter their name. Moving the
trail right goes to next letter in the alphabet, while moving it to the
left goes to the previous letter. The alphabet wraps around when the user
goes past the beginning or end. Moving the trail down goes on to the
calibration page.
"""
def Control(state):
    nameScreen.Draw(state)
    if state.direction == constants.Direction.UP:
        state.currentUser.name += constants.ALPHABET[state.alphabetIndex]
        state.resetDirection()
    elif state.direction == constants.Direction.RIGHT:
        state.alphabetIndex = (state.alphabetIndex + 1) % constants.ALPHA_SIZE
        state.resetDirection()
    elif state.direction == constants.Direction.LEFT:
        state.alphabetIndex = (state.alphabetIndex - 1) % constants.ALPHA_SIZE
        state.resetDirection()
    elif state.direction == constants.Direction.DOWN:
        state.setPage(constants.Page.CALIBRATE)
        state.resetDirection()
