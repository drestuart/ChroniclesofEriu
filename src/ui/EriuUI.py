'''
Created on Oct 20, 2014

@author: dstuart
'''

from __future__ import print_function

from UIClass import UI
import pygame
import os.path
from PanelClass import GameMenuWindow, EscapeMenuWindow
import Const as C
import EriuGame as G

class EriuUI (UI):
    
    def __init__(self, **kwargs):
        super(EriuUI, self).__init__(**kwargs)
        
    def ShowLogo(self):
        # Show coldbrew credit
        lines = ["coldbrew software", "presents"] 
        if not self.showCenteredText(lines, 3000):
            return
        
        self.clearWindow()
        
        # Show logo image
        logoPath = os.path.join("data", "img", "logo_kells.png")
        if self.fadeInImage(logoPath, 2000, 30):
            # Unless interrupted, wait a sec, then clear screen
            pygame.time.delay(1000)
            
        self.clearWindow()
    
    def MainMenu(self):
        menuOptions = [{"text" : "New Game", "enabled" : True, "function" : lambda: print("New Game")},
                       {"text" : "Load", "enabled" : True, "function" : lambda: print("Load")},
                       {"text" : "Functional Tests", "enabled" : True, "function" : self.tests},
                       {"text" : "Options", "enabled" : False},
                       {"text" : "About", "enabled" : False},
                       {"text" : "Quit", "enabled" : True, "function" : self.quit}]
        
        menu = GameMenuWindow(self, options = menuOptions, width = C.MENU_WIDTH, title = C.TITLE)

        return menu.getSingleChoice()
    
    def tests(self):
        
        tests = [{"text" : "Combat Arenas", "enabled" : True, "function" : self.arenas},
                 {"text" : "World Map", "enabled" : True, "function" : G.game.worldMapTest},
                 {"text" : "Dungeon", "enabled" : True, "function" : G.game.dungeonTest},
                 {"text" : "Town", "enabled" : True, "function" : G.game.townTest},
                 ]
        
        menu = GameMenuWindow(self, options = tests, width = C.MENU_WIDTH, title = "Tests")

        func = menu.getSingleChoice()
        self.clearScreen()
        func()
    
    def arenas(self):
        arenas = [{"text" : "Empty", "enabled" : True, "function" : G.game.emptyArenaTest},
                  {"text" : "Pillars", "enabled" : True, "function" : G.game.pillarsArenaTest},
                  {"text" : "Single Door", "enabled" : True, "function" : G.game.doorTest},
                  ]
        
        menu = GameMenuWindow(self, options = arenas, width = C.MENU_WIDTH, title = "Arenas")

        func = menu.getSingleChoice()
        self.clearScreen()
        func()
        
    def gameMenu(self):
        options = [{"text" : "Quit", "enabled" : True, "function" : self.quit}]
        
        menu = EscapeMenuWindow(self, options=options, width=C.MENU_WIDTH, title = '')
        
        func = menu.getSingleChoice()
        self.clearScreen()
        if func:
            func()