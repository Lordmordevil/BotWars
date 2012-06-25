from pygamehelper import *
from pygame import *
from vec2d import vec2d
from animation import Animation

from drone import Drone
from buildings import MainBase, Outpost

class Ore:
    def __init__(self):
        self.pos = vec2d(0, 0)
        self.pic = pygame.image.load("sprites/iron_ore.png")
        self.ico = pygame.image.load("sprites/icons/ore_ico.png")
        self.quantity = 800000
        self.size = 50
        
    def mine(self, targ, drone):
        reldist = 0
        drone.inventory[1][1] += drone.mining_speed
        self.quantity -= 1
        if self.quantity < 0:
            return False
        if drone.inventory[1][1] >= 1000 and drone.task == 0:
            for building in targ.buildings:
                if type(building) is MainBase or type(building) is Outpost:
                    dir = drone.pos - building.pos
                    if dir.length < reldist or reldist == 0:
                        tempbuilding = building
                        reldist = dir.length
            drone.target.append(tempbuilding.pos)
            drone.task = 1
            drone.target.append(vec2d(int(drone.pos[0]), int(drone.pos[1])))
        return True