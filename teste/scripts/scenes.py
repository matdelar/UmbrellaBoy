import pygame
from scripts.player import Player
from scripts.tiles import *
from scripts.ui import *
from scripts.enemies import *

class Demo:
    def __init__(self,screen):
        self.init_modules()
        self.screen = screen
        self.map = []
        for x in range(80):
            for y in range(1):
                self.map.append(CollTile(self.screen,(x*48,y*48+630),(48,48)))


        self.player = Player(self.screen,(100,100))

        self.checks = [
            CheckBox(self.screen,(10,100),(30,30)),
            CheckBox(self.screen,(10,150),(30,30)),
            CheckBox(self.screen,(10,200),(30,30))
        ]
        self.texts = [
            Text(self.screen,(10,50),"MODE:",20),
            Text(self.screen,(60,100),"Shotgun",20),
            Text(self.screen,(60,150),"Harpoon",20),
            Text(self.screen,(60,200),"Default",20),
            ]

        self.mobs = [
            Rock_DragonFly(self.screen,(300,300))
        ]
        
    
    def update(self):
        for tile in self.map:
            tile.draw()
        
        for check in self.checks:
            check.update()
            check.draw()

        for text in self.texts:
            text.draw()
        
        for i,m in enumerate(self.mobs):
            result = m.update()
            if result == 'dead':
                self.mobs.pop(i)
                

        self.player.update(self.map,self.mobs)
        self.player.draw()

        pygame.draw.rect(self.screen,(67,47,36),(0,678,1280,48))
    
    def init_modules(self):
        pygame.font.init()
        pygame.mixer.init()