# coding: utf_8
'''
Created on May 14, 2014

@author: dstuart
'''

from EriuLevel import EriuWildernessLevel, ForestLevel, EriuTownLevel
import MapTileClass as M
from colors import *
import symbols
import KingdomClass as K
import EriuGame as G
from EriuAreas import TownArea

class EriuMapTile(M.MapTile, K.hasKingdom):
    
    def __init__(self, x, y, **kwargs):
        super(EriuMapTile, self).__init__(x, y, **kwargs)
        self.kingdomName = kwargs.get('kingdomName', None)
        self.kingdom = K.getKingdomByName(self.kingdomName)
    
    description = u"eriutile"
    
    def getBackgroundColor(self):
        if self.__dict__.get('kingdom'):
            return self.kingdom.color
        return super(EriuMapTile, self).getBackgroundColor()
        
 
class Forest(EriuMapTile):
    symb = symbols.lowerTau
    terrainType = ForestLevel
    color = colorForest
    description = u"forest"
    
    def __init__(self, *args, **kwargs):
        super(Forest, self).__init__(*args, baseSymbol = self.symb, **kwargs)
 
class Plain(EriuMapTile):
    color = colorPlain
    description = u"plains"
    
    def __init__(self, *args, **kwargs):
        super(Plain, self).__init__(*args, baseSymbol = u'.', **kwargs)
         
class Field(EriuMapTile):
    color = colorField
    description = u"field"
    
    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, baseSymbol = u'.', **kwargs)
 
class Mountain(EriuMapTile):
    color = colorMountain
    description = u"mountain"
    
    def __init__(self, *args, **kwargs):
        super(Mountain, self).__init__(*args, baseSymbol = u'^', **kwargs)
        
class Water(EriuMapTile):
    waterTile = True
    
    def __init__(self, *args, **kwargs):
        super(Water, self).__init__(*args, **kwargs)
 
class Ocean(Water):
    color = colorOcean
    description = u"ocean"
    
    def __init__(self, *args, **kwargs):
        super(Ocean, self).__init__(*args, baseSymbol = symbols.doubleWavy, **kwargs)

class ShallowOcean(Ocean):
    color = colorShallowOcean
    
    def __init__(self, *args, **kwargs):
        super(ShallowOcean, self).__init__(*args, **kwargs)

class River(Water):
    color = colorRiver
    description = u"river"
    
    def __init__(self, *args, **kwargs):
        super(River, self).__init__(*args, baseSymbol = u'~', **kwargs)

class Lake(Water):
    color = colorLake
    description = u"lake"
    
    def __init__(self, *args, **kwargs):
        super(Lake, self).__init__(*args, baseSymbol = u'~', **kwargs) 

class Bridge(EriuMapTile):
    color = colorWood
    description = u"bridge"
    
    def __init__(self, *args, **kwargs):
        super(Bridge, self).__init__(*args, baseSymbol = u'^', **kwargs)
 
class Town(EriuMapTile):
    symb = symbols.townShape
    terrainType = EriuTownLevel
    areaType = TownArea
    color = colorTown
    description = u"town"
    
    def __init__(self, *args, **kwargs):
        super(Town, self).__init__(*args, baseSymbol = self.symb, **kwargs)
        self.name = kwargs.get('name') or G.getPlaceName()
         
    def getDescription(self):
        return self.name + " (" + self.description + ")"

class Capital(Town):
    description = u"capital"
    color = colorCapital

    def __init__(self, *args, **kwargs):
        super(Capital, self).__init__(*args, **kwargs)
