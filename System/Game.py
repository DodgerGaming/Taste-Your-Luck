from Entities.Actor import Actor
from Entities.Shotgun import Shotgun

class Game:
    def __init__(self):

        self.player = Actor()
        self.enemy = Actor()
        self.shotgun = Shotgun()

        self.current_level = 1
        self.win_count = 0