from models import user
import constants
import collections
import datetime
from tkinter import Tk, Canvas

"""
This class keeps track of all the temporary values used throughout our
system.
"""
class SystemState():
    def __init__(self):
        self.currentUser = user.User(None)
        self.trailPoints = collections.deque()
        self.currentPage = constants.Page.HOME
        self.direction = constants.Direction.NONE
        self.lastSwipe = 0 # the last time
        self.userList = [] # all the user objects saved in the system
        self.alphabetIndex = 0 # index of the alphabet user is currently on for the name screen
        self.selectedMonth = datetime.date.today().month # the current month the user is looking at on the habits screen
        self.active = True # whether the system is on or not
        self.gameStart = 0 # what time the game started at
        self.lastGermCheck = 0 # the last time the game checked to generate a germ
        self.germList = [] # the germs currently active for the game
        self.gameScore = 0
        
        # the order in which the 4 quadrants are gone through for a game
        self.quadrantOrder = [constants.Quadrant.TOPRIGHT, constants.Quadrant.TOPLEFT, constants.Quadrant.BOTTOMLEFT, constants.Quadrant.BOTTOMRIGHT]
        self.curId = 0 # the id in the quadrant order the game is currently on
        self.currentQuadrant = 0 # the current quadrant the game is on
        self.lastQuadrantTransition = 0 # the last time 
        self.canvas = self.makeCanvas() # the canvas everything is drawn on
        self.faceTracking = False # whether or not the system is performing facial recognition
        self.selectedUser = 0 # which user (as an index) the user has currently selected on the enterUser screen
        self.newHighScore = False # whether or not the user got a new high score on their last game
     
    # sets the page of the system to the passed page
    def setPage(self, newPage):
        self.currentPage = newPage
        trailPoints = collections.deque()
    
    # sets the direction of the system to nothing
    def resetDirection(self):
        self.direction = constants.Direction.NONE

    # adds points to the trail, pops off oldest point if past length limit
    def addPoint(self, x):
        self.trailPoints.append(x)
        if len(self.trailPoints) > constants.POINT_LIMIT:
            self.trailPoints.popleft()
     
    # returns a black fullscreen canvas
    def makeCanvas(self):
        root = Tk()
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        GUI = MyFirstGUI(root)
        return GUI.canvas
            
# a class used to initiate a canvas
class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("BrushSmart")
        
        self.canvas = Canvas(master, width=1824, height=992, background="black")
        self.canvas.pack()
