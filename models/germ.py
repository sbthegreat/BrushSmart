import constants

# A class representing the germs used in the game.
class Germ():
    def __init__(self):
        self.size = 0 # the radius of the germ
        self.speed = 0 # number of pixels germ moves every refresh
        self.xPos = 0
        self.yPos = 0
        self.direction = 0
       
    # moves the germ in the direction it's currently in
    def move(self):
        if self.direction == constants.Direction.UP:
            self.yPos -= self.speed
        elif self.direction == constants.Direction.RIGHT:
            self.xPos += self.speed
        elif self.direction == constants.Direction.DOWN:
            self.yPos += self.speed
        elif self.direction == constants.Direction.LEFT:
            self.xPos -= self.speed
