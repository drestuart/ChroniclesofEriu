'''
Created on Jun 26, 2014

@author: dstuart
'''

import random

from pubsub import pub

from AreaClass import Area
import Game as G
import LevelClass as L
import database as db
from randomChoice import weightedChoice
from LevelClass import DungeonLevel


class SingleLevelArea(Area):
    __mapper_args__ = {'polymorphic_identity': 'single_level_area'}
    defaultWidth = 100
    defaultHeight = 80

    def generateLevels(self, numLevels = 1):
        terrainType = self.getTerrainType()
        newLevel = terrainType(area = self, depth = 0, width = self.defaultWidth, height = self.defaultHeight)
        self.startingLevel = newLevel
        newLevel.buildLevel()
        db.saveDB.save(self)


class TownArea(Area):
    __mapper_args__ = {'polymorphic_identity': 'town_area'}

    def generateLevels(self, numLevels = 1):
        newName = G.getPlaceName()
        newLevel = L.TownLevel(area = self, name = newName, depth = 0, 
                               cellsWide = random.randint(2, 4), cellsHigh = random.randint(2, 4))
        self.startingLevel = newLevel
        newLevel.buildLevel()
        db.saveDB.save(self)



class MultiLevelArea(Area):
    
    defaultWidth = 100
    defaultHeight = 80
    
    __mapper_args__ = {'polymorphic_identity': 'multi_level_area'}

    def generateLevels(self, numLevels = 1):
        # Build levels
        for i in range(numLevels):
            newDepth = i
            newName = self.name + " " + str(i + 1)
            
            if self.withTown and newDepth == 0:
                newName = G.getPlaceName()
                newLevel = L.TownLevel(3, 3, area = self, name = newName, depth = newDepth)
                self.startingLevel = newLevel
                
            elif newDepth == 0:
                terrainType = self.getTerrainType()
                newLevel = terrainType(area = self, depth = 0, width = self.defaultWidth, height = self.defaultHeight)
                self.startingLevel = newLevel
                
            else:
#                 newLevelType = weightedChoice(self.levelChances)
                # TODO get cave levels back in here!
                newLevelType = DungeonLevel
                newLevel = newLevelType(4, 4, area = self, name = newName, depth = newDepth)
            
            newLevel.buildLevel()
            
            
            # TODO chance to generate a branch or loop
            
            # Connect levels
            if i > 0:
                plevel = self.levels[i-1]
                
                # The depth values should be off by only 1. TODO better validation
                
                if plevel.depth < newLevel.depth:
                    L.connectLevels(plevel, newLevel)
                else:
                    L.connectLevels(newLevel, plevel)
            
#             self.levels.append(newLevel)
            db.saveDB.save(newLevel)
            
        db.saveDB.save(self)

        # TODO Connect top level to world map


class DungeonArea(MultiLevelArea):
    
    levelChances = {L.DungeonLevel : 7,
                    L.CaveLevel : 3}
    defaultWidth = 100
    defaultHeight = 80
    
    __mapper_args__ = {'polymorphic_identity': 'dungeon_area'}
    
    









class CaveArea(MultiLevelArea):
    
    levelChances = {L.CaveLevel : 10}
    defaultWidth = 100
    defaultHeight = 80
    
    __mapper_args__ = {'polymorphic_identity': 'cave_area'}

    






