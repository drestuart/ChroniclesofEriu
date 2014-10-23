'''
Created on Oct 20, 2014

@author: dstuart
'''

from __future__ import print_function

from UIClass import UI
import pygame
import os.path
from PanelClass import GameMenuPanel
import Const as C

class EriuUI (UI):
    
    def __init__(self, **kwargs):
        super(EriuUI, self).__init__(**kwargs)
        
    def ShowLogo(self):
        # Show coldbrew credit
        lines = ["coldbrew games", "presents"] 
        self.showCenteredText(lines, 3000)
        self.clearWindow()
        
        # Show logo image
        logoPath = os.path.join("data", "img", "logo_kells.png")
        self.fadeInImage(logoPath, 2000, 30)
            
        # Wait a sec, then clear screen
        pygame.time.delay(1000)
        self.clearWindow()
    
    def MainMenu(self):
        menuOptions = [{"text" : "New Game", "enabled" : True, "function" : lambda: print("New Game")},
                       {"text" : "Load", "enabled" : True, "function" : lambda: print("Load")},
                       {"text" : "Nope", "enabled" : False},
                       {"text" : "Quit", "enabled" : True, "function" : lambda: print("Quit")}]
        
        menu = GameMenuPanel(self.window, options = menuOptions, width = C.MENU_WIDTH, title = C.TITLE)

        return menu.getSingleChoice()
    
    