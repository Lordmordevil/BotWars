from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import vec2d
from animation import Animation
from math import e, pi, cos, sin, sqrt
from random import uniform


class Building:
    def __init__(self):
        self.pos = vec2d(0, 0)
        self.size = 0

    def update(self):
        pass

class MainBase(Building):
    def __init__(self):
        self.size = 140
        self.storepic = pygame.image.load("sprites/main_store.png")
        self.image = Animation()
        self.image.setup("main")
        self.ico_pic = pygame.image.load("sprites/main_ico.png")
        self.bat_ico = pygame.image.load("sprites/icons/bat_ico.png")
        self.dro_ico = pygame.image.load("sprites/icons/dro_ico.png")
        self.inventory = [["battery", 2], ["iron ore", 500000]]
        self.powergain = 5
        self.target = vec2d(0, 0)
        self.power = 100000
        self.inv = 1000000
        
    def request(self, requester, caller):
        if self.power > 255:
            self.power -= int(255 - requester.power)
            requester.power = 255
        if requester.task == 1:
            self.inventory[1][1] += requester.inventory[1][1]
            requester.inventory[1][1] = 0
            print("Main stock is: ", self.inventory, "Power: ", self.power)
            requester.task = 0
            print("Drone returns to mining duty.")
        elif requester.task == 2:
            if self.inventory[0][1] > 0:
                print("Drone took one battery from store.We have ", self.inventory[0][1]," left!")
                self.inventory[0][1] -= 1
                requester.inventory[0][1] += 1
        requester.target.insert(1, caller.target)
               
    def buy_drone(self):
        if self.inventory[1][1] > 10000:
            self.inventory[1][1] -= 10000
            tempdrone = Drone()
            tempdrone.pos = self.pos
            target = self.pos
            tempdrone.target.append(target)
            print("New drone is waiting for orders!")
            return tempdrone
        else:
            print("You need 10 000 ore to buy this!")
            
    def buy_battery(self):
        if self.inventory[1][1] > 5000:
            self.inventory[1][1] -= 5000
            self.inventory[0][1] += 1
            print("Another battery added to storage!")
        else:
            print("You need 5000 to buy a battery!")
            
    def update (self):
        if self.power < 255000:
            self.power += self.powergain
            
    def draw_hud(self, target):
        target.screen.blit(self.ico_pic, (230, 500))
        target.drawbattery(cap = 1000)       
        target.screen.blit(self.storepic, (381, 501))
        pygame.draw.rect(target.screen, (85, 85, 85), (381, 501, 201, 51 - int(self.inventory[1][1] / (self.inv / 50))))
        pygame.draw.rect(target.screen, (0, 0, 0), (380, 500, 202, 52), 2)  
        target.draw_hudbuttons(2)
        target.screen.blit(self.dro_ico, (637, 447))
        target.screen.blit(self.bat_ico, (687, 447))
            
    def detectact(self, target, curpos):
        if curpos.get_distance(vec2d(646, 456)) <= 15:
            target.drones.append(self.buy_drone())
        if curpos.get_distance(vec2d(696, 456)) <= 15:
            self.buy_battery()
            
class UpgradeFactory(Building):
    def __init__(self):
        self.ico_pic = pygame.image.load("sprites/factory_ico.png")
        self.image = Animation()
        self.image.setup("factory")
        self.supic = pygame.image.load("sprites/icons/spu.png")
        self.mupic = pygame.image.load("sprites/icons/mup.png")
        self.size = 50
        
    def draw_hud(self, target):
        target.screen.blit(self.ico_pic, (230, 500))
        target.draw_hudbuttons(2)
        target.screen.blit(self.supic, (637, 447))
        target.screen.blit(self.mupic, (687, 447))
        
    def detectact(self, target, curpos):
        if curpos.get_distance(vec2d(646, 456)) <= 15:
            if target.buildings[0].inventory[1][1] > 40000:
                target.buildings[0].inventory[1][1] -= 40000
                Drone.speed = 6
                print("Drone speed upgraded by 20%.")
                for drone in target.drones:
                    drone.speed = 6
            else:
                print("You need 40 000 ore to buy speed upgrade!")
        if curpos.get_distance(vec2d(696, 456)) <= 15:
            if target.buildings[0].inventory[1][1] > 40000:
                target.buildings[0].inventory[1][1] -= 40000
                Drone.mining_speed = 2
                print("Drone mining speed increased by 100%")
                for drone in target.drones:
                    drone.mining_speed = 2
            else:
                print("You need 40 000 ore to buy mining speed upgrade!")
        
class Generator(Building):
    def __init__(self):
        self.ico_pic = pygame.image.load("sprites/generator_ico.png")
        self.image = Animation()
        self.image.setup("generator")
        self.size = 50    
    
    def draw_hud(self, target):
        pass
        
    def detectact(self, target, curpos):
        pass
        
class Whearhouse(Building):
    def __init__(self):
        self.ico_pic = pygame.image.load("sprites/generator_ico.png")
        self.image = Animation()
        self.image.setup("stockpile")
        self.size = 50    
    
    def draw_hud(self, target):
        pass
        
    def detectact(self, target, curpos):
        pass
        
class Outpost(Building):
    def __init__(self):
        self.ico_pic = pygame.image.load("sprites/generator_ico.png")
        self.up_ico = pygame.image.load("sprites/icons/up_ico.png")
        self.image = Animation()
        self.image.setup("outpost")
        self.size = 35
        self.level = 0
        self.target = vec2d(0, 0)
        self.fire_target = vec2d(0, 0)
        
    def draw_hud(self, target):
        target.screen.blit(self.ico_pic, (230, 500))
        target.draw_hudbuttons(1)
        target.screen.blit(self.up_ico, (637, 447))

    def detectact(self, target, curpos):
        if curpos.get_distance(vec2d(646, 456)) <= 15:
            self.upgrade()
            
    def upgrade(self):
        self.level = 1
        self.target = self.pos
        self.fire_target = self.pos
        tempimage = Animation()
        tempimage.setup("upoutpost")
        self.image = tempimage

class Medbay(Building):
    def __init__(self):
        self.ico_pic = pygame.image.load("sprites/generator_ico.png")
        self.image = Animation()
        self.image.setup("medbay")
        self.ico_medic = pygame.image.load("sprites/icons/mup.png")
        self.ico_medshop = pygame.image.load("sprites/icons/mup.png")
        self.size = 50

    def draw_hud(self, target):        
        target.screen.blit(self.ico_pic, (230, 500))
        target.draw_hudbuttons(2)
        target.screen.blit(self.ico_medic, (637, 447))
        target.screen.blit(self.ico_medshop, (687, 447))
        
    def detectact(self, target, curpos):
        if curpos.get_distance(vec2d(646, 456)) <= 15:
            if target.buildings[0].inventory[1][1] > 20000:
                target.buildings[0].inventory[1][1] -= 20000

                print("Medic ready for duty!")

            else:
                print("You need 20 000 ore to buy this unit!")
        if curpos.get_distance(vec2d(696, 456)) <= 15:
            if target.buildings[0].inventory[1][1] > 40000:
                target.buildings[0].inventory[1][1] -= 40000

                print("Battery truck ready for duty!")

            else:
                print("You need 40 000 ore to buy this unit!")
