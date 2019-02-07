from views import loadScreen
import constants

"""
This file controls the load screen. Since the load screen only shows data
rather than do anything on its own, this file only exists for architecture
consistency.
"""
def Control(state):
    loadScreen.Draw(state)
