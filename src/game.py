"""
Kevin Henderson 2019

"""
# IMPORTS
import pygame
from pygame.mixer import *
from pygame.font import *
from pygame.locals import *

import random
import os # for unixtime command

#from message import *
from player import *
from object import *


FLAGS = FULLSCREEN | DOUBLEBUF

WIDTH = 1280
HEIGHT = 720

LEVEL_WIDTH = 19200
LEVEL_HEIGHT = 10800

CAMERA_X = 100
CAMERA_Y = 100

MAXFPS = 30

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (1, 142, 214)

class Game():
    """ main game class, there should only ever be one instance """
    def __init__(self):
        # INIT
        pygame.init()
        #pygame.mixer.init()
        pygame.font.init()

        # MIXER start playing
        #pygame.mixer.music.load("../audio/1.mp3")
        #pygame.mixer.music.play()
        
        # CLOCK
        self.clock = pygame.time.Clock()
        self.ticks = 0
        self.running = True
        
        # SCREEN
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT),  FLAGS)
        pygame.display.set_caption('~ Heliocentrica ~')
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(black)
        
        # game state - 0 is for menu, 1 for level1 etc.
        self.state = 1
        
        self.scale = 2
        
        # object groups
        self.all_stars = pygame.sprite.Group()
        self.all_asteroids = pygame.sprite.Group()
        self.all_enemies = pygame.sprite.Group()
        
        self.planet_init()
        self.main_loop()
        
    def planet_init(self):

        for i in range(200):
            star = Object()
            star.surf = pygame.Surface((1, 1))
            colour = random.randint(0, 255)
            star.surf.fill((colour, colour, colour))
            self.all_stars.add(star)
            
        # init player
        self.player = Player()
        
        for i in range(2):
            asteroid= Planet("asteroid",  2, random.randint(2100, 2700),  3000)
            asteroid.label = ""
            asteroid.surf = pygame.transform.rotate(asteroid.surf,  random.randint(0, 359))
            scale = random.randint(1, 6)
            asteroid.surf = pygame.transform.scale(asteroid.surf, (int(asteroid.rect.width/scale), int(asteroid.rect.height/scale)))
            self.all_asteroids.add(asteroid)
        
        self.mercury = Planet("mercury",  18,  700,  100)
        
        self.moon = Planet("moon",  5,  350,  100)
        self.earth = Planet("earth",  25, 1500,  400)
        self.earth.all_orbit.add(self.moon)
        
        self.phobos = Planet("phobos",  3,  400,  10)
        self.deimos = Planet("deimos", 3,  600,  50)
        self.mars = Planet("mars",23,  1800,  500)
        self.mars.all_orbit.add(self.phobos)
        self.mars.all_orbit.add(self.deimos)
        
        self.io = Planet("io",  5,  600,  10)
        self.europa = Planet("europa", 5,  700,  30)
        self.callisto = Planet("callisto", 5,  500,  20)
        self.ganymede = Planet("ganymede", 5, 600,  50)
        self.jupiter = Planet("jupiter",17,  3000,  800)
        self.jupiter.all_orbit.add(self.io)
        self.jupiter.all_orbit.add(self.europa)
        self.jupiter.all_orbit.add(self.callisto)
        self.jupiter.all_orbit.add(self.ganymede)
        
        self.neptune = Planet("neptune", 28,  3900,  900)
        
        self.uranus = Planet("uranus",  30,  4500,  1000)
        
        self.pluto = Planet("pluto",  12,  5600,  1200)
  
        #TODO get rid of sun2
        self.sun2 = Planet("sun", 80,  0, 1)
        self.sun2.rect.centerx = 6000
        self.sun2.rect.centery = 3500
        self.sun = Planet("sun", 80,  0,  1)
        self.sun.rect.centerx = 6000
        self.sun.rect.centery = 3500
        self.sun.all_orbit.add(self.mercury)
        self.sun.all_orbit.add(self.earth)
        self.sun.all_orbit.add(self.mars)
        self.sun.all_orbit.add(self.jupiter)    
        self.sun.all_orbit.add(self.neptune)  
        self.sun.all_orbit.add(self.uranus)  
        self.sun.all_orbit.add(self.pluto)
        
        for asteroid in self.all_asteroids:
            self.sun.all_orbit.add(asteroid)             
    
    
        self.sun2.all_orbit.add(self.sun)
        
    def main_loop(self):
        """ main game loop runs until we set running = False """
        while self.running:
            
            self.events()
            self.update()
            self.tick()            
            
        # EXIT
        pygame.quit()
        quit()
        
    def events(self):
        """ resolves pygame event queue """
                
        # EVENT QUEUE
        for event in pygame.event.get():
            # KEYDOWN event
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                if event.key == K_0:
                    self.state = 0
                if event.key == K_1:
                    self.state = 1
                if event.key == K_3:
                    self.scale +=0.1
                if event.key == K_2:
                    if self.scale > 1: self.scale -= 0.1

            # QUIT event;
            elif event.type == QUIT:
                self.running = False
        # END EVENT QUEUE
        
    def render_menu(self):
        pass
        
    def update(self):
        """ updates and blits everything to the screen surface """
        global CAMERA_X,  CAMERA_Y
        # background
        self.screen.blit(self.background, (0, 0))
        
        if self.ticks % 15:
            pass
            #enemy = Planet("asteroid", 4500, 0, 0)
            #self.all_enemies.add(enemy)
            
        for enemy in self.all_enemies:
            enemy.updatePosition()
            enemy.renderTiny(self.screen,  CAMERA_X, CAMERA_Y, self.scale)
            enemy.renderTiny(self.screen,  CAMERA_X, CAMERA_Y, 10)
            enemy.calcGravity(self.sun2)
        
        self.sun2.update()
        
        self.player.calcGravity(self.sun2)
        self.player.detectCollision(self.sun2)
        
        if self.state == 1:
            pressed_keys = pygame.key.get_pressed()
            self.player.update(pressed_keys)
            self.sun2.renderTiny(self.screen,  CAMERA_X,  CAMERA_Y,  self.scale)
            self.player.renderTiny(self.screen,  CAMERA_X, CAMERA_Y,  self.scale)   

        else:
            self.sun2.renderTiny(self.screen,  0,  0,  10)
            self.player.renderTiny(self.screen,  0, 0,  10)
            blit_text( self.screen,  "MENU", 20,  white, WIDTH/2,  HEIGHT/2)
            blit_text( self.screen,  "<--- YOU ARE HERE", 16,  red, (self.player.rect.right / 10) + 10,  self.player.rect.y / 10,  -1)


        # stars
        for star in self.all_stars:
            self.screen.blit(star.surf, star.rect)    
            
        #self.sun2.render(self.screen,  CAMERA_X,  CAMERA_Y)
        #self.player.render(self.screen,  CAMERA_X, CAMERA_Y)
                   
                
        for entity in self.player.bullets:
            entity.update()
            entity.countdown-=1
            entity.render(self.screen,  CAMERA_X,  CAMERA_Y)
            if entity.deathTime > 10 or entity.countdown < -5:
                self.player.bullets.remove(entity)

        if (self.player.rect.left)  <  CAMERA_X + WIDTH * self.scale /4:  CAMERA_X =  self.player.rect.left - (WIDTH * self.scale /4)
        elif (self.player.rect.right ) >  CAMERA_X + WIDTH * self.scale * 3/4: CAMERA_X =  self.player.rect.right - (WIDTH * self.scale * 3/4)
        if (self.player.rect.top )  <  CAMERA_Y + HEIGHT* self.scale /4: CAMERA_Y =  self.player.rect.top - (HEIGHT* self.scale /4)
        elif (self.player.rect.bottom ) >  CAMERA_Y + HEIGHT* self.scale * 3/4: CAMERA_Y =  self.player.rect.bottom - (HEIGHT * self.scale * 3/4)
        

     
        # END UPDATE SPRITES

        # HUD
        # top left
        blit_text( self.screen,  str(self.player.rect.center[0]) + "x : " + str(self.player.rect.center[1]) + "y", 16,  white, 0,  0)
        blit_text( self.screen,  "camera: " + str(CAMERA_X) + "x " + str(CAMERA_Y) + " y", 20,  white, 0,  20)
        blit_text( self.screen,  "scale: " + str(self.scale), 20,  white, 0,  40)
        
        blit_text( self.screen,   str(self.player.alive),  16,  white, WIDTH - 50,  HEIGHT -50, 1)

        # bottom right
        fps = self.clock.get_fps()
        if int(fps) < MAXFPS:
            blit_text( self.screen,  str(int(fps)) + " fps",  16,  red, WIDTH - 5,  HEIGHT -16,  1 )
        else:
            blit_text( self.screen,   str(int(fps)) + " fps",  16,  white, WIDTH - 5,  HEIGHT -16, 1)
        # END HUD
        

        
    def tick(self):
        """ limits FPS """
        if self.state == 0:
            self.clock.tick(10)
        else:
            self.clock.tick(MAXFPS)
        self.ticks +=1
            
        # Update the display
        pygame.display.flip()
            
def blit_text(surface,  text, size,  colour,  x,  y,  allign = -1):
    """ simple function to blit text to a surface """
    font = pygame.font.Font('freesansbold.ttf',size)
    textSurface = font.render(str(text), False, colour)
    textSurface.set_alpha(100)
    textRect = textSurface.get_rect()
    if allign == -1:
        textRect.left = x
    elif allign == 1:
        textRect.right = x
    else:
        textRect.centerx = x
    textRect.top = y
    surface.blit(textSurface, textRect)
    

# execute game when file run
if __name__ == "__main__":
    game = Game()
