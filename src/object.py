import pygame
import random
import math
from game import *

class Object(pygame.sprite.Sprite,  Game):
    """ everything that moves is a member of the Object class """
    def __init__(self):
        super(Object, self).__init__()

        self.alive = True
        self.deathTime = 0
        
        self.r = 255
        self.g = 0
        self.b = 0

        self.radius = random.randint(2, 3)
        
        self.maxVel = 12
        
        self.posX = random.randint(0, 1280)
        self.posY = random.randint(0, 720)
        self.posZ = 0
        self.velX = random.randint(-12, 12)
        self.velY = random.randint(-12, 12)
        self.velZ = 0
        self.accX = 0
        self.accY = 0
        self.accZ = 0
        
        self.pullX = 0
        self.pullY = 0
        self.pullZ = 0
                
        self.mass = 34
        
        self.surf = pygame.Surface((self.radius*2 , self.radius*2 ))
        self.surf.fill((self.r, self.g, self.b))
        self.surfOG = self.surf.copy()
        
        self.rect = self.surf.get_rect()   
        self.rect.x = self.posX
        self.rect.y = self.posY
        
       
    def renderRect(self,  surface,  CAMERA_X,  CAMERA_Y,SCALE):
        """ renders object to surface only if within screen bounds """
        
        if self.rect.right  - CAMERA_X> 0 and self.rect.left - CAMERA_X < WIDTH:
            if self.rect.bottom - CAMERA_Y>0 and self.rect.top - CAMERA_Y< HEIGHT:     
                if self.alive == True:
                    pygame.draw.circle(surface, (self.r, self.g, self.b), (int(self.rect.x - CAMERA_X), int(self.rect.y - CAMERA_Y)) , int(self.radius), 0)
                    pygame.draw.circle(surface, (self.r, self.g, self.b), (int(self.rect.x/SCALE), int(self.rect.y/SCALE)) , int(self.radius), 0)
            
    def updatePosition(self):
        """ updates position of object """
                   
        self.accX = self.pullX
        self.accY = self.pullY
        
        self.velX += self.accX
        self.velY += self.accY
        
        # limit velocity
        if self.velX < -self.maxVel:   self.velX = -self.maxVel 
        elif self.velX > self.maxVel: self.velX = self.maxVel 
        if self.velY < -self.maxVel:   self.velY = -self.maxVel 
        elif self.velY > self.maxVel: self.velY = self.maxVel 
        
        self.rect.x += self.velX
        self.rect.y += self.velY
        
        self.posX = self.rect.centerx
        self.posY = self.rect.centery
        
        # reset pull forces
        self.pullX = 0
        self.pullY = 0
                    
        
    def detectCollision(self,  planet):
        """
        hit = pygame.sprite.spritecollideany(self,  group)
        if hit:
            self.alive = False
            hit.alive = False
        """
        # circlular collision detection between objects and larger planets
        if self.getPolar(planet.rect)[1] < planet.radius + self.radius:
            self.alive = False
        for item in planet.all_orbit:
            self.detectCollision(item)
    
    def getCartesian(self,  theta,  radius):
        """" takes theta and radius values, and returns x and y components (x, y) """
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        return (x,  y)
        
    def getPolar(self,  rect2):
        """ takes a Rect, and returns polar coordinates (theta, radius) relative to given rect """
        distX = self.rect.center[0] - rect2.center[0]
        distY = self.rect.center[1] - rect2.center[1]
        
        radius = math.sqrt(distX*distX + distY *distY )
        theta = math.atan2(distY, distX)
        
        return (theta,  radius)
        
    def calcGravity(self,  object2):
        """ takes an object and adds gravity pull force  """
        polar = self.getPolar(object2.rect)
        if polar[1] != 0:
            self.pullX += -self.mass * object2.mass / polar[1] * math.cos(polar[0])
            self.pullY += -self.mass * object2.mass/ polar[1] * math.sin(polar[0])
            
        for planet in object2.all_orbit:
            self.calcGravity(planet)

class Planet(Object):
        def __init__(self,  file,  mass, orbit,  period):
            super(Planet, self).__init__()

            self.file = file
            self.label = file
            self.surf = pygame.image.load("../images/" + file + ".png").convert_alpha()
            self.surfOG = self.surf.copy()
            self.rect = self.surf.get_rect()   
            self.rect.centerx = self.posX
            self.rect.centery = self.posY
            self.radius = self.rect.width/2
            
            self.maxVel = 3
            
            self.posZ = 0
            
            self.all_orbit = pygame.sprite.Group()
            
            self.mass = mass
            self.orbit = orbit
            self.period = period
            self.theta = random.randint(0, 6000)
            self.rotation = 45
            
            self.rect = self.surf.get_rect()   
            self.rect.x = self.posX
            self.rect.y = self.posY

        def update(self):
            """ updates position of object """
            
            # rotate original surface
            #self.surf = pygame.transform.rotate(self.surfOG,  self.rotation)
            self.rect = self.surf.get_rect(center=self.rect.center)
            self.rotation -=2
                
            for item in self.all_orbit:
                item.resolveOrbits()
                item.update()
                
        def render(self,  surface,  CAMERA_X,  CAMERA_Y):
            """ renders object to surface only if within screen bounds """
            
            if self.rect.right  - CAMERA_X> 0 and self.rect.left - CAMERA_X < WIDTH:
                if self.rect.bottom - CAMERA_Y>0 and self.rect.top - CAMERA_Y< HEIGHT:     
                    surface.blit(self.surf,  (self.rect.x - CAMERA_X, self.rect.y - CAMERA_Y))
            for item in self.all_orbit:
                item.render(surface,  CAMERA_X,  CAMERA_Y)
                
        def renderTiny(self,  surface,  CAMERA_X,  CAMERA_Y,  SCALE):
            """ renders object to surface only if within screen bounds """
            if self.rect.right  - CAMERA_X > 0 and self.rect.left - CAMERA_X < WIDTH * SCALE:
                if self.rect.bottom - CAMERA_Y>0 and self.rect.top - CAMERA_Y< HEIGHT * SCALE:                
                    tinySurf = pygame.transform.scale(self.surf, (int(self.rect.width/SCALE), int(self.rect.height/SCALE)))
                    surface.blit(tinySurf,  ((self.rect.x - CAMERA_X )/SCALE, (self.rect.y - CAMERA_Y )/SCALE))
                    blit_text( surface,   self.label,  12,  white, int((self.rect.centerx - CAMERA_X)/SCALE),  int((self.rect.y - CAMERA_Y - 28)/SCALE),  0)
                    self.radius = tinySurf.get_rect().width/2

                    
            for item in self.all_orbit:
                item.renderTiny(surface,  CAMERA_X,  CAMERA_Y,  SCALE)

            
        def resolveOrbits(self):
            for planet in self.all_orbit:
                planet.theta -= math.pi / planet.period
                if planet.theta > math.pi:
                    planet.theta -= 2 *math.pi
                if planet.theta < -math.pi:
                    planet.theta += 2 *math.pi
                planet.rect.centerx = self.rect.centerx + planet.orbit* math.cos(planet.theta) 
                planet.rect.centery = self.rect.centery + planet.orbit * math.sin(planet.theta) 
