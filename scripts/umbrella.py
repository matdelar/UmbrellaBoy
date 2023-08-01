import random
import pygame, math
from scripts.particle import ParticleEmitter

class Umbrella:
    def __init__(self,screen):
        self.screen = screen
        self.pos = [0,0]
        self.angle = 0
        self.distance = 48
        self.sprites = []
        self.sprites.append(pygame.transform.scale_by(pygame.image.load("assets/image/items/umbrella1.png ").convert_alpha(),3))
        self.sprites.append(pygame.transform.scale_by(pygame.image.load("assets/image/items/umbrella2.png ").convert_alpha(),3))
        self.sprites.append(pygame.transform.scale_by(pygame.image.load("assets/image/items/umbrella3.png ").convert_alpha(),3))
        self.isOpen = False
        self.rect = pygame.Rect(self.pos,(48,48))
        self.tip_rect = pygame.Rect(self.pos,(12,12))

        self.frameCount = 0
        self.currentSprite = 0
        
        self.projectiles = []
        self.mlock = False
        self.audio = pygame.mixer.Sound("assets/audio/items/umbrellaOpen.wav")
        self.audio_shot = pygame.mixer.Sound("assets/audio/items/shot.wav")
        self.closeDelay = 30

        self.particle = ParticleEmitter(self.screen)
        self.particle.set(
            color=(233,200,150),
            loop=0,
            speed="0,0",
            maxRange= 128,
            amount=10,
            size=(8,8)
            )
        
        self.current_mode = 'shotgun'
        
        self.shot_angle = 0
        self.shot_delay = 15
        self.shot_tick = 0
    
    def update(self,playerPos):
        x,y = pygame.mouse.get_pos()
        self.angle = math.atan2(playerPos[1]-y+24,x-playerPos[0]-24)
        self.shot_tick -=1

        self.tip_rect.center = math.cos(self.angle)*64+playerPos[0]+24,-math.sin(self.angle)*64+playerPos[1]+24
        self.tip_rect.update(self.tip_rect)


        if pygame.mouse.get_pressed()[0] and not self.mlock:
            self.isOpen = True
            self.mlock = True
            self.audio.play()

        elif not pygame.mouse.get_pressed()[0]:
            self.mlock = False
            self.isOpen = False
        



        new_pos = [playerPos[0]+24+math.cos(self.angle)*48,playerPos[1]+24-math.sin(self.angle)*self.distance]
        rot_sprite, new_rect = self.rot_center(self.sprites[self.currentSprite],math.degrees(self.angle)+90,new_pos[0],new_pos[1])

        if self.isOpen and self.currentSprite < 2:
            self.frameCount += 1
            if self.frameCount == 3:
                self.currentSprite += 1 if self.currentSprite < 2 else True
                self.frameCount = 0
        elif not self.isOpen and self.currentSprite > 0:
            self.frameCount += 1
            if self.frameCount == 3:
                self.currentSprite -= 1 if self.currentSprite > 0  else True
                self.frameCount = 0
        
        for p in self.projectiles:
            result = p.update()
            if result == 'bullet_dead':
                self.projectiles.pop(self.projectiles.index(p))
        
        self.pos = self.rect.topleft


        self.rect.update(new_rect)
        self.screen.blit(rot_sprite,self.rect)

        dynamic_speed = "math.cos("+str(self.shot_angle)+"+ ((random.random()-0.5)*(math.pi/2)))*6,-math.sin("+str(self.shot_angle)+"+ ((random.random()-0.5)*(math.pi/2)))*6"

        self.particle.update(dynamic_speed)
        self.particle.draw(self.tip_rect.center)


        down_hand = self.tip_rect.x-math.cos(self.get_angle(True))*16+3, self.tip_rect.y+math.sin(self.get_angle(True))*16+3
        upper_hand = self.tip_rect.x-math.cos(self.get_angle(True))*40+3, self.tip_rect.y+math.sin(self.get_angle(True))*40+3

        pygame.draw.rect(self.screen,(255,0,255),(upper_hand,(6,6)),1)
        pygame.draw.rect(self.screen,(255,0,0),(down_hand,(6,6)),1)
    
    def get_angle(self,isRad=False):
        return  self.angle if isRad else math.degrees(self.angle )
    
    def rot_center(self,image, angle, x, y):
    
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect
    
    def collide_surface(self,tiles):
        for tile in tiles:
            if self.tip_rect.colliderect(tile.get_rect()):
                return True
        
        return False
    
    def shot_bullets(self,tiles):
        if len(self.projectiles) == 0 and not self.collide_surface(tiles):
            self.shot_angle = self.get_angle(True)
            self.particle.set(loop=1,
                fixedPos=self.rect.center
            )
            self.audio_shot.play()

            for i in range(5):
                rand_angle = self.angle - (math.pi/24)+(i*math.pi/60)
                self.projectiles.append(Bullets(self.screen,rand_angle,self.tip_rect.center))
    
    def shot_arrow(self,tiles):
        return
        if len(self.projectiles) < 5 and not self.collide_surface(tiles) and self.shot_tick<=0:
            self.shot_tick = 6
            self.shot_angle = self.get_angle(True)
            self.particle.set(loop=1,
                fixedPos=self.rect.center
            )
            self.audio_shot.play()
            self.projectiles.append(Arrow(self.screen,self.angle,self.tip_rect.center,13))
    
    def get_projectiles(self):
        return self.projectiles

class Bullets:
    def __init__(self,screen,angle,pos):
        self.screen = screen
        self.angle = angle
        self.pos = pos
        self.speed = 20
        self.speed = [math.cos(self.angle)*self.speed,-math.sin(self.angle)*self.speed]
        self.lifeTime = 60
        self.rect = pygame.Rect(self.pos,(6,6))
        self.trail = ParticleEmitter(self.screen)
        self.trail.set(
            loop = -1,
            size = (9,9),
            color = (200,180,0),
            maxRange = (64),#
            speed = str(-self.speed[0])+"*(i/20),"+str(-self.speed[1])+"*(i/20)",
            amount = 20
        )
    
    def update(self):
        self.lifeTime -=1
        self.pos = self.pos[0]+self.speed[0],  self.pos[1]+self.speed[1]

        self.rect.update(self.pos,(6,6))
        self.trail.update()
        self.trail.draw(self.pos)

        pygame.draw.rect(self.screen,(255,255,0),self.rect,1)

        if self.lifeTime == 0:
            return 'bullet_dead'
    
    def get_rect(self):
        return self.rect
    
    def get_angle(self):
        return [math.cos(self.angle),-math.sin(self.angle)]

class Glove:
    def __init__(self,screen):
        pass