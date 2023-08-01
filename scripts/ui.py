import pygame

class CheckBox:
    def __init__(self,screen,pos,size):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.is_checked = False
        self.is_hover = False
        self.rect = pygame.Rect(self.pos,self.size)
        self.insideRect = pygame.Rect(self.pos[0]+6,self.pos[1]+6,self.size[0]-12,self.size[1]-12)
        self.mlock = False

    def draw(self):
        pygame.draw.rect(self.screen,(255,255,255),self.rect,3)
        if self.is_checked:
            pygame.draw.rect(self.screen,(255,255,255),self.insideRect)
    
    def update(self):
        self.is_hover = self.rect.collidepoint(pygame.mouse.get_pos())

        if self.is_hover and pygame.mouse.get_pressed()[0] and not self.mlock:
            self.mlock = True
            self.is_checked = not self.is_checked
        elif not pygame.mouse.get_pressed()[0]:
            self.mlock = False

class Text:
    def __init__(self,screen,pos,text,size) -> None:
        self.pos = pos
        self.screen = screen
        self.text = text
        self.font = pygame.font.Font(None,size)
        self.render = self.font.render(self.text,True,(255,255,255))

    def draw(self):
        self.screen.blit(self.render,self.pos)    

class Healthbar:
    def __init__(self,screen,pos,size,maxValue,bg_color,main_color):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.max_value = maxValue
        self.value = maxValue
        self.bg_color = bg_color
        self.main_color = main_color
    
    def update(self,newPos=None):
        if newPos != None:
            self.pos = newPos
        pygame.draw.rect(self.screen,self.bg_color,(self.pos,self.size))
        value_size = (self.value/self.max_value) * self.size[0],self.size[1]
        pygame.draw.rect(self.screen,self.main_color,(self.pos,value_size))

    def set_value(self,newValue):
        self.value = newValue

    def get_value(self):
        return self.value        


class Cursor:
    def __init__(self,screen):
        self.screen = screen
        self.sprites = [
            pygame.transform.scale_by(pygame.image.load("assets/image/ui/mouse1.png").convert_alpha(),3),
            pygame.transform.scale_by(pygame.image.load("assets/image/ui/mouse2.png").convert_alpha(),3)
        ]

    
    def update(self):
        x,y = pygame.mouse.get_pos()
        x -= 9
        y -= 9
        self.screen.blit(self.sprites[pygame.mouse.get_pressed()[2]],(x,y))


class WheelSelector:
    def __init__(self,screen):
        self.screen = screen
        self.pos = self.screen.get_width()/2,self.screen.get_height()/2