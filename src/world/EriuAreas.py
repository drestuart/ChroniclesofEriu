'''
Created on Jun 26, 2014

@author: dstuart
'''

from AreaClass import Area
import EriuLevel as EL
import EriuGame as G
import LevelClass as L
import database as db
from randomChoice import weightedChoice

class SingleLevelArea(Area):
    __mapper_args__ = {'polymorphic_identity': 'single_level_area'}
    defaultWidth = 100
    defaultHeight = 80

    def buildStartingLevel(self):
        terrainType = self.getTerrainType()
        newLevel = terrainType(area = self, depth = 0, width = self.defaultWidth, height = self.defaultHeight)
        self.startingLevel = newLevel
        newLevel.buildLevel()
        db.saveDB.save(self)
        
    def convertToMultilevelArea(self):
        newArea = MultiLevelArea(name=self.name)
        mt = self.getMapTile()
        
        self.levels[0].placeDungeonEntrance()
        newArea.levels = self.levels
        self.levels = []
        
        mt.setConnectedArea(newArea)
        del self
        db.saveDB.save(newArea)
        
        return newArea


class TownArea(Area):
    __mapper_args__ = {'polymorphic_identity': 'town_area'}

    def buildStartingLevel(self):
        newName = G.getPlaceName()
        newLevel = EL.EriuTownLevel(tilesWide = 3, tilesHigh = 3, area = self, name = newName, depth = 0)

        self.startingLevel = newLevel
        newLevel.buildLevel()
        db.saveDB.save(self)



class MultiLevelArea(Area):
    
    defaultWidth = 100
    defaultHeight = 80
    hasDungeon = True
    
    __mapper_args__ = {'polymorphic_identity': 'multi_level_area'}
    
    
    def buildStartingLevel(self):
        newDepth = 0
        
        terrainType = self.getTerrainType()
        newLevel = terrainType(area = self, depth = newDepth, width = self.defaultWidth, height = self.defaultHeight)
        self.startingLevel = newLevel
        
        newLevel.buildLevel()
        newLevel.placeDungeonEntrance()
    
    def buildLowerLevels(self, numLevels, levelChances):
        # Build levels
        for i in range(numLevels):
            newDepth = i + 1
            newName = self.name + " " + str(i + 1)
            
            newLevelType = weightedChoice(levelChances)
            newLevel = newLevelType(width = self.defaultWidth, height = self.defaultHeight, tilesWide = 4, tilesHigh = 4, 
                                    area = self, name = newName, depth = newDepth)
            
            newLevel.buildLevel()

            # TODO chance to generate a branch or loop
            
            # Connect levels
            plevel = self.levels[i-1]
            
            # The depth values should be different by only 1. TODO better validation
            
            if plevel.depth < newLevel.depth:
                L.connectLevels(plevel, newLevel)
            else:
                L.connectLevels(newLevel, plevel)
            
#             self.levels.append(newLevel)
            db.saveDB.save(newLevel)
            
        db.saveDB.save(self)

        # TODO Connect top level to world map (Done?)


    def buildDungeon(self, numLevels):
        levelChances = {EL.EriuDungeonLevel : 7,
                        L.CaveLevel : 3}
        return self.buildLowerLevels(numLevels, levelChances)
    
    
    def buildCave(self, numLevels):
        levelChances = {L.CaveLevel : 10}
        return self.buildLowerLevels(numLevels, levelChances)


