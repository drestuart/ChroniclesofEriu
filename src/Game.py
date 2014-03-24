'''
Created on Mar 10, 2013

@author: dstu
'''

from pubsub import pub
import Const as C
import CreatureClass as Cr
import DungeonClass as D
import LevelClass as L
import PlayerClass as P
import UIClass as ui
import EriuWorldMap as W
import database as db
import pygame
import random

game = 0
myUI = 0

defaultNames = 0

def message(msg):
    game.message(msg)

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
        
        db.saveDB.start(True)
        
        self.fontsize = kwargs.get('fontsize')
        self.font = kwargs.get("font", None)
    
        seed = 1155272238
        print seed
        random.seed(seed)
        
        self.worldMapTest()
#         self.dungeonTest()
        
        
    def worldMapTest(self):
        
        worldMap = W.EriuWorldMap(width = C.WORLD_MAP_WIDTH, height = C.WORLD_MAP_HEIGHT, num_regions = 8)
        worldMap.buildMap()
        
        player = P.Player()
        worldMap.placePlayer(player)
        db.saveDB.save(worldMap)
        
        global myUI
        myUI = ui.UI(level = worldMap, player = player, font = self.font, fontsize = self.fontsize)
    
    def dungeonTest(self):
        
        d = D.Dungeon(name = "The Dungeons of Dread", startingDepth = 0, withTown = True)
        d.generateLevels(4)
          
        d1 = d.getLevels()[1]
         
        player = P.Player()
#         d1.placeCreatureAtRandom(player)
        d1.placeOnUpStair(player)
        
        orc1 = Cr.Orc()
        d1.placeCreatureAtRandom(orc1)
         
        orc2 = Cr.Orc()
        d1.placeCreatureAtRandom(orc2)
        
        db.saveDB.save(d)
        
        global myUI
        myUI = ui.UI(level = d1, player = player, font = self.font, fontsize = self.fontsize)

        
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



