from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import vec2d
from animation import Animation
from math import e, pi, cos, sin, sqrt
from random import uniform

from drone import Drone
from resource import Ore
from buildings import *            
    
class Hud:
    def __init__(self):
        self.build_mode = 0
        self.buildcolor = (0, 255, 0)
        self.pos = vec2d(0, 0) 
        self.hud = pygame.image.load("sprites/hud.png")
        self.sing_dir = pygame.image.load("sprites/icons/sp.png")
        self.mul_dir = pygame.image.load("sprites/icons/mp.png")
        self.tile = pygame.image.load("sprites/grass.png")
        self.move = [0,0,0,0]

class Starter(PygameHelper):
    def __init__(self):
        self.w, self.h = 800, 600
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((255,255,255)))
        
        self.hud = Hud()
        
        self.drones = []
        
        for i in range(4): 
            tempagent = Drone()
            tempagent.pos = vec2d(int(uniform(0, self.w - 20)), int(uniform(0, 400)))
            target = vec2d(int(uniform(0, self.w - 20)), int(uniform(0, 400)))
            tempagent.target.append(target)
            self.drones.append(tempagent)

        self.selected = self.drones[0]
        self.builder = self.drones[0]
        self.project = vec2d(0, 0)
        self.buildtype = 0
        self.buildpos = vec2d(0, 0)
        
        self.buildings = []
        self.ores = []
        
        count = 0
        while count < 15:
            tempore = Ore()
            tempore.pos = vec2d(int(uniform(0, 1500)), int(uniform(0, 1500)))
            if not len(self.ores) == 0:
                flag = 1
                for orecheck in self.ores:
                    dist = orecheck.pos.get_distance(tempore.pos)
                    if dist < 120:
                        flag = 0
                if flag:
                    self.ores.append(tempore)
                    count += 1
            else:
                self.ores.append(tempore)
                count += 1
        
        firstbuild = MainBase()
        firstbuild.pos = vec2d(300, 300)
        firstbuild.target = vec2d(firstbuild.pos[0] + 10, firstbuild.pos[1])
        self.buildings.append(firstbuild)
            
    def update(self):
    
        def finishbuild (buildtype):
            if buildtype == 1:
                tempbuild = UpgradeFactory()
            elif buildtype == 2:
                tempbuild = Generator()
                self.buildings[0].powergain += 5    
            elif buildtype == 3:
                tempbuild = Medbay()
            elif buildtype == 4:
                tempbuild = Outpost()
                tempbuild.target = vec2d(self.project[0] + 10, self.project[1])
            elif buildtype == 5:
                tempbuild = Whearhouse()
                self.buildings[0].inv += 500000
            tempbuild.pos = self.project
            self.buildings.append(tempbuild)
            self.hud.build_mode = 0
        
        for building in self.buildings:
            building.update()
    
        for drone in self.drones:
            if drone.power > 1:
                for ore in self.ores:
                    if drone.pos.get_distance(ore.pos) < 50:
                        if not ore.mine(self, drone):
                            self.ores.remove(ore)
                            
                dir = drone.target[0] - drone.pos
                if dir.length <= drone.speed and self.hud.build_mode == 2 and drone == self.builder and drone.target[0] == self.project:    
                    if self.builder.pos.get_distance(self.project) < 20:
                        finishbuild(self.buildtype)
                        
                drone.update()
            
            for odrone in self.drones:
                if not drone == odrone: drone.colider(odrone, self)
                
            for building in self.buildings:
                if building.pos.get_distance(drone.pos) < drone.speed:
                    if drone.target[0] == building.pos and (type(building)  is MainBase or type(building)  is Outpost):
                        self.buildings[0].request(drone, building)
                if type(building) is Outpost and building.level == 1 and building.pos.get_distance(drone.pos) < 200:
                    if drone.power > 10:
                        building.fire_target = drone.pos
                        drone.power -= 10
        self.move_window()
                        
    def keyUp(self, key):
        if key == 100:
            self.hud.move[0] = 0
        if key == 97:
            self.hud.move[1] = 0
        if key == 119:
            self.hud.move[2] = 0
        if key == 115:
            self.hud.move[3] = 0
     
    def keyDown(self, key):
        if type(self.selected) is Drone:
            if key == 304:
                self.selected.single_t = not self.selected.single_t
        if key == 100:
            self.hud.move[0] = 1
        if key == 97:
            self.hud.move[1] = 1
        if key == 119:
            self.hud.move[2] = 1
        if key == 115:
            self.hud.move[3] = 1
        
    def mouseUp(self, button, pos):
        
        if pos[1] < 400:
            if button == 3:
                if type(self.selected) is Drone:
                    self.selected.droneaction(self, pos)
                elif type(self.selected) is MainBase or type(self.selected) is Outpost:
                    self.selected.target = vec2d(pos[0] + self.hud.pos[0], pos[1] + self.hud.pos[1])
            elif button == 1:
                found = 0
                for drone in self.drones:
                    if drone.pos.get_distance(vec2d(pos[0] + self.hud.pos[0], pos[1] + self.hud.pos[1])) < 20:
                        self.selected = drone
                        found = 1;
                if found == 0:
                    for building in self.buildings:
                        if building.pos.get_distance(vec2d(pos[0] + self.hud.pos[0], pos[1] + self.hud.pos[1])) < building.size:
                            self.selected = building
                     
        # ------------------- Hud control ------------------------
        else:
            curpos = vec2d(pos)
            if button == 1:
                self.selected.detectact(self, curpos)
        
    def mouseMotion(self, buttons, pos, rel):
        if pos[0] > 750 and pos[1] < 400:
            self.hud.pos[0] += 10
        elif pos[0] < 50 and pos[1] < 400:
            self.hud.pos[0] -= 10
        elif pos[1] < 50:
            self.hud.pos[1] -= 10
        elif pos[1] > 350 and pos[1] < 400:
            self.hud.pos[1] += 10
            
        if  self.hud.build_mode == 1:
            self.buildpos = vec2d(int(pos[0]), int(pos[1]))
            self.hud.buildcolor = (0, 200, 0)
            for building in self.buildings:
                dir = (building.pos - self.hud.pos) - pos
                if dir.length < building.size + 60:
                    self.hud.buildcolor = (255, 0, 0)
                    
    def startbuild(self, price, type):
        if self.buildings[0].inventory[1][1] > price:
            self.buildings[0].inventory[1][1] -= price
            self.hud.build_mode = 1
            self.buildtype = type
            self.selected.target.append(self.buildings[0].pos)
            self.builder = self.selected
  
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        self.drawstaticmap()
            
        if  self.hud.build_mode == 1:
            pygame.draw.rect(self.screen, self.hud.buildcolor, (self.buildpos[0] - 50, self.buildpos[1] - 50, 102, 102), 2)
        
        self.drawentities()
        
        self.screen.blit(self.hud.hud, (0, 400))

        self.selected.draw_hud(self)
                      
    def drawentities(self):
        for drone in self.drones:
            if drone == self.selected:
                pygame.draw.circle(self.screen, (255, 0, 0), drone.target[0] - self.hud.pos, 26, 1)
                for target in drone.target:
                    pygame.draw.circle(self.screen, (255, 0, 0), target - self.hud.pos, 3, 1)
                for i in range(len(drone.target) - 1):
                    pygame.draw.line(self.screen, (255, 0, 0), drone.target[i] - self.hud.pos, drone.target[i + 1] - self.hud.pos)        
            drone.image.draw(self, (drone.pos[0] - 25 - self.hud.pos[0], drone.pos[1] - 25 - self.hud.pos[1]))
            pygame.draw.circle(self.screen, (255 - drone.power, 0 + drone.power, 0), (int(drone.pos[0]) - self.hud.pos[0], int(drone.pos[1] - 2) - self.hud.pos[1]), 2)
        pygame.draw.rect(self.screen, (0, 150, 0), (9, 9, 104, 5), 2)
        pygame.draw.line(self.screen, (255, 255, 0), (11,11), (11 + int(self.buildings[0].inventory[1][1]/112000),11), 2)
        if int(self.buildings[0].inventory[1][1]/112000) == 100:
            self.running = False
        
    def drawstaticmap(self):
        for i in range(9):
            for j in range(7):
                self.screen.blit(self.hud.tile, ( (100 * i) - (self.hud.pos[0] % 100) , (100 * j) - (self.hud.pos[1] % 100) ) )
        for ore in self.ores:
            self.screen.blit(ore.pic, (ore.pos[0] - 50 - self.hud.pos[0], ore.pos[1] - 50 - self.hud.pos[1]) )
        if type(self.selected) is MainBase or type(self.selected) is Outpost:
            pygame.draw.circle(self.screen, (0, 200, 0), self.selected.target - self.hud.pos, 26, 1)
            pygame.draw.line(self.screen, (0, 200, 0), self.selected.pos - self.hud.pos, self.selected.target - self.hud.pos)    
        for building in self.buildings:
            if type(building) is Outpost:
                pygame.draw.line(self.screen, (0, 255, 0), building.pos - self.hud.pos, (building.pos[0],self.buildings[0].pos[1]) - self.hud.pos)
                pygame.draw.line(self.screen, (0, 255, 0), (building.pos[0],self.buildings[0].pos[1]) - self.hud.pos, self.buildings[0].pos - self.hud.pos)
            elif type(building) is Generator or type(building) is Whearhouse:
                tempbuilding = 0
                reldist = 0
                for obuilding in self.buildings:
                    if type(obuilding) is MainBase or type(obuilding) is Outpost:
                        dir = building.pos - obuilding.pos
                        if dir.length < reldist or reldist == 0:
                            tempbuilding = obuilding
                            reldist = dir.length
                pygame.draw.line(self.screen, (0, 255, 0), building.pos - self.hud.pos, (building.pos[0],tempbuilding.pos[1]) - self.hud.pos)
                pygame.draw.line(self.screen, (0, 255, 0), (building.pos[0],tempbuilding.pos[1]) - self.hud.pos, tempbuilding.pos - self.hud.pos)
        for building in self.buildings:
            building.image.draw(self, (building.pos[0] - building.size - self.hud.pos[0], building.pos[1] - building.size - self.hud.pos[1]))
            if type(building) is Outpost and building.level == 1:
                pygame.draw.circle(self.screen, (0, 0, 40), building.pos - self.hud.pos, 200, 2)
                pygame.draw.line(self.screen, (0, 0, 200), building.pos - self.hud.pos, building.fire_target - self.hud.pos)
                building.fire_target = building.pos
                
    def drawbattery(self, cap):
        pygame.draw.rect(self.screen, (0, 0, 0), (345, 515, 15, 10), 2)
        pygame.draw.rect(self.screen, (255 - int(self.selected.power / cap), 0 + int(self.selected.power / cap), 0), (340, 520, 25, 75))
        pygame.draw.rect(self.screen, (0, 0, 0), (340, 520, 25, 75), 2)
        pygame.draw.rect(self.screen, (0, 0, 0), (340, 520, 25, 75 - (self.selected.power / (3.4 * cap))))
           
    def draw_hudbuttons(self, butons):
        if butons >= 1:
            pygame.draw.rect(self.screen, (45, 45, 45), (632, 442, 30, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), (630, 440, 32, 32), 2)
        if butons >= 2:
            pygame.draw.rect(self.screen, (45, 45, 45), (682, 442, 30, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), (680, 440, 32, 32), 2)
        if butons >= 3:
            pygame.draw.rect(self.screen, (45, 45, 45), (732, 442, 30, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), (730, 440, 32, 32), 2)
        if butons >= 4:
            pygame.draw.rect(self.screen, (45, 45, 45), (632, 492, 30, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), (630, 490, 32, 32), 2)
        if butons >= 5:
            pygame.draw.rect(self.screen, (45, 45, 45), (682, 492, 30, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), (680, 490, 32, 32), 2)
        if butons >= 6:
            pygame.draw.rect(self.screen, (45, 45, 45), (732, 492, 30, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), (730, 490, 32, 32), 2)
            
    def move_window(self):
        if self.hud.move[0]: self.hud.pos[0] += 10
        if self.hud.move[1]: self.hud.pos[0] -= 10
        if self.hud.move[2]: self.hud.pos[1] -= 10
        if self.hud.move[3]: self.hud.pos[1] += 10
        
s = Starter()
s.mainLoop(40)
