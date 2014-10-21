'''
Created on Oct 20, 2014

@author: dstuart
'''

from UIClass import UI
import pygame
import os.path
import Const as C

class EriuUI (UI):
    
    def __init__(self, **kwargs):
        super(EriuUI, self).__init__(**kwargs)
        
    def ShowLogo(self):
        loadTime = 2000. #ms
        alphaMax = 255
        alphaSteps = 30
        fadeInDelay = int(loadTime/alphaSteps)
        
        # Load and scale the logo image
        image = pygame.image.load(os.path.join("data", "img", "logo_kells.png")).convert()
        imageWidth, imageHeight = image.get_width(), image.get_height()
        imageRatio = float(imageHeight)/imageWidth
        
        windowWidth, windowHeight = self.window.pixelsize
        
        newWidth = int(windowWidth*.9)
        newHeight = int(newWidth*imageRatio)
        
        image = pygame.transform.scale(image, (newWidth, newHeight))
        
        # Logo postioning -- centered
        logox, logoy = ((windowWidth - newWidth)/2, (windowHeight - newHeight)/2)
        
        # Fade in logo
        for i in range(alphaSteps):
            self.window.surface.fill((0,0,0))
            
            alpha = i*alphaMax/alphaSteps
            image.set_alpha(alpha)
            
            self.window.surface.blit(image, (logox, logoy))
            self.drawWindow()
            pygame.time.delay(fadeInDelay)
            
        # Clear
        pygame.time.delay(1000)
        self.window.surface.fill((0,0,0))
        self.drawWindow()
    
    def MainMenu(self):
        pass
    
    