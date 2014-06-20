'''
Created on May 14, 2014

@author: dstuart
'''

import random

from sqlalchemy.types import String
from sqlalchemy.schema import Column

from LevelClass import WildernessLevel, ForestLevel, TownLevel
import MapTileClass as M
from colors import colorForest, colorPlain, colorMountain, colorField, colorOcean, colorRiver, colorLake, colorWood
import symbols
import KingdomClass as K
import Game

class EriuMapTile(M.MapTile, K.hasKingdom):
    
    def __init__(self, x, y, **kwargs):
        super(EriuMapTile, self).__init__(x, y, **kwargs)
        self.kingdomName = kwargs.get('kingdomName', None)
        self.kingdom = K.getKingdomByName(self.kingdomName)
    
    connectedLevelType = WildernessLevel
    kingdomName = Column(String)
    description = "eriutile"
    
    __mapper_args__ = {'polymorphic_identity': 'eriu_maptile'}
    
    def getBackgroundColor(self):
        if self.kingdom:
            return self.kingdom.color
        return super(EriuMapTile, self).getBackgroundColor()
        
 
class Forest(EriuMapTile):
    symb = symbols.lowerTau
    connectedLevelType = ForestLevel
    color = colorForest
    description = "forest"
    
    __mapper_args__ = {'polymorphic_identity': 'forest'}
    
    def __init__(self, *args, **kwargs):
        super(Forest, self).__init__(*args, baseSymbol = self.symb, **kwargs)
 
class Plain(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'plain'}
    color = colorPlain
    description = "plains"
    
    def __init__(self, *args, **kwargs):
        super(Plain, self).__init__(*args, baseSymbol = '.', **kwargs)
         
class Field(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'field'}
    color = colorField
    description = "field"
    
    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, baseSymbol = '.', **kwargs)
 
class Mountain(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'mountain'}
    color = colorMountain
    description = "mountain"
    
    def __init__(self, *args, **kwargs):
        super(Mountain, self).__init__(*args, baseSymbol = '^', **kwargs)
 
class Ocean(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'ocean'}
    color = colorOcean
    waterTile = True
    description = "ocean"
    
    def __init__(self, *args, **kwargs):
        super(Ocean, self).__init__(*args, baseSymbol = symbols.doubleWavy, **kwargs)
 
class River(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'river'}
    waterTile = True
    color = colorRiver
    description = "river"
    
    def __init__(self, *args, **kwargs):
        super(River, self).__init__(*args, baseSymbol = '~', **kwargs)

class Lake(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'lake'}
    waterTile = True
    color = colorLake
    description = "lake"
    
    def __init__(self, *args, **kwargs):
        super(Lake, self).__init__(*args, baseSymbol = '~', **kwargs) 

class Bridge(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': 'bridge'}
    color = colorWood
    description = "bridge"
    
    def __init__(self, *args, **kwargs):
        super(Bridge, self).__init__(*args, baseSymbol = '^', **kwargs)
 
class Town(EriuMapTile):
    symb = symbols.townShape
    connectedLevelType = TownLevel
    color = colorWood
    description = "town"
    
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
