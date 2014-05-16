'''
Created on May 14, 2014

@author: dstuart
'''

from sqlalchemy.schema import Column
from sqlalchemy.types import String

import colors


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
#
######################################
kingdoms = dict()

def getKingdomByName(name):
    if not name: return None
    return kingdoms.get(name, None)

class Kingdom(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.color = kwargs['color']
        self.capital = kwargs['capital']
        
        global kingdoms
        kingdoms[self.name] = self
        
    def getName(self):
        return self.name
    
    def getColor(self):
        return self.color
    
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
ulaid = Kingdom(name="Ulaid", color=colors.red, capital="Emain Macha")
connacht = Kingdom(name="Connacht", color=colors.blue, capital="Cruachan")
leinster = Kingdom(name="Leinster", color=colors.green, capital="Leinster")
munster = Kingdom(name="Munster", color=colors.yellow, capital="Munster")
mide = Kingdom(name="Mide", color=colors.orange, capital="Mide")


