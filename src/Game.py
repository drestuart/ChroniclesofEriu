'''
Created on Mar 10, 2013

@author: dstu
'''

from pubsub import pub
import Const as C
import CreatureClass as Cr
import EriuAreas as A
import PlayerClass as P
import EriuUI as ui
import EriuWorldMap as W
import database as db
import pygame
import random
import mname

game = 0
myUI = 0

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

    def __init__(self, **kwargs):
        global game
        game = self
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
        global myUI
        myUI = ui.EriuUI(font = self.font, fontsize = self.fontsize)
        
        myUI.ShowLogo()
        myUI.MainMenu()
        
        self.worldMapTest()
        
    def worldMapTest(self):
        ''' Set up world map test '''
        worldMap = W.EriuWorldMap(width = C.WORLD_MAP_WIDTH, height = C.WORLD_MAP_HEIGHT, num_regions = C.NUM_REGIONS)
        worldMap.buildMap()
        
        player = P.Player()
        worldMap.placePlayer(player)
        db.saveDB.save(worldMap)
        
        global myUI
        myUI.setPlayer(player)
        myUI.setCurrentLevel(worldMap)
    
    def dungeonTest(self):
        ''' Set up dungeon test '''
        from EriuMapTileClass import Forest
        mt = Forest(3, 5)
        d = A.MultiLevelArea(name = "The Dungeons of Dread")
        
        mt.setConnectedArea(d)
        
        d.buildStartingLevel()
        d.buildDungeon(4)
          
        d1 = d.getLevels()[0]
         
        player = P.Player()
        d1.placeCreatureAtEntrance(player)
        
#         orc1 = Cr.Orc()
#         d1.placeCreatureAtRandom(orc1)
#          
#         orc2 = Cr.Orc()
#         d1.placeCreatureAtRandom(orc2)
        
        db.saveDB.save(d)
        
        global myUI
        myUI.setPlayer(player)
        myUI.setCurrentLevel(d1)
        
    def debugListener(self,topic=pub.AUTO_TOPIC, **args):
        print 'Got an event of type: ' + topic.getName()
        print '  with data: ' + str(args)
        
    def play(self):
        global myUI
        myUI.gameLoop()
        db.saveDB.save(myUI.getCurrentLevel())
        
    def message(self, msg):
        global myUI
        if self.debug: print msg
        myUI.message(msg)



