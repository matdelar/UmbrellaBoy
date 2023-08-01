import math
import pygame
from scripts.umbrella import Umbrella
from scripts.particle import ParticleEmitter

class Player:
    def __init__(self,screen,position):
        self.screen = screen
        self.pos = [position[0],position[1]]
        self.size = [48,48]
        self.rect = pygame.Rect(self.pos,self.size)
        self.jump_force = -7
        self.is_grounded = False
        self.speed = 5
        self.movement = [float(0),float(0)]
        self.slow_fall = 1.5
        self.dash_speed = 30
        self.dash = [0,0]

        self.umbrella = Umbrella(self.screen)
        self.gravity = 1/60 * 2
        self.gravity_actual_speed = 0
        self.gravity_max_speed = self.gravity *4
        self.jump_momentum = 0
        self.is_flipped = False
        self.grounded_lock = True

        self.sprites = [
            pygame.transform.scale_by(pygame.image.load('assets/image/entities/player.png').convert_alpha(),3)
        ]
        self.audio = pygame.mixer.Sound("assets/audio/entities/player/jump.wav")

        self.jump_particle = ParticleEmitter(self.screen)
        self.jump_particle.set(
            amount =20,
            color = (240,240,240),
            size=(6,6),
            maxRange=(96),
            loop = 0,
            speed = "(random.random()-0.5)*6,(random.random())*-3"
        )

        self.buffer_frames = 12
        self.buffer_counter = 0

        self.coyote_frames = 12
        self.coyote_counter = 0
        


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

    def update(self,tiles,mobs):
        newRect, collision_sides = self.move_collide(self.movement,tiles)
        self.buffer_counter -= 1
        self.coyote_counter -= 1

        
        ###Basic Movement
        keys = pygame.key.get_pressed()
        hspd = keys[pygame.K_d]-keys[pygame.K_a]
        dynamic_gravity_limit = self.gravity_max_speed/(1+((45 <self.umbrella.get_angle()<135 and self.umbrella.isOpen))*3)
        dynamic_gravity = self.gravity/(1+((45 <self.umbrella.get_angle()<135 and self.umbrella.isOpen))*3)

        

        
        self.is_flipped = hspd<0 if hspd != 0 else self.is_flipped

        self.gravity_actual_speed += dynamic_gravity  if self.gravity_actual_speed + dynamic_gravity < dynamic_gravity_limit else dynamic_gravity_limit
        self.jump_momentum += self.gravity  if self.jump_momentum + self.gravity < 0  else 0

        self.movement[0] = hspd*self.speed + self.dash[0]
        self.movement[1] = self.gravity_actual_speed + self.jump_momentum + self.dash[1]

        self.is_grounded = collision_sides['bottom']

        if collision_sides['bottom'] or collision_sides['top']:
            self.movement[1] = 0
            self.gravity_actual_speed = 0
            self.jump_momentum = 0
    
        
        if self.is_grounded and (keys[pygame.K_w]):
            self.jump_momentum = self.jump_force
            self.audio.play()

        if self.is_grounded and self.grounded_lock and self.jump_momentum<0:
            self.grounded_lock = False
            self.jump_particle.set(loop=1,fixedPos=(self.rect.centerx,self.rect.bottom))
        else:
            self.grounded_lock = True
        
        
        mov_angle = math.atan2(self.movement[1],self.movement[0])

        dynamic_speed = str(math.cos(mov_angle)*2)+","+str(math.sin(mov_angle)*2)
        self.jump_particle.update(dynamic_speed)
        self.jump_particle.draw((0,0))


        #mobs hit update:
        moblist = [mob for mob in mobs]
        projectlist = [bullet for bullet in self.umbrella.get_projectiles()]

        for p in projectlist:
            for m in moblist:
                if p.get_rect().colliderect(m.get_rect()):
                    m.deal_damage(p.get_angle(),10)



        ##Umbrella update #Dash Simple
        if self.umbrella.collide_surface(tiles) and self.umbrella.isOpen and self.dash[0]==0:
            self.dash = [-math.cos(math.radians(self.umbrella.get_angle()))*self.dash_speed,math.sin(math.radians(self.umbrella.get_angle()))*self.dash_speed]

        self.dash[0] /= 1.1
        self.dash[1] /= 1.1

        if math.fabs(self.dash[0])<=self.dash_speed/800:
            self.dash[0]=0
            self.dash[1]=0
        
        ##Umbrella update #Shotgun

        if not self.umbrella.collide_surface(tiles) and self.umbrella.isOpen and pygame.mouse.get_pressed()[2]:
            self.umbrella.shot()


        self.umbrella.update(newRect.topleft)

        self.pos = newRect.topleft
        self.rect.update(newRect)
        


    def draw(self):
        new_image = pygame.transform.flip(self.sprites[0], self.is_flipped, False)
        self.screen.blit(new_image,self.pos)