import datetime

# A class representing the users of our system.
class User():
    # Initiated with an image of the user's face.
    def __init__(self, image):
        self.name = ""
        self.image = image
        
        # the coordinates the user's game screen is centered around
        self.gamePositionX = 912
        self.gamePositionY = 496
        
        self.highScore = 0 # the high score they've gotten on the game
        self.brushingTimes = {} # a dictionary (hashmap) associating dates with # of times brushed that date
        self.registerDate = datetime.date.today()
