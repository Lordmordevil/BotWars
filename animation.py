import glob, sys
import pygame

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
   