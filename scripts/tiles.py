import pygame
from scripts.particle import *

class CollTile:
    #Tile used to represent collision
    def __init__(self,screen,pos,size):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.sprite = pygame.transform.scale_by(pygame.image.load("assets/image/tiles/grass.png").convert_alpha(),3)
        self.rect = pygame.Rect(pos,size)

    def draw(self):
        self.screen.blit(self.sprite,self.pos)
    
    def get_rect(self):
        return self.rect

