import pygame
from object import *

class Player(Planet):
    """ Player class adds additional functions like player keyboard events """
    def __init__(self):
        super(Player, self).__init__("ship",  10, 0, 0)
        
        self.maxVel = 24
        
        self.rect.x = 4000
        self.rect.y = 3000
        
        self.bullets = pygame.sprite.Group()

    def update(self,  pressed_keys):
        """ updates player specific functions and calls basic update class """
        # thrusters
        self.surfOG = pygame.image.load("../images/ship0.png").convert_alpha()
        if pressed_keys[K_UP]:      
            self.velY += -3
            self.surfOG = pygame.image.load("../images/ship.png").convert_alpha()
        if pressed_keys[K_DOWN]: 
            self.velY += 3
            self.surfOG = pygame.image.load("../images/ship.png").convert_alpha()
        if pressed_keys[K_LEFT]:   
            self.velX += -3
            self.surfOG = pygame.image.load("../images/ship.png").convert_alpha()
        if pressed_keys[K_RIGHT]: 
            self.velX += 3
            self.surfOG = pygame.image.load("../images/ship.png").convert_alpha()
        
        rotation = self.getPolar(pygame.Rect(self.rect.centerx + self.velX* 10,  self.rect.centery + self.velY* 10,  1,  1))[0] * 180 / math.pi
        self.surf = pygame.transform.rotate(self.surfOG,  -(rotation - 45))
        self.rect = self.surf.get_rect(center=self.rect.center)
        
        if pressed_keys[K_SPACE]:
            self.shoot()
            
        if pressed_keys[K_DELETE]:
            self.rect.x = random.randint(5000, 5000)
            self.rect.y = random.randint(2500, 2500)
            
        if self.alive == False:
            self.surf = pygame.image.load("../images/shipX.png").convert_alpha()
        
        self.updatePosition()
        


            
            
    def shoot(self):
        b = Object()
        b.rect.x = self.rect.centerx
        b.rect.y = self.rect.centery
        b.maxVel = self.maxVel*1.5
        b.velX = self.velX*1.5
        b.velY = self.velY*1.5
        b.width = 2
        b.height = 2
        self.bullets.add(b)
        
            
class Bullet(Object):
        def __init__(self):
            pass    
