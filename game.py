from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

class Drone:
    def __init__(self):
        self.pos = vec2d(0, 0)
        self.target = []
        self.single_t = True
        self.def_pic = pygame.image.load("sprites/bot.png")
        self.sel_pic = pygame.image.load("sprites/bot_s.png")
        self.ico_pic = pygame.image.load("sprites/bot_ico.png")
        self.generator_ico = pygame.image.load("sprites/gico.png")
        self.factory_ico = pygame.image.load("sprites/faico.png")
        self.medbay_ico = pygame.image.load("sprites/bat_ico.png")
        self.power = 255
        self.inventory = [["battery", 0], ["iron ore", 0]]
        self.task = 0
        self.speed = 5
        self.mining_speed = 1
        
    def update(self):
        dir = self.target[0] - self.pos      
        self.power -= 0.1
        if dir.length >= self.speed:
            dir.length = self.speed
            self.pos = vec2d(int(self.pos[0] + dir[0]), int(self.pos[1] + dir[1]))
        else:
            if len(self.target) > 1:
                temptargets = self.target[1:len(self.target)]
                self.target = temptargets
                
    def drawhud(self, target):
        if self.single_t == 1:
            target.screen.blit(target.hud.sing_dir, (280, 427))
        else:
            target.screen.blit(target.hud.mul_dir, (280, 427))
            
        target.screen.blit(self.ico_pic, (230, 505))
        target.drawbattery(cap = 1)
            
        target.screen.blit(target.ores[0].ico, (380, 505))
        pygame.draw.rect(target.screen, (75, 75, 75), (380, 505, 25, 25 - int(self.inventory[1][1] / 40)))
        pygame.draw.rect(target.screen, (0, 0, 0), (380, 505, 25, 25), 2)
            
        target.drawhudbuttons(3)
        target.screen.blit(self.factory_ico, (637, 447))
        target.screen.blit(self.generator_ico, (687, 447))
        target.screen.blit(self.medbay_ico, (737, 447))
        
class Building:
    def __init__(self):
        self.pos = vec2d(0, 0)
        self.size = 0

class Main_base(Building):
    def __init__(self):
        self.size = 35
        self.storepic = pygame.image.load("sprites/main_store.png")
        self.pic = pygame.image.load("sprites/main_base.png")
        self.ico_pic = pygame.image.load("sprites/main_ico.png")
        self.bat_ico = pygame.image.load("sprites/bat_ico.png")
        self.inventory = [["battery", 2], ["iron ore", 500000]]
        self.powergain = 5
        self.power = 100000
        self.inv = 1000000
        
    def request(self, requester):
        if self.power > 255:
            requester.power = 255
            self.power -= 255
        requester.target.insert(1, vec2d(self.pos[0], self.pos[1] + 50))
        if requester.task == 1:
            self.inventory[1][1] += requester.inventory[1][1]
            requester.inventory[1][1] = 0
            print("Resursite v bazata sa", self.inventory, "Power: ", self.power)
            requester.task = 0
            print("Rabotnika se zavrushta da kopae")
        elif requester.task == 2:
            if self.inventory[0][1] > 0:
                print("Rabotnik vze 1 bateriq ot sklada!")
                self.inventory[0][1] -= 1
                requester.inventory[0][1] += 1
               
    def bdrone(self):
        if self.inventory[1][1] > 40000:
            self.inventory[1][1] -= 40000
            tempdrone = Drone()
            tempdrone.pos = self.pos
            target = self.pos
            tempdrone.target.append(target)
            return tempdrone
        else:
            print("You need 40 000 ore to buy this!")
            
    def bbat(self):
        if self.inventory[1][1] > 5000:
            self.inventory[1][1] -= 5000
            self.inventory[0][1] += 1
        else:
            print("You need 5000 to buy a battery!")
            
    def drawhud(self, target):
        target.screen.blit(self.ico_pic, (230, 500))
        target.drawbattery(cap = 1000)       
        target.screen.blit(self.storepic, (381, 501))
        pygame.draw.rect(target.screen, (85, 85, 85), (381, 501, 201, 51 - int(self.inventory[1][1] / (self.inv / 50))))
        pygame.draw.rect(target.screen, (0, 0, 0), (380, 500, 202, 52), 2)  
        target.drawhudbuttons(2)
        target.screen.blit(target.drones[0].sel_pic, (637, 447))
        target.screen.blit(self.bat_ico, (687, 447))
                        
