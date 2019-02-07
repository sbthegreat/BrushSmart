from views import gameScreen
from models import germ
import constants
import time
import random
import math
import datetime
import cv2

"""
This file controls the game. Germs are generated over the game screen,
which disappear and give the user points when the trail crosses over
them. Smaller germs give more points. The germs are only generated in
one quadrant at a time, which is changed every 30 seconds. The game
automatically ends after 2 minutes, and the user's brushing habits and
potentially high score (if beaten) are updated.
"""
def Control(state):
    gameScreen.Draw(state)
    now = time.time()
    
    # check if it's time to move to a new quadrant
    if now - state.lastQuadrantTransition >= constants.SECTION_LENGTH:
        state.lastQuadrantTransition = now
        state.currentQuadrant = state.quadrantOrder[state.curId]
        state.curId += 1
        state.germList = []
    
    # every 1 second, check to see if germ should be generated
    if now - state.lastGermCheck > 1:
        rand = random.randint(1, 2)
        if rand == 1:
            generateGerm(state)
        state.lastGermCheck = now
    
    # see if germs collide with boundaries or trail
    remaining = []
    for currentGerm in state.germList:
        collisionDetection(currentGerm, state)
        currentGerm.move()
        
        keep = True
        for id in range(len(state.trailPoints) - 1):
            if lineIntersection(state.trailPoints[id], state.trailPoints[id + 1], (currentGerm.xPos, currentGerm.yPos), currentGerm.size):
                keep = False
        if keep:
            remaining.append(currentGerm)
        else:
            state.gameScore += 30 - currentGerm.size
                
    state.germList = remaining
    
    # finishing the game
    if now - state.gameStart > constants.GAME_LENGTH:
        if state.currentUser.highScore < state.gameScore:
            state.currentUser.highScore = state.gameScore
            
        today = datetime.date.today()
        if today in state.currentUser.brushingTimes:
            state.currentUser.brushingTimes[today] += 1
        else:
            state.currentUser.brushingTimes[today] = 1
        state.setPage(constants.Page.HISCORE)
        state.resetDirection()

"""
This function creates a new germ with a random starting direction, 
starting position, and category, denoted with id. The category determines
what color, size, and speed the germ moves at, all defined in constants.
"""
def generateGerm(state):
    newGerm = germ.Germ()
    id = random.randint(0,2)
    directions = [-2, -1, 1, 2]
    newGerm.color = constants.GERM_COLORS[id]
    newGerm.size = constants.GERM_SIZES[id]
    newGerm.xPos, newGerm.yPos = getRandStartPt(state.currentUser.gamePositionX, state.currentUser.gamePositionY, constants.GAME_SIZE, newGerm.size, state)
    newGerm.speed = constants.GERM_SPEEDS[id]
    newGerm.direction = random.choice(directions)
    
    state.germList.append(newGerm) 

"""
This function generates a random starting point for a germ, based on the 
current quadrant. It takes in the center of the user's position for their
game screen as (x0, y0), the radius of their game screen (r), and the
size of the germ.
"""
def getRandStartPt(x0, y0, r, germSize, state):
    smallR = r - germSize
    # start by determining the rectangular bounds for a point based on the current quadrant
    if state.currentQuadrant == constants.Quadrant.BOTTOMRIGHT:
        minX = x0
        maxX = x0 + smallR
        minY = y0
        maxY = y0 + smallR
    elif state.currentQuadrant == constants.Quadrant.TOPRIGHT:
        minX = x0
        maxX = x0 + smallR
        minY = y0 - smallR
        maxY = y0
    elif state.currentQuadrant == constants.Quadrant.BOTTOMLEFT:
        minX = x0 - smallR
        maxX = x0
        minY = y0
        maxY = y0 + smallR
    elif state.currentQuadrant == constants.Quadrant.TOPLEFT:
        minX = x0 - smallR
        maxX = x0
        minY = y0 - smallR
        maxY = y0
    
    # however, the quadrants have circular rather than rectangular borders,
    # so, after generating a random point, need to make sure it's in the
    # circlar border as well. if it's not, generate a new one until it is.
    noRand = True
    while noRand:
        randX = random.randint(minX, maxX)
        randY = random.randint(minY, maxY)
        if math.hypot(x0 - randX, y0 - randY) <= smallR:
            noRand = False
            
    return randX, randY

"""
This function checks if the passed germ is colliding with the game's
outer borders, or if it would cross over into an inactive quadrant. If a
collision occurs, the germ's direction is reversed.
""" 
def collisionDetection(currentGerm, state):
    x0 = state.currentUser.gamePositionX
    y0 = state.currentUser.gamePositionY
    if state.currentQuadrant == constants.Quadrant.BOTTOMRIGHT:
        outOfQuadrant = currentGerm.xPos < x0 or currentGerm.yPos < y0
    elif state.currentQuadrant == constants.Quadrant.TOPRIGHT:
        outOfQuadrant = currentGerm.xPos < x0 or currentGerm.yPos > y0
    elif state.currentQuadrant == constants.Quadrant.BOTTOMLEFT:
        outOfQuadrant = currentGerm.xPos > x0 or currentGerm.yPos < y0
    elif state.currentQuadrant == constants.Quadrant.TOPLEFT:
        outOfQuadrant = currentGerm.xPos > x0 or currentGerm.yPos > y0
  
    outOfCircle = distance(x0, y0, currentGerm.xPos, currentGerm.yPos) + currentGerm.size > constants.GAME_SIZE
    if outOfQuadrant or outOfCircle:
        currentGerm.direction *= -1

"""
This function checks if the line formed by pt1 and pt2 intersects with
the circle defined by circleCenter and r. This is a loose algorithm that
only checks if the end points or the midpoint of that line is inside the
circle.
"""
def lineIntersection(pt1, pt2, circleCenter, r):
    pt1Inside = distance(pt1[0], pt1[1], circleCenter[0], circleCenter[1]) < r
    pt2Inside = distance(pt2[0], pt2[1], circleCenter[0], circleCenter[1]) < r
    midX = int((pt1[0] + pt2[0]) / 2)
    midY = int((pt1[1] + pt2[1]) / 2)
    midInside = distance(midX, midY, circleCenter[0], circleCenter[1]) < r
    
    return pt1Inside or pt2Inside or midInside
   
"""
This functions computes the distance between two points.
"""  
def distance(px1, py1, px2, py2):
    return math.hypot(px1 - px2, py1 - py2)
