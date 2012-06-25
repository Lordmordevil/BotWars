from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform
import glob, sys

class Animation:
    ''' Visualisation of entity. '''
    def __init__(self):
        self.frames = []
        self.curframe = 0
        self.maxframe = 0
        self.timer = 0
    
    def setup(self, folder):
        ''' Goes in the given folder and takes all the framse in order to visualise them later. '''
        tempimages = glob.glob("sprites/" + folder + "/frame*.png")
        tempimages.sort()
        for i in range(len(tempimages)):        
            self.frames.append(pygame.image.load(tempimages[i]))
        self.maxframe = len(self.frames) - 1
 
    def draw(self, target, pos):
        ''' Draw curent frame and move to the next one. '''
        target.screen.blit(self.frames[self.curframe], pos)
        
        if self.curframe == self.maxframe:
            self.curframe = 0
        else:
            if self.timer == 4:
                self.curframe += 1
                self.timer = 0
            else:
                self.timer += 1
    
class Drone:
    '''Class for workers!'''
    def __init__(self):
        self.pos = vec2d(0, 0)
        self.target = []
        self.single_t = True
        self.image = Animation()
        self.image.setup("drone")
        self.def_pic = pygame.image.load("sprites/icons/bat_ico.png")
        self.ico_pic = pygame.image.load("sprites/bot_ico.png")
        self.generator_ico = pygame.image.load("sprites/icons/gico.png")
        self.factory_ico = pygame.image.load("sprites/icons/faico.png")
        self.medbay_ico = pygame.image.load("sprites/icons/med_ico.png")
        self.outpost_ico = pygame.image.load("sprites/icons/out_ico.png")
        self.stockpile_ico = pygame.image.load("sprites/icons/sto_ico.png")
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
                temptargets = self.target[1:]
                self.target = temptargets
                
    def draw_hud(self, target):
        if self.single_t == 1:
            target.screen.blit(target.hud.sing_dir, (280, 427))
        else:
            target.screen.blit(target.hud.mul_dir, (280, 427))
            
        target.screen.blit(self.ico_pic, (230, 505))
        target.drawbattery(cap = 1)
            
        target.screen.blit(target.ores[0].ico, (380, 505))
        pygame.draw.rect(target.screen, (75, 75, 75), (380, 505, 25, 25 - int(self.inventory[1][1] / 40)))
        pygame.draw.rect(target.screen, (0, 0, 0), (380, 505, 25, 25), 2)
            
        target.draw_hudbuttons(5)
        target.screen.blit(self.factory_ico, (637, 447))
        target.screen.blit(self.generator_ico, (687, 447))
        target.screen.blit(self.medbay_ico, (737, 447))
        target.screen.blit(self.outpost_ico, (637, 497))
        target.screen.blit(self.stockpile_ico, (687, 497))
        
    def detectact(self, target, curpos):
        ''' `buttons` contains button coords and building instructions '''
        button = [((646, 456), (6000, 1)), ((696, 456), (5000, 2)), ((746, 456), (5000, 3)), ((646, 506), (5000, 4)), ((696, 506), (5000, 5)),]
        for build_button in button:
            if curpos.get_distance(vec2d(*build_button[0])) <= 15:
                target.startbuild(*build_button[1]) 
       
    def colider (self, odrone, targ):
        dist = self.pos.get_distance(odrone.pos)
        if dist < 56:
            overlap = 56 - dist
            ndir = odrone.pos - self.pos
            ndir.length = overlap
            if self.task == 2 and odrone.power < 1:
                self.inventory[0][1] -= 1
                odrone.power = 150
                self.task = 0    
            if self == targ.selected:
                odrone.pos = odrone.pos + ndir
            elif odrone == targ.selected:
                self.pos = self.pos - ndir
            else:
                ndir.length =  ndir.length / 2
                odrone.pos = odrone.pos + ndir
                self.pos = self.pos - ndir
                
    def droneaction(self, target, pos):
        def helpdrone(target, pos):
            for drone in target.drones:
                if drone.pos.get_distance(vec2d(pos[0] + target.hud.pos[0], pos[1] + target.hud.pos[1])) < 20 and drone.power < 1:
                    if drone is not target.selected:
                        target.selected.target.append(target.buildings[0].pos)
                        target.selected.task = 2
                        target.selected.target.append(vec2d(int(drone.pos[0]), int(drone.pos[1])))
                        print("Going to charge another drone!")
                        return 1
            return 0
        
        def visitbuilding(target, pos):
            for building in target.buildings:
                if building.pos.get_distance(vec2d(pos[0] + target.hud.pos[0], pos[1] + target.hud.pos[1])) < building.size:
                    target.selected.target.append(building.pos)
                    return 1
            return 0
            
        def builddata(target, pos):
            if target.hud.build_mode == 1:
                permit = True
                btarget = vec2d(pos[0] + target.hud.pos[0], pos[1] + target.hud.pos[1])
                for building in target.buildings:
                    dir = building.pos - btarget
                    if dir.length < building.size + 50: permit = False
                if permit:
                    print("The new building will be built at - ", btarget)
                    target.project = btarget
                    target.hud.build_mode = 2
                    target.builder.target.append(target.project)
                    return 1
            return 0
            
        def movedrone(target, pos):
            if target.selected.single_t == 0:
                dtarget = vec2d(pos[0] + target.hud.pos[0], pos[1] + target.hud.pos[1])
                target.selected.target.append(dtarget)
            else:
                targets = []
                dtarget = vec2d(pos[0] + target.hud.pos[0], pos[1] + target.hud.pos[1])
                targets.append(dtarget)
                target.selected.target = targets
                
        found = helpdrone(target, pos)
        if found == 0:
            found = visitbuilding(target, pos)           
        if found == 0:
            found = builddata(target, pos)            
        if found == 0:
            movedrone(target, pos)            
        
class Building:
    def __init__(self):
        self.pos = vec2d(0, 0)
        self.size = 0

    def update(self):
        pass
        
class Main_base(Building):
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
        
    def update(self):
        pass
        
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
                if type(building) is Main_base or type(building) is Outpost:
                    dir = drone.pos - building.pos
                    if dir.length < reldist or reldist == 0:
                        tempbuilding = building
                        reldist = dir.length
            drone.target.append(tempbuilding.pos)
            drone.task = 1
            drone.target.append(vec2d(int(drone.pos[0]), int(drone.pos[1])))
        return True
    
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
        
        firstbuild = Main_base()
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
                    if drone.target[0] == building.pos and (type(building)  is Main_base or type(building)  is Outpost):
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
                elif type(self.selected) is Main_base or type(self.selected) is Outpost:
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
        print(int(self.buildings[0].inventory[1][1]/112000))
        if int(self.buildings[0].inventory[1][1]/112000) == 5:
            self.running = False
        
    def drawstaticmap(self):
        for i in range(9):
            for j in range(7):
                self.screen.blit(self.hud.tile, ( (100 * i) - (self.hud.pos[0] % 100) , (100 * j) - (self.hud.pos[1] % 100) ) )
        for ore in self.ores:
            self.screen.blit(ore.pic, (ore.pos[0] - 50 - self.hud.pos[0], ore.pos[1] - 50 - self.hud.pos[1]) )
        if type(self.selected) is Main_base or type(self.selected) is Outpost:
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
                    if type(obuilding) is Main_base or type(obuilding) is Outpost:
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