class Up_factory(Building):
    def __init__(self):
        self.ico_pic = pygame.image.load("sprites/factory_ico.png")
        self.pic = pygame.image.load("sprites/factory.png")
        self.supic = pygame.image.load("sprites/spu.png")
        self.mupic = pygame.image.load("sprites/mup.png")
        self.size = 50
        
    def drawhud(self, target):
        target.screen.blit(self.ico_pic, (230, 500))
        target.drawhudbuttons(2)
        target.screen.blit(self.supic, (637, 447))
        target.screen.blit(self.mupic, (687, 447))
        
class Generator(Building):
    def __init__(self):
        self.ico_pic = pygame.image.load("sprites/generator_ico.png")
        self.pic = pygame.image.load("sprites/generator.png")
        self.size = 50    
        
    def drawhud(self, target):
        pass

class Medbay(Building):
    def __init__(self):
        self.ico_pic = pygame.image.load("sprites/generator_ico.png")
        self.pic = pygame.image.load("sprites/medbay.png")
        self.ico_medic = pygame.image.load("sprites/mup.png")
        self.ico_medshop = pygame.image.load("sprites/mup.png")
        self.size = 50

    def drawhud(self, target):        
        target.screen.blit(self.ico_pic, (230, 500))
        target.drawhudbuttons(2)
        target.screen.blit(self.ico_medic, (637, 447))
        target.screen.blit(self.ico_medshop, (687, 447))

class Ore:
    def __init__(self):
        self.pos = vec2d(0, 0)
        self.pic = pygame.image.load("sprites/iron_ore.png")
        self.ico = pygame.image.load("sprites/ore_ico.png")
        self.quantity = 800000
        self.size = 50
        
