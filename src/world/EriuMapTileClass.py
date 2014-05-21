'''
Created on May 14, 2014

@author: dstuart
'''

import random

from sqlalchemy.types import String
from sqlalchemy.schema import Column

from LevelClass import WildernessLevel, ForestLevel, TownLevel
import MapTileClass as M
from colors import colorForest, colorPlain, colorMountain, colorField, colorOcean, colorRiver, colorWood
# import database as db
import symbols
import KingdomClass as K
import Game

# Base = db.saveDB.getDeclarativeBase()

class EriuMapTile(M.MapTile, K.hasKingdom):
    
    def __init__(self, x, y, **kwargs):
        super(EriuMapTile, self).__init__(x, y, **kwargs)
        self.kingdomName = kwargs.get('kingdomName', None)
        self.kingdom = K.getKingdomByName(self.kingdomName)
    
    connectedLevelType = WildernessLevel
    kingdomName = Column(String)

    
    __mapper_args__ = {'polymorphic_identity': 'eriu_maptile'}
    
    def getBackgroundColor(self):
        if self.kingdom:
            return self.kingdom.color
        return super(EriuMapTile, self).getBackgroundColor()
        
 
class Forest(EriuMapTile):
    symb = symbols.lowerTau
    connectedLevelType = ForestLevel
    __mapper_args__ = {'polymorphic_identity': 'forest'}
    def __init__(self, *args, **kwargs):
        super(Forest, self).__init__(*args, baseSymbol = self.symb, color = colorForest, **kwargs)
 
class Plain(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'plain'}
    def __init__(self, *args, **kwargs):
        super(Plain, self).__init__(*args, baseSymbol = '.', color = colorPlain, **kwargs)
         
class Field(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'field'}
    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, baseSymbol = '.', color = colorField, **kwargs)
 
class Mountain(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'mountain'}
    def __init__(self, *args, **kwargs):
        super(Mountain, self).__init__(*args, baseSymbol = '^', color = colorMountain, **kwargs)
 
class Ocean(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'ocean'}
    waterTile = True
    def __init__(self, *args, **kwargs):
        super(Ocean, self).__init__(*args, baseSymbol = symbols.doubleWavy, color = colorOcean, **kwargs)
 
class River(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'river'}
    waterTile = True
    def __init__(self, *args, **kwargs):
        super(River, self).__init__(*args, baseSymbol = '~', color = colorRiver, **kwargs)
 
class Bridge(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'bridge'}
    def __init__(self, *args, **kwargs):
        super(Bridge, self).__init__(*args, baseSymbol = '^', color = colorWood, **kwargs)
 
class Town(EriuMapTile):
    symb = symbols.townShape
    connectedLevelType = TownLevel
     
    __mapper_args__ = {'polymorphic_identity': 'town'}
     
    def __init__(self, *args, **kwargs):
        super(Town, self).__init__(*args, baseSymbol = self.symb, color = colorWood, **kwargs)
        self.name = Game.getPlaceName()
         
    def generateConnectedLevel(self):
        self.connectedLevel = self.connectedLevelType(cellsWide = random.randint(2, 4), cellsHigh = random.randint(2, 4))
        self.connectedLevel.buildLevel()


