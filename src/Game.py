'''
Created on Mar 10, 2013

@author: dstu
'''

from pubsub import pub
import Const as C
import delvelibConst as DC
import CreatureClass as Cr
import EriuAreas as A
import PlayerClass as P
import EriuUI as ui
import EriuWorldMap as W
import database as db
import pygame
import random
import mname
from EriuLevel import EmptyArena, PillarsArena

defaultNames = 0

def message(msg):
    game.message(msg)
    
def getPlaceName():
    return game.placeNames.name()

def getMaleName():
    return game.maleNames.name()

def getFemaleName():
    return game.femaleNames.name()

class Game(object):
    
    fontsize = None

    def initialize(self, **kwargs):
        self.debug = kwargs.get('debug', False)
        
        if self.debug:
            pub.subscribe(self.debugListener, 'event')
                
        if pygame.init() != (6,0):
            print "Error starting pygame"
            
        print "Loading name files"
        self.maleNames = mname.MName("male")
        self.femaleNames = mname.MName("female")
        self.placeNames = mname.MName("places")
        
        db.saveDB.start(True)
        
        self.fontsize = kwargs.get('fontsize')
        self.font = kwargs.get("font", None)
    
        seed = 1155272238
        print seed
        random.seed(seed)
        
#         self.worldMapTest()
#         self.dungeonTest()
        self.start()
        
    def start(self):
        self.myUI = ui.EriuUI(font = self.font, fontsize = self.fontsize)
        
        self.myUI.ShowLogo()
        
        # Main menu loop
        while True:
            menuOpt = self.myUI.MainMenu()
            self.myUI.clearWindow()
            menuOpt()
        
#         self.worldMapTest()
        
    def worldMapTest(self):
        ''' Set up world map test '''
        worldMap = W.EriuWorldMap(width = C.WORLD_MAP_WIDTH, height = C.WORLD_MAP_HEIGHT, num_regions = C.NUM_REGIONS)
        worldMap.buildMap()
        
        self.player = P.Player()
        worldMap.placePlayer(self.player)
        db.saveDB.save(worldMap)
        
        self.myUI.setPlayer(self.player)
        self.myUI.setCurrentLevel(worldMap)
        
        self.play()
    
    def dungeonTest(self):
        ''' Set up dungeon test '''
        from EriuMapTileClass import Forest
        mt = Forest(3, 5)
        d = A.MultiLevelArea(name = "The Dungeons of Dread")
        
        mt.setConnectedArea(d)
        
        d.buildStartingLevel()
        d.buildDungeon(4)
          
        d1 = d.getLevels()[0]
         
        self.player = P.Player()
        d1.placeCreatureAtEntrance(self.player)
        
#         orc1 = Cr.Orc()
#         d1.placeCreatureAtRandom(orc1)
#          
#         orc2 = Cr.Orc()
#         d1.placeCreatureAtRandom(orc2)
        
        db.saveDB.save(d)
        
        self.myUI.setPlayer(self.player)
        self.myUI.setCurrentLevel(d1)
        
        self.play()
    
    def arenaTest(self, arenaClass):
        d = arenaClass(depth = 0, width = DC.MAP_WIDTH, height = DC.MAP_HEIGHT)
        d.buildLevel()
        
        self.player = P.Player()
        d.placeCreatureAtRandom(self.player, False)
        
        db.saveDB.save(d)
        
        self.myUI.setPlayer(self.player)
        self.myUI.setCurrentLevel(d)
        
        self.play()
        
    def emptyArenaTest(self):
        self.arenaTest(EmptyArena)
        
    def pillarsArenaTest(self):
        self.arenaTest(PillarsArena)
        
    def debugListener(self,topic=pub.AUTO_TOPIC, **args):
        print 'Got an event of type: ' + topic.getName()
        print '  with data: ' + str(args)
        
    def play(self):
        self.myUI.gameLoop()
        db.saveDB.save(self.myUI.getCurrentLevel())
        
    def message(self, msg):
        if self.debug: print msg
        self.myUI.message(msg)
        
    def getPlayer(self):
        return self.player
    

game = Game()

