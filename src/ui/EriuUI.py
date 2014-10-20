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
        image = pygame.image.load(os.path.join("data", "img", "logo_kells.png")).convert()
        background=pygame.Surface((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        background.fill((0, 0, 0))
        
        for i in range (225):
            print i
            background.fill((0,0,0))    
            image.set_alpha(i)
            self.window.surface.blit(background, background.get_rect())
            self.window.surface.blit(image,(0,0))
            pygame.display.flip()
            self.drawWindow()
            pygame.time.delay(20)
        
    
    def MainMenu(self):
        pass
    
    