import pygame
import math
from scripts.particle import *
from scripts.ui import *

class Rock_DragonFly:
    def __init__(self,screen,pos):
        self.screen = screen
        self.pos = pos
        self.head_pos = self.pos
        self.body_pos = self.pos
        self.tail_pos = self.pos
        self.health = 100
        self.sprites = [
            pygame.transform.scale_by(pygame.image.load("assets/image/entities/rock_dragon_fly1.png").convert_alpha(),3),
            pygame.transform.scale_by(pygame.image.load("assets/image/entities/rock_dragon_fly2.png").convert_alpha(),3),
            pygame.transform.scale_by(pygame.image.load("assets/image/entities/rock_dragon_fly3.png").convert_alpha(),3),
            pygame.transform.scale_by(pygame.image.load("assets/image/entities/rock_dragon_fly4.png").convert_alpha(),3)
        ]
        self.off_tick = 0
        self.is_flipped = False
        self.rect = pygame.Rect(self.pos,(24,24))
        self.hit_speed =[0,0]
        self.gravity = 1/10
        self.gravity_actual_speed = 0
        self.gravity_limit = 10
        self.corpse_tick = 60
        self.particle_hit = ParticleEmitter(screen)
        self.particle_hit.set(
            loop = 0,
            amount = 10,
            color=(92,112,129),
            size=(9,9),
            maxRange=(128)
        )
        self.health_bar = Healthbar(self.screen,(self.pos[0],self.pos[1]+24),(18,6),self.health,(0,0,0),(255,0,0),)
        self.angle = 0

        self.patrol_center_x = pos[0]  # Define o centro da rota de patrulha na metade da tela horizontalmente
        self.patrol_center_y = pos[1]  # Define o centro da rota de patrulha na metade da tela verticalmente
        self.patrol_radius_x = 100  # Define o raio do eixo X da rota de patrulha
        self.patrol_radius_y = 50 
        
    
    def update(self):
        if self.health <= 0:
            self.dead_update()
        else: 
            self.angle += 0.05  # Ajuste esse valor para controlar a velocidade da rotação elíptica
            x = self.patrol_center_x + self.patrol_radius_x * math.cos(self.angle)
            y = self.patrol_center_y + self.patrol_radius_y * math.sin(self.angle)

            hspd = 1 if x >= self.pos[0] else -1  # Define a direção do flip horizontal

            self.pos = x, y
            ###
            self.off_tick += 1/6

            self.is_flipped = hspd > 0 if hspd !=0 else self.is_flipped

            self.pos =  self.pos[0],self.pos[1]-math.sin(self.off_tick)



            self.head_pos =  self.head_pos[0]-(self.head_pos[0]-(self.pos[0]-(24-self.is_flipped*48)))*0.25,math.sin(self.off_tick)*1+self.head_pos[1]-(self.head_pos[1]-(self.pos[1]-3))*0.5
            self.body_pos =  self.body_pos[0]-(self.body_pos[0]-(self.pos[0]+(24-self.is_flipped*48)))*0.25,math.sin(self.off_tick)*2+self.body_pos[1]-(self.body_pos[1]-(self.pos[1]))*0.5
            self.tail_pos =  self.tail_pos[0]-(self.tail_pos[0]-(self.pos[0]+(48-self.is_flipped*96)))*0.25,math.sin(self.off_tick)*3+self.tail_pos[1]-(self.tail_pos[1]-(self.pos[1]))*0.25

            self.rect.update(self.pos,(24,24))

            self.particle_hit.draw()


            dynamic_hit = str(self.hit_speed[0])+"*(random.random())*(math.pi/2)*2,"+str(self.hit_speed[1])+"*(random.random())*(math.pi/2)*2"
            self.particle_hit.update(dynamic_hit)
            self.health_bar.update((self.pos[0],self.pos[1]+24))
        
        self.draw()
        if self.corpse_tick == 0:
            return 'dead'
        
    def dead_update(self):
        self.corpse_tick -= 1
        self.gravity_actual_speed = self.gravity_actual_speed+self.gravity if  self.gravity_actual_speed+self.gravity <self.gravity_limit else self.gravity_limit
        self.pos =       self.pos[0]     +self.hit_speed[0]*1.1,self.pos[1]     +self.hit_speed[1]*1.1+self.gravity_actual_speed
        self.head_pos =  self.head_pos[0]+self.hit_speed[0]*1.0,self.head_pos[1]+self.hit_speed[1]*1.0+self.gravity_actual_speed
        self.body_pos =  self.body_pos[0]+self.hit_speed[0]*1.2,self.body_pos[1]+self.hit_speed[1]*1.2+self.gravity_actual_speed
        self.tail_pos =  self.tail_pos[0]+self.hit_speed[0]*1.3,self.tail_pos[1]+self.hit_speed[1]*1.3+self.gravity_actual_speed

    def get_rect(self):
        return self.rect
    
    def draw(self):
        
        self.screen.blit(pygame.transform.flip(self.sprites[0],self.is_flipped,False),self.head_pos)
        self.screen.blit(pygame.transform.flip(self.sprites[1],self.is_flipped,False),self.pos)
        self.screen.blit(pygame.transform.flip(self.sprites[2],self.is_flipped,False),self.body_pos)
        self.screen.blit(pygame.transform.flip(self.sprites[3],self.is_flipped,False),self.tail_pos)

    def deal_damage(self,hitAngle,damage=0):
        self.particle_hit.set(
            loop=1,
            fixedPos=self.rect.center)
        self.health -= damage
        x,y = hitAngle
        self.hit_speed = [x*5,y*5]
        self.health_bar.set_value(self.health)
class Sheep:
    def __init__(self,screen,pos):
        self.screen = screen
        self.pos = pos
        self.health = 10
        self.sprites = [
            pygame.transform.scale_by(pygame.image.load("assets/image/entities/sheep.png").convert_alpha(),3)
        ]
        self.rect = pygame.Rect(self.pos,(48,48))


    def update(self):
        self.screen.blit(self.sprites[0],self.pos)
    

    def get_hit_list(self,tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile.get_rect()):
                hit_list.append(tile.get_rect())
        
        return hit_list
    
    def move_collide(self,movement,tiles):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        self.rect.x += movement[0]
        hit_list = self.get_hit_list(tiles)
        for tile in hit_list:
            if movement[0] > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                self.rect.left = tile.right
                collision_types['left'] = True

        self.rect.y += movement[1]
        hit_list = self.get_hit_list(tiles)
        for tile in hit_list:
            if movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True
        return self.rect, collision_types

    def get_rect(self):
        return self.rect