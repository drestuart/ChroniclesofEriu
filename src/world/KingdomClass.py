'''
Created on May 14, 2014

@author: dstuart
'''

from sqlalchemy.schema import Column
from sqlalchemy.types import String

import colors
import Const as C

kingdomsByName = dict()
allKingdoms = []

def getKingdomByName(name):
    if not name: return None
    return kingdomsByName.get(name, None)

class Kingdom(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.color = kwargs['color']
        self.capital = kwargs['capital']
        self.startingCoords = kwargs['coords']
        
        global kingdomsByName
        global allKingdoms
        
        kingdomsByName[self.name] = self
        allKingdoms.append(self)
        
    def getName(self):
        return self.name
    
    def getColor(self):
        return self.color
    
    def getStartingCoords(self):
        return self.startingCoords
    
class hasKingdom(object):
    
    kingdomName = Column(String)
    
    def getKingdom(self):
        if self.kingdom:
            return self.kingdom
        self.kingdom = getKingdomByName(self.kingdomName)
        return self.kingdom
    
    def setKingdom(self, k):
        self.kingdom = k
    
    
# Define the five kingdoms of Eriu

######################################
#
#   Kingdoms
#   
#   Ulaid: NE, Red
#   Connact: NW, Blue
#   Leinster: W, Green
#   Munster: SW, Yellow
#   Mide: Center-east, Orange
#
######################################

ulaid = Kingdom(name="Ulaid", color=colors.red, capital="Emain Macha", coords=(C.WORLD_MAP_WIDTH, 0))
connacht = Kingdom(name="Connacht", color=colors.blue, capital="Cruachan", coords=(0, 0))
leinster = Kingdom(name="Leinster", color=colors.green, capital="Leinster", coords=(0, C.WORLD_MAP_HEIGHT/2))
munster = Kingdom(name="Munster", color=colors.yellow, capital="Munster", coords=(0, C.WORLD_MAP_HEIGHT))
mide = Kingdom(name="Mide", color=colors.orange, capital="Mide", coords=(C.WORLD_MAP_WIDTH, C.WORLD_MAP_HEIGHT/2))


