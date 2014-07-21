# coding: utf_8
'''
Created on May 14, 2014

@author: dstuart
'''

from colors import colorUlaid, colorConnacht, colorLeinster, colorMunster, colorMide
import Const as C

kingdoms = dict()
allKingdoms = []

def getKingdomByName(name):
    if not name: return None
    return kingdoms.get(name, None)

class Kingdom(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.color = kwargs['color']
        self.capitalName = kwargs['capitalName']
        self.startingCoords = kwargs['coords']
        
        global kingdoms
        global allKingdoms
        
        kingdoms[self.name] = self
        allKingdoms.append(self)
        
    def getName(self):
        return self.name
    
    def getCapitalName(self):
        return self.capitalName
    
    def getColor(self):
        return self.color
    
    def getCoords(self):
        return self.startingCoords
    
    def __repr__(self):
        return "Kingdom " + self.name
    
class hasKingdom(object):
    
    def getKingdom(self):
        if self.__dict__.get('kingdom'):
            return self.kingdom
        self.kingdom = getKingdomByName(self.kingdomName)
        return self.kingdom
    
    def setKingdom(self, k):
        self.kingdom = k
        if k:
            self.kingdomName = k.getName()

    
######################################
#
#   Kingdoms
#   
#   Ulaid: NE, Red, Emain Macha
#   Connact: NW, Blue, Cruachan
#   Leinster: SE, Green, 
#   Munster: SW, Yellow, 
#   Mide: Center-east, Orange, 
#
######################################

# Define the five kingdoms of Eriu
ulaid = Kingdom(name="Ulaid", color = colorUlaid, capitalName="Emain Macha", coords=(C.WORLD_MAP_WIDTH, 0))
connacht = Kingdom(name="Connacht", color = colorConnacht, capitalName="Cruachan", coords=(0, C.WORLD_MAP_HEIGHT/3))
leinster = Kingdom(name="Leinster", color = colorLeinster, capitalName=u"Dún Ailinne", coords=(C.WORLD_MAP_WIDTH, C.WORLD_MAP_HEIGHT))
munster = Kingdom(name="Munster", color = colorMunster, capitalName="Luimneach", coords=(0, C.WORLD_MAP_HEIGHT))
mide = Kingdom(name="Mide", color = colorMide, capitalName=u"Teamhair na Rí", coords=(C.WORLD_MAP_WIDTH, C.WORLD_MAP_HEIGHT/2))


