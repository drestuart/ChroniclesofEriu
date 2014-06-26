'''
Created on Jun 26, 2014

@author: dstuart
'''

from AreaClass import Area
from randomChoice import weightedChoice
from pubsub import pub
import Game as G

import database as db
import LevelClass as L

class TownArea(Area):
    __mapper_args__ = {'polymorphic_identity': 'town_area'}

    def generateLevels(self, numLevels = 1):
        newName = G.getPlaceName()
#         cellsWide = random.randint(2, 4), cellsHigh = random.randint(2, 4)
        newLevel = L.TownLevel(name = newName, depth = 0, cellsWide = 3, cellsHigh = 3)
        self.startingLevel = newLevel
        db.saveDB.save(self)








class DungeonArea(Area):
    
    levelChances = {L.DungeonLevel : 7,
                    L.CaveLevel : 3}
    defaultWidth = 100
    defaultHeight = 80
    
    __mapper_args__ = {'polymorphic_identity': 'dungeon_area'}
    
    def generateLevels(self, numLevels = 1):
        # Build levels
        for i in range(numLevels):
            newDepth = i
            newName = self.name + " " + str(i + 1)
            
            if self.withTown and newDepth == 0:
                newName = G.getPlaceName()
                newLevel = L.TownLevel(name = newName, depth = newDepth, cellsWide = 2, cellsHigh = 2)
                self.startingLevel = newLevel
                
            elif newDepth == 0:
                levelType = self.
                self.startingLevel = newLevel
                
            else:
                newLevelClass = weightedChoice(self.levelChances)
                newLevel = newLevelClass(name = newName, depth = newDepth, width = self.defaultWidth,
                                         height = self.defaultHeight) # Do something more interesting with the dimensions999 here
            
            newLevel.buildLevel()
            
            
            # TODO chance to generate a branch or loop
            
            # Connect levels
            if i > 0:
                plevel = self.levels[-1]
                
                # The depth values should be off by only 1. TODO better validation
                
                if plevel.depth < newLevel.depth:
                    L.connectLevels(plevel, newLevel)
                else:
                    L.connectLevels(newLevel, plevel)
            
            self.levels.append(newLevel)
            db.saveDB.save(newLevel)
            
        db.saveDB.save(self)

        # TODO Connect top level to world map









class CaveArea(Area):
    
    __mapper_args__ = {'polymorphic_identity': 'cave_area'}
    
    levelChances = {L.CaveLevel : 10}
    defaultWidth = 100
    defaultHeight = 80
    
    def generateLevels(self, numLevels = 1):
        # Build levels
        for i in range(numLevels):
            newDepth = i
            newName = self.name + " " + str(i + 1)
            
            if self.withTown and newDepth == 0:
                newLevel = L.TownLevel(name = newName, depth = newDepth, cellsWide = 2, cellsHigh = 2)
                
            else:
                newLevelClass = weightedChoice(self.levelChances)
                newLevel = newLevelClass(name = newName, depth = newDepth, width = self.defaultWidth,
                                         height = self.defaultHeight) # Do something more interesting with the dimensions999 here
            
            newLevel.buildLevel()
            
            if newDepth == 0:
                self.startingLevel = newLevel
            
            # TODO chance to generate a branch or loop
            
            # Connect levels
            if i > 0:
                plevel = self.levels[-1]
                
                # The depth values should be off by only 1. TODO better validation
                
                if plevel.depth < newLevel.depth:
                    L.connectLevels(plevel, newLevel)
                else:
                    L.connectLevels(newLevel, plevel)
            
            self.levels.append(newLevel)
            db.saveDB.save(newLevel)
            
        db.saveDB.save(self)

        # TODO Connect top level to world map










