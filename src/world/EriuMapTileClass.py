# coding: utf_8
'''
Created on May 14, 2014

@author: dstuart
'''

import random

from sqlalchemy.types import Unicode
from sqlalchemy.schema import Column

from EriuLevel import EriuWildernessLevel, ForestLevel, EriuTownLevel
import MapTileClass as M
from colors import colorForest, colorPlain, colorMountain, colorField, colorOcean, colorShallowOcean, colorRiver, colorLake, colorWood
import symbols
import KingdomClass as K
import EriuGame as G
from EriuAreas import EriuSingleLevelArea, TownArea

class EriuMapTile(M.MapTile, K.hasKingdom):
    
    def __init__(self, x, y, **kwargs):
        super(EriuMapTile, self).__init__(x, y, **kwargs)
        self.kingdomName = kwargs.get('kingdomName', None)
        self.kingdom = K.getKingdomByName(self.kingdomName)
    
    terrainType = EriuWildernessLevel
    areaType = EriuSingleLevelArea
    kingdomName = Column(Unicode)
    description = u"eriutile"
    
    __mapper_args__ = {'polymorphic_identity': u'eriu_maptile'}
    
    def getBackgroundColor(self):
        if self.__dict__.get('kingdom'):
            return self.kingdom.color
        return super(EriuMapTile, self).getBackgroundColor()
        
 
class Forest(EriuMapTile):
    symb = symbols.lowerTau
    terrainType = ForestLevel
    color = colorForest
    description = u"forest"
    
    __mapper_args__ = {'polymorphic_identity': u'forest'}
    
    def __init__(self, *args, **kwargs):
        super(Forest, self).__init__(*args, baseSymbol = self.symb, **kwargs)
 
class Plain(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': u'plain'}
    color = colorPlain
    description = u"plains"
    
    def __init__(self, *args, **kwargs):
        super(Plain, self).__init__(*args, baseSymbol = u'.', **kwargs)
         
class Field(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': u'field'}
    color = colorField
    description = u"field"
    
    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, baseSymbol = u'.', **kwargs)
 
class Mountain(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': u'mountain'}
    color = colorMountain
    description = u"mountain"
    
    def __init__(self, *args, **kwargs):
        super(Mountain, self).__init__(*args, baseSymbol = u'^', **kwargs)
        
class Water(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': u'water'}
    waterTile = True
    
    def __init__(self, *args, **kwargs):
        super(Water, self).__init__(*args, **kwargs)
 
class Ocean(Water):
    __mapper_args__ = {'polymorphic_identity': u'ocean'}
    color = colorOcean
    description = u"ocean"
    
    def __init__(self, *args, **kwargs):
        super(Ocean, self).__init__(*args, baseSymbol = symbols.doubleWavy, **kwargs)

class ShallowOcean(Ocean):
    __mapper_args__ = {'polymorphic_identity': u'shallow ocean'}
    color = colorShallowOcean
    
    def __init__(self, *args, **kwargs):
        super(ShallowOcean, self).__init__(*args, **kwargs)

class River(Water):
    __mapper_args__ = {'polymorphic_identity': u'river'}
    color = colorRiver
    description = u"river"
    
    def __init__(self, *args, **kwargs):
        super(River, self).__init__(*args, baseSymbol = u'~', **kwargs)

class Lake(Water):
    __mapper_args__ = {'polymorphic_identity': u'lake'}
    color = colorLake
    description = u"lake"
    
    def __init__(self, *args, **kwargs):
        super(Lake, self).__init__(*args, baseSymbol = u'~', **kwargs) 

class Bridge(EriuMapTile):
    __mapper_args__ = {'polymorphic_identity': u'bridge'}
    color = colorWood
    description = u"bridge"
    
    def __init__(self, *args, **kwargs):
        super(Bridge, self).__init__(*args, baseSymbol = u'^', **kwargs)
 
class Town(EriuMapTile):
    symb = symbols.townShape
    terrainType = EriuTownLevel
    areaType = TownArea
    color = colorWood
    description = u"town"
    
    __mapper_args__ = {'polymorphic_identity': u'town'}
     
    def __init__(self, *args, **kwargs):
        super(Town, self).__init__(*args, baseSymbol = self.symb, **kwargs)
        self.name = kwargs.get('name') or G.getPlaceName()
         
    def generateConnectedLevel(self):
        raise NotImplementedError("Deprecated generateConnectedLevel()")
#         self.connectedLevel = self.terrainType(cellsWide = random.randint(2, 4), cellsHigh = random.randint(2, 4))
#         self.connectedLevel.buildLevel()

class Capital(Town):
    
    __mapper_args__ = {'polymorphic_identity': u'capital'}

    def __init__(self, *args, **kwargs):
        super(Capital, self).__init__(*args, **kwargs)
