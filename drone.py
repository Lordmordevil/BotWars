from pygamehelper import *
from pygame import *
from vec2d import vec2d
from animation import Animation

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
        target.screen.blit(self.factory_ico, target.hud.all_coords[0])
        target.screen.blit(self.generator_ico, target.hud.all_coords[1])
        target.screen.blit(self.medbay_ico, target.hud.all_coords[2])
        target.screen.blit(self.outpost_ico, target.hud.all_coords[3])
        target.screen.blit(self.stockpile_ico, target.hud.all_coords[4])
        
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