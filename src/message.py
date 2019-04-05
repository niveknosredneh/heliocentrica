import pygame

class Message():
    """ Message class which holds text data """
    def __init__(self, message,  size, colour,  x,  y, allign, timeout=0):
        self.alive = True
        self.fadeIn = False
        self.fadeOut = False
        if timeout == 0:
            self.timeout = 0
        else:
            self.timeout = pygame.time.get_ticks() + timeout
            self.fadeOut = True
        
        self.r = colour[0]
        self.g = colour[1]
        self.b = colour[2]
        
        if self.fadeIn == True:
            self.alpha = 0
        else: 
            self.alpha = 255
        
        self.message = message
        
        self.font = pygame.font.Font('freesansbold.ttf',size)
        self.textSurface = self.font.render(str(message), False, (self.r, self.g, self.b))
        self.rect = self.textSurface.get_rect()
        
        self.textSurface.set_alpha(self.alpha)
        
        self.rect.top = y
        if allign == -1: # allign left
            self.rect.left = x
        elif allign == 1: # allign right
            self.rect.right = x
        elif allign == 0: # allign centre
            self.rect.centerx = x
            
    def changeColour(self,  r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.textSurface = self.font.render(str(self.message), False, (self.r, self.g, self.b))
        
    def setAA(self):
        """ sets anti aliasing of text on, must be set off for transparency """
        self.textSurface = self.font.render(str(self.message), True, (self.r, self.g, self.b))
        
    def render(self,  surface):
        """ blits text to screen """
        if self.fadeIn == True and self.alpha < 255:
            self.alpha+=5
            self.textSurface.set_alpha(self.alpha)
        elif self.fadeIn == True and self.alpha == 255:
            self.fadeIn == False
            
        elif self.fadeOut == True and pygame.time.get_ticks() > self.timeout:
            if self.alpha > 0:    
                self.alpha-=5
                self.textSurface.set_alpha(self.alpha)
            else:
                self.alive = False
        elif pygame.time.get_ticks() > self.timeout:
            self.alive = False
        
        surface.blit(self.textSurface, self.rect)