class Hud:
    def __init__(self):
        self.build_mode = 0
        self.pos = vec2d(0, 0) 
        self.hud = pygame.image.load("sprites/hud.png")
        self.sing_dir = pygame.image.load("sprites/sp.png")
        self.mul_dir = pygame.image.load("sprites/mp.png")
        
        self.tile = pygame.image.load("sprites/grass.png")

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
        
        for ore in range (15):
            tempore = Ore()
            tempore.pos = vec2d(int(uniform(0, 1500)), int(uniform(0, 1500)))
            self.ores.append(tempore)
        
        firstbuild = Main_base()
        firstbuild.pos = vec2d(300, 300)
        self.buildings.append(firstbuild)
            
    def update(self):
    
        def finishbuild (buildtype):
            if buildtype == 1:
                tempbuild = Up_factory()
            elif buildtype == 2:
                tempbuild = Generator()
                self.buildings[0].powergain += 5    
            elif buildtype == 3:
                tempbuild = Medbay()
            tempbuild.pos = self.project
            self.buildings.append(tempbuild)
            self.hud.build_mode = 0
        
        if self.buildings[0].power < 255000:
            self.buildings[0].power += self.buildings[0].powergain
    
        for drone in self.drones:
            if drone.power > 1:
                for ore in self.ores:
                    if drone.pos.get_distance(ore.pos) < 50:
                        drone.inventory[1][1] += drone.mining_speed
                        ore.quantity -= 1
                        if ore.quantity < 0:
                            self.ores.remove(ore)
                        if drone.inventory[1][1] >= 1000 and drone.task == 0:
                            drone.target.append(self.buildings[0].pos)
                            drone.task = 1
                            print("Rabotnika se vrushta za da ostavi resursi v bzata")
                            drone.target.append(vec2d(int(drone.pos[0]), int(drone.pos[1])))
                            
                dir = drone.target[0] - drone.pos
                if dir.length <= drone.speed and self.hud.build_mode == 2 and drone == self.builder and drone.target[0] == self.project:    
                    if self.builder.pos.get_distance(self.project) < 20:
                        finishbuild(self.buildtype)
                        
                drone.update()
            for odrone in self.drones:
                if drone == odrone: continue
                dist = drone.pos.get_distance(odrone.pos)
                if dist < 26:
                    overlap = 26 - dist
                    ndir = odrone.pos - drone.pos
                    ndir.length = overlap
                    if drone.task == 2 and odrone.power < 1:
                        drone.inventory[0][1] -= 1
                        odrone.power = 150
                        drone.task = 0    
                    if drone == self.selected:
                        odrone.pos = odrone.pos + ndir
                    elif odrone == self.selected:
                        drone.pos = drone.pos - ndir
                    else:
                        ndir.length =  ndir.length / 2
                        odrone.pos = odrone.pos + ndir
                        drone.pos = drone.pos - ndir
            for building in self.buildings:
                if building.pos.get_distance(drone.pos) < drone.speed:
                    if drone.target[0] == building.pos and building == self.buildings[0]:
                        building.request(drone)
                    
    def keyUp(self, key):
        pass 
     
    def keyDown(self, key):
        if type(self.selected) is Drone:
            if key == 304:
                self.selected.single_t = not self.selected.single_t
        
    def mouseUp(self, button, pos):
        
        if pos[1] < 400:
            if button == 3:
                if type(self.selected) is Drone:
                    found = 0
                    for drone in self.drones:
                        if drone.pos.get_distance(vec2d(pos[0] + self.hud.pos[0], pos[1] + self.hud.pos[1])) < 20 and drone.power < 1:
                            if not drone == self.selected:
                                self.selected.target.append(self.buildings[0].pos)
                                self.selected.task = 2
                                self.selected.target.append(vec2d(int(drone.pos[0]), int(drone.pos[1])))
                                found = 1
                    if found == 0:
                        for building in self.buildings:
                            if building.pos.get_distance(vec2d(pos[0] + self.hud.pos[0], pos[1] + self.hud.pos[1])) < building.size:
                                self.selected.target.append(building.pos)
                                found = 1
                    if found == 0:
                        if self.hud.build_mode == 1:
                            target = vec2d(pos[0] + self.hud.pos[0], pos[1] + self.hud.pos[1])
                            print("Sgradata shte bude ostroena na koordinati - ", target)
                            self.project = target
                            self.hud.build_mode = 2
                            self.builder.target.append(self.project)
                            found = 1
                    if found == 0:
                        if self.selected.single_t == 0:
                            target = vec2d(pos[0] + self.hud.pos[0], pos[1] + self.hud.pos[1])
                            self.selected.target.append(target)
                        else:
                            targets = []
                            target = vec2d(pos[0] + self.hud.pos[0], pos[1] + self.hud.pos[1])
                            targets.append(target)
                            self.selected.target = targets
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
        
        def startbuild(price, type):
            if self.buildings[0].inventory[1][1] > price:
                self.buildings[0].inventory[1][1] -= price
                self.hud.build_mode = 1
                self.buildtype = type
                self.selected.target.append(self.buildings[0].pos)
                self.builder = self.selected
        
        curpos = vec2d(pos)
        if button == 1:
            if type(self.selected) == Main_base:
                if curpos.get_distance(vec2d(646, 456)) <= 15:
                    self.drones.append(self.selected.bdrone())
                if curpos.get_distance(vec2d(696, 456)) <= 15:
                    self.selected.bbat()
            if type(self.selected) == Up_factory:
                if curpos.get_distance(vec2d(646, 456)) <= 15:
                    if self.buildings[0].inventory[1][1] > 40000:
                        self.buildings[0].inventory[1][1] -= 40000
                        Drone.speed = 6
                        print("Drone speed upgraded 20%")
                        for drone in self.drones:
                            drone.speed = 6
                    else:
                        print("You need 40 000 ore to buy speed upgrade!")
                if curpos.get_distance(vec2d(696, 456)) <= 15:
                    if self.buildings[0].inventory[1][1] > 40000:
                        self.buildings[0].inventory[1][1] -= 40000
                        Drone.mining_speed = 2
                        print("Drone mining speed increased by 100%")
                        for drone in self.drones:
                            drone.mining_speed = 2
                    else:
                        print("You need 40 000 ore to buy mining speed upgrade!")
            if type(self.selected) == Medbay:
                if curpos.get_distance(vec2d(646, 456)) <= 15:
                    if self.buildings[0].inventory[1][1] > 40000:
                        self.buildings[0].inventory[1][1] -= 40000

                        print("medic ready for duty")

                    else:
                        print("You need 40 000 ore to buy this unit!")
                if curpos.get_distance(vec2d(696, 456)) <= 15:
                    if self.buildings[0].inventory[1][1] > 40000:
                        self.buildings[0].inventory[1][1] -= 40000

                        print("Battery truck ready for duty")

                    else:
                        print("You need 40 000 ore to buy this unit!")
            if type(self.selected) == Drone:
                if curpos.get_distance(vec2d(646, 456)) <= 15:
                    startbuild(60000, 1)
                if curpos.get_distance(vec2d(696, 456)) <= 15:
                    startbuild(50000, 2)
                if curpos.get_distance(vec2d(746, 456)) <= 15:
                    startbuild(50000, 3)
                    
        
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
            
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        self.drawstaticmap()
            
        if  self.hud.build_mode == 1:
            pygame.draw.rect(self.screen, (0, 200, 0), (self.buildpos[0] - 50, self.buildpos[1] - 50, 102, 102), 2)
        
        self.drawentities()
        
        self.screen.blit(self.hud.hud, (0, 400))

        self.selected.drawhud(self)
            
            
    def drawentities(self):
        for drone in self.drones:
            if drone == self.selected:
                pygame.draw.circle(self.screen, (255, 0, 0), drone.target[0] - self.hud.pos, 21, 1)
                for target in drone.target:
                    pygame.draw.circle(self.screen, (255, 0, 0), target - self.hud.pos, 3, 1)
                for i in range(len(drone.target) - 1):
                    pygame.draw.line(self.screen, (255, 0, 0), drone.target[i] - self.hud.pos, drone.target[i + 1] - self.hud.pos)
                self.screen.blit(drone.sel_pic, (drone.pos[0] - 10 - self.hud.pos[0], drone.pos[1] - 10 - self.hud.pos[1]))
            else:
                self.screen.blit(drone.def_pic, (drone.pos[0] - 10 - self.hud.pos[0], drone.pos[1] - 10 - self.hud.pos[1]))
            pygame.draw.circle(self.screen, (255 - drone.power, 0 + drone.power, 0), (int(drone.pos[0]) - self.hud.pos[0], int(drone.pos[1] - 2) - self.hud.pos[1]), 2)
            
    def drawstaticmap(self):
        for i in range(9):
            for j in range(7):
                self.screen.blit(self.hud.tile, ( (100 * i) - (self.hud.pos[0] % 100) , (100 * j) - (self.hud.pos[1] % 100) ) )
        for ore in self.ores:
            self.screen.blit(ore.pic, (ore.pos[0] - 50 - self.hud.pos[0], ore.pos[1] - 50 - self.hud.pos[1]) )
        for building in self.buildings:
            self.screen.blit(building.pic, (building.pos[0] - building.size - self.hud.pos[0], building.pos[1] - building.size - self.hud.pos[1]))
            pygame.draw.circle(self.screen, (255, 0, 0), (building.pos[0] - self.hud.pos[0], building.pos[1] - self.hud.pos[1]), 2)
            
    def drawbattery(self, cap):
        pygame.draw.rect(self.screen, (0, 0, 0), (345, 515, 15, 10), 2)
        pygame.draw.rect(self.screen, (255 - int(self.selected.power / cap), 0 + int(self.selected.power / cap), 0), (340, 520, 25, 75))
        pygame.draw.rect(self.screen, (0, 0, 0), (340, 520, 25, 75), 2)
        pygame.draw.rect(self.screen, (0, 0, 0), (340, 520, 25, 75 - (self.selected.power / (3.4 * cap))))
           
    def drawhudbuttons(self, butons):
        if butons >= 1:
            pygame.draw.rect(self.screen, (45, 45, 45), (632, 442, 30, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), (630, 440, 32, 32), 2)
        if butons >= 2:
            pygame.draw.rect(self.screen, (45, 45, 45), (682, 442, 30, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), (680, 440, 32, 32), 2)
        if butons >= 3:
            pygame.draw.rect(self.screen, (45, 45, 45), (732, 442, 30, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), (730, 440, 32, 32), 2)
        
s = Starter()
s.mainLoop(40)
