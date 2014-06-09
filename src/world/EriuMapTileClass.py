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
    color = colorForest
    __mapper_args__ = {'polymorphic_identity': 'forest'}
    def __init__(self, *args, **kwargs):
        super(Forest, self).__init__(*args, baseSymbol = self.symb, **kwargs)
 
class Plain(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'plain'}
    color = colorPlain
    def __init__(self, *args, **kwargs):
        super(Plain, self).__init__(*args, baseSymbol = '.', **kwargs)
         
class Field(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'field'}
    color = colorField
    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, baseSymbol = '.', **kwargs)
 
class Mountain(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'mountain'}
    color = colorMountain
    def __init__(self, *args, **kwargs):
        super(Mountain, self).__init__(*args, baseSymbol = '^', **kwargs)
 
class Ocean(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'ocean'}
    color = colorOcean
    waterTile = True
    def __init__(self, *args, **kwargs):
        super(Ocean, self).__init__(*args, baseSymbol = symbols.doubleWavy, **kwargs)
 
class River(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'river'}
    waterTile = True
    color = colorRiver
    def __init__(self, *args, **kwargs):
        super(River, self).__init__(*args, baseSymbol = '~', **kwargs)
 
class Bridge(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'bridge'}
    color = colorWood
    def __init__(self, *args, **kwargs):
        super(Bridge, self).__init__(*args, baseSymbol = '^', **kwargs)
 
class Town(EriuMapTile):
    symb = symbols.townShape
    connectedLevelType = TownLevel
    color = colorWood
    
    __mapper_args__ = {'polymorphic_identity': 'town'}
     
    def __init__(self, *args, **kwargs):
        super(Town, self).__init__(*args, baseSymbol = self.symb, **kwargs)
        self.name = kwargs.get('name') or Game.getPlaceName()
         
    def generateConnectedLevel(self):
        self.connectedLevel = self.connectedLevelType(cellsWide = random.randint(2, 4), cellsHigh = random.randint(2, 4))
        self.connectedLevel.buildLevel()

class Capital(Town):
    
    __mapper_args__ = {'polymorphic_identity': 'capital'}

    def __init__(self, *args, **kwargs):
        super(Capital, self).__init__(*args, **kwargs)
