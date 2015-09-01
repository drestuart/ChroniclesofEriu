'''
Created on Mar 10, 2013

@author: dstu
'''

from pubsub import pub
from OptionClass import OptionType, Option
import Const as C
import delvelibConst as DC
import CreatureClass as Cr
import EriuAreas as A
import PlayerClass as P
import EriuUI as ui
import EriuWorldMap as W
import pygame
import mname
from EriuLevel import EmptyArena, PillarsArena, DoorArena, EriuTownLevel
import Game as G

defaultNames = 0

def getPlaceName():
    return game.placeNames.name()

def getMaleName():
    return game.maleNames.name()

def getFemaleName():
    return game.femaleNames.name()

class EriuGame(G.Game):

    def initialize(self, **kwargs):
        self.debugOptions = set()
        self.debug = kwargs.get('debug', False)

        if self.debug:
#             pub.subscribe(self.debugListener, 'event')
            
            showPaths = Option("showPaths", "Show Paths", OptionType.TOGGLE, True, trueText = "On", falseText = "Off")
            showCoords = Option("showCoords", "Show Coordinates", OptionType.TOGGLE, True, trueText = "On", falseText = "Off")
            anIntegerOption = Option("anInteger", "An integer", OptionType.INTEGER, 10, min = 0, max = 20)

            self.debugOptions = [showPaths, showCoords, anIntegerOption]

        if pygame.init() != (6,0):
            print "Error starting pygame"

        print "Loading name files"
        self.maleNames = mname.MName("male")
        self.femaleNames = mname.MName("female")
        self.placeNames = mname.MName("places")

        self.fontsize = kwargs.get('fontsize')
        self.font = kwargs.get("font", None)
        
        self.quests = []
        self.currentLevel = None

        seed = 1155272238
        self.setRandomSeed(seed)

    def start(self, **kwargs):
        self.initialize(**kwargs)
        G.ui = ui.EriuUI(font = self.font, fontsize = self.fontsize)

        G.ui.ShowLogo()

        # Main menu loop
        while True:
            menuOpt = G.ui.MainMenu()
            G.ui.clearWindow()
            menuOpt()

    def play(self):
        G.ui.gameLoop()
        # TODO:
#         db.saveDB.save(G.ui.getCurrentLevel())

    def worldMapTest(self):
        ''' Set up world map test '''
        self.worldMap = W.EriuWorldMap(width = C.WORLD_MAP_WIDTH, height = C.WORLD_MAP_HEIGHT, num_regions = C.NUM_REGIONS)
        self.worldMap.buildMap()

        self.player = P.Player()
        self.worldMap.placePlayer(self.player)

        self.openShelf()

        G.ui.setPlayer(self.player)
        G.setCurrentLevel(self.worldMap)

        self.play()

    def dungeonTest(self):
        ''' Set up dungeon test '''
        from EriuMapTileClass import Forest
        mt = Forest(3, 5)
        d = A.MultiLevelArea(name = u"The Dungeons of Dread")

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

        self.openShelf()

        G.ui.setPlayer(self.player)
        G.setCurrentLevel(d1)

        self.play()

    def townTest(self):
        name = getPlaceName()
        d = EriuTownLevel(tilesWide = 3, tilesHigh = 3, area = None, name = name, depth = 0)
        d.buildLevel()

        self.player = P.Player()
        d.placeCreatureAtRandom(self.player, False)

        self.openShelf()

        G.ui.setPlayer(self.player)
        G.setCurrentLevel(d)

        self.play()

    def arenaTest(self, arenaClass):
        d = arenaClass(depth = 0, width = DC.MAP_WIDTH, height = DC.MAP_HEIGHT)
        d.buildLevel()

        self.player = P.Player()
        d.placeCreatureAtRandom(self.player, False)

        orc1 = Cr.Orc()
        d.placeCreatureAtRandom(orc1)

#         orc2 = Cr.Orc()
#         d.placeCreatureAtRandom(orc2)

        self.openShelf()

        G.ui.setPlayer(self.player)
        G.setCurrentLevel(d)

        self.play()

    def emptyArenaTest(self):
        self.arenaTest(EmptyArena)

    def pillarsArenaTest(self):
        self.arenaTest(PillarsArena)

    def doorTest(self):
        self.arenaTest(DoorArena)
        
    def questTest(self, questType):
        self.worldMap = W.EriuWorldMap(width = C.WORLD_MAP_WIDTH, height = C.WORLD_MAP_HEIGHT, num_regions = C.NUM_REGIONS)
        self.worldMap.buildMap()

        self.player = P.Player()
        self.worldMap.placePlayer(self.player)

        self.openShelf()

        G.ui.setPlayer(self.player)
        G.setCurrentLevel(self.worldMap)

        # Add quest
        q = questType()

        self.play()

game = EriuGame()
G.game = game