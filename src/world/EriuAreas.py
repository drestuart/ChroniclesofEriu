'''
Created on Jun 26, 2014

@author: dstuart
'''

from AreaClass import SingleLevelArea, MultiLevelArea
import EriuLevel as EL
import EriuGame as G
import LevelClass as L
from randomChoice import weightedChoice

class EriuSingleLevelArea(SingleLevelArea):
    pass

class TownArea(EriuSingleLevelArea):

    def buildStartingLevel(self):
        newName = G.getPlaceName()
        newLevel = EL.EriuTownLevel(tilesWide = 3, tilesHigh = 3, area = self, name = newName, depth = 0)

        self.startingLevel = newLevel
        newLevel.buildLevel()
#         db.saveDB.save(self)

class EriuMultiLevelArea(MultiLevelArea):

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
            
            if plevel.depth < newLevel.depth:
                L.connectLevels(plevel, newLevel)
            else:
                L.connectLevels(newLevel, plevel)
            
#             db.saveDB.save(newLevel)
            
#         db.saveDB.save(self)

    def buildDungeon(self, numLevels):
        levelChances = {EL.EriuDungeonLevel : 7,
                        L.CaveLevel : 3}
        return self.buildLowerLevels(numLevels, levelChances)
    
    
    def buildCave(self, numLevels):
        levelChances = {L.CaveLevel : 10}
        return self.buildLowerLevels(numLevels, levelChances)
