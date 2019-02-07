from enum import Enum
from enum import IntEnum
import numpy as np

# An enum representing every page of the system.
class Page(Enum):
    HOME = 1
    GAME = 2
    HISCORE = 3
    HABITS = 4
    ENTERNAME = 5
    CALIBRATE = 6
    CONFIRM = 7
    LOAD = 8
    ENTERUSER = 9

# An enum representing the direction that the user or a germ is moving.
# The values are set up so that their negative values reverse the direction.
class Direction(IntEnum):
    UP = 1
    RIGHT = 2
    DOWN = -1
    LEFT = -2
    NONE = 0

# An enum representing the quadrant of the game screen the user should be
# brushing in.
class Quadrant(IntEnum):
    TOPRIGHT = 0
    TOPLEFT = 90
    BOTTOMLEFT = 180
    BOTTOMRIGHT = 270

FONT = ("lato", 30, "bold") # the font used throughout the system
TRAIL_COLOR = (31,239,239) # the BGR color of the trail following the tracked object during gameplay
FPS = 60 # the FPS the game runs at
POINT_LIMIT = 5 # the maximum number of points stored in the trail
COOLDOWN = 1 # the number of seconds swipes are not tracked after a swipe occurs
MIN_SIZE = 10000 # the smallest size a collection of thresholded pixels can be to register as a tracked object

SCREEN_HEIGHT = 918
SCREEN_WIDTH = 1822

# coordinates used to place menu text in the 4 directions
UP_NAV = (912,125)
DOWN_NAV = (912,795)
RIGHT_NAV = (1712, 481)
LEFT_NAV = (110, 481)

# coordinates used to draw arrows in the 4 directions
UP_ARROW = SCREEN_WIDTH/2 - 150, 100, SCREEN_WIDTH/2 + 150, 100, SCREEN_WIDTH/2, 30
DOWN_ARROW = SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT - 100, SCREEN_WIDTH/2 + 150, SCREEN_HEIGHT - 100, SCREEN_WIDTH/2, SCREEN_HEIGHT - 30
RIGHT_ARROW = SCREEN_WIDTH - 100, SCREEN_HEIGHT/2 - 150, SCREEN_WIDTH - 100, SCREEN_HEIGHT/2 + 150, SCREEN_WIDTH - 30, SCREEN_HEIGHT/2
LEFT_ARROW = 100, SCREEN_HEIGHT/2 - 150, 100, SCREEN_HEIGHT/2 + 150, 30, SCREEN_HEIGHT/2

# the HSV color values that are tracked
LOW_H = 54
HIGH_H = 82
LOW_S = 77
HIGH_S = 255
LOW_V = 42
HIGH_V = 255

# A string containing the alphabet that the system goes through on the naming screen.
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHA_SIZE = 26

GAME_INCREMENT = 30 # how many pixels each swipes moves the game screen during calibration
GAME_SIZE = 200 # how many pixels the radius of the game screen circle is
GAME_LENGTH = 120 # how many seconds each game lasts for
SECTION_LENGTH = 30 # how long each part of the game lasts

# the speeds and radii of the 3 types of germs, used as parallel arrays
GERM_SPEEDS = [4, 3, 2]
GERM_SIZES = [10, 15, 20]
