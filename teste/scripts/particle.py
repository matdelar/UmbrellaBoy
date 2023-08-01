import pygame
import random
import math

class ParticleEmitter:
    def __init__(self,screen) -> None:
        self.screen = screen
        self.particle = {
            'pos':[0,0],
            'size' : [5,5],
            'speed' : "[0,0]", #use eval so expressions can be passed as parameters
            'color':(255,0,0),
            'amount' : 20,
            'maxRange' : 48,
            'shape' : "rect",
            'loop' : 0,
            'fixedPos':None

        }
        self.posList = [[0]*2 for _ in range(self.particle['amount'])]
        self.sizeList = [self.particle['size'] for _ in range(self.particle['amount'])]
        self.loopList = [self.particle['loop'] for _ in range(self.particle['amount'])]
        

    def draw(self,pos=(0,0)):
        if self.particle['fixedPos'] != None:
            pos = self.particle['fixedPos']
        for i in range(self.particle['amount']):
            if self.loopList[i]==0:
                continue


            if self.particle['shape'] == "circle":
                pygame.draw.circle(self.screen, (128+random.random()*128,32+random.random()*32,random.random()*16), [self.posList[i][0]+pos[0],self.posList[i][1]+pos[1]], self.particle['size'][0])
            elif self.particle['shape'] == "rect":
                pygame.draw.rect(self.screen, self.particle['color'], ([self.posList[i][0]+pos[0],self.posList[i][1]+pos[1]],self.sizeList[i]))
    
    def set(self,**kwargs):
        for arg in kwargs:
            self.particle[arg] = kwargs[arg]
            if arg == 'amount':
                self.posList = [[0]*2 for _ in range(self.particle['amount'])]
                self.sizeList = [self.particle['size'] for _ in range(self.particle['amount'])]
            elif arg == 'loop':
                self.loopList = [kwargs[arg] for _ in range(self.particle['amount'])]
    
    def update(self,dynamicSpeed="[0,0]"):
        for i in range(self.particle['amount']):
            if self.loopList[i] == 0:
                continue    

            distance = self.calculate_distance(self.posList[i])
            newSize = self.calculate_size(distance)
            self.sizeList[i] = newSize,newSize
            sx,sy = eval(self.particle['speed'])
            dsx,dsy = eval(dynamicSpeed)
            newPos = self.posList[i][0]+sx+dsx,  self.posList[i][1]+sy+dsy
            if distance > self.particle['maxRange']-1 and self.loopList[i]!=0:
                self.loopList[i] -=1
                self.sizeList[i] = self.particle['size']
                newPos = [0,0]

            self.posList[i] = newPos
    
    def calculate_size(self,distance):
        x = distance
        a = float(self.particle['maxRange'])

        y = (-(x*x*x*x)/(a*a*a*a)+1)*self.particle['size'][0]


        return y
    
    def calculate_distance(self,particle_pos):
        x = particle_pos[0]
        y = particle_pos[1]
        distance = math.hypot(x,y)
    
        return distance
