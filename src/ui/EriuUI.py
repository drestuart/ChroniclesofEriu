'''
Created on Oct 20, 2014

@author: dstuart
'''

from UIClass import UI
import pygame
import os.path

class EriuUI (UI):
    
    def __init__(self, **kwargs):
        super(EriuUI, self).__init__(**kwargs)
        
    def ShowLogo(self):
        # Show logo image
        logoPath = os.path.join("data", "img", "logo_kells.png")
        self.fadeInImage(logoPath, 2000, 30)
            
        # Wait a sec, then clear screen
        pygame.time.delay(1000)
        self.window.surface.fill((0,0,0))
        self.drawWindow()
    
    def MainMenu(self):
        pass
    
    