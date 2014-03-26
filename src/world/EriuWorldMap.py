'''
Created on Mar 21, 2014

@author: dstuart
'''

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer

from WorldMapClass import Region, WorldMap
from MapTileClass import Forest, Field, Plain, Mountain, Town, Ocean, River
import Util as U
from VoronoiMap import VMap
import database as db
import random
import Const as C
import os.path

Base = db.saveDB.getDeclarativeBase()

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

class EriuRegion(Region):
    __tablename__ = "regions"
    __table_args__ = {'extend_existing': True}
    
    def __init__(self, **kwargs):
        super(EriuRegion, self).__init__(**kwargs)
        
    kingdomId = Column(Integer, ForeignKey("kingdoms.id"))
    mapTiles = relationship("MapTile", backref=backref("region", uselist=False), primaryjoin="EriuRegion.id==MapTile.regionId")
    
    def setKingdom(self, k):
        self.kingdom = k
        
class Kingdom(Base):
    __tablename__ = "kingdoms"
    __table_args__ = {'extend_existing': True}
    
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        
    id = Column(Integer, primary_key=True)
    name = Column(String)
    regions = relationship("EriuRegion", backref=backref("kingdom", uselist=False), primaryjoin="Kingdom.id==EriuRegion.kingdomId")
    
    def getRegions(self):
        return self.regions
    
    def addRegion(self, reg):
        self.regions.append(reg)
        reg.setKingdom(self)
    
    def containsRegion(self, reg):
        return reg in self.regions

class EriuWorldMap(WorldMap):

    def __init__(self, **kwargs):
        super(EriuWorldMap, self).__init__(**kwargs)
        
    mapTiles = relationship("MapTile", backref=backref("worldMap", uselist=False), primaryjoin="EriuWorldMap.id==MapTile.worldMapId")
    regions = relationship("EriuRegion", backref=backref("worldMap", uselist=False), primaryjoin="EriuWorldMap.id==EriuRegion.worldMapId")
        
    __mapper_args__ = {'polymorphic_identity':'eriu_world_map'}
    
    def getRandomTile(self, isWater = False):
        while True:
            retTile = random.choice(self.mapTiles)
            
            if retTile.isWaterTile() == isWater:
                return retTile
            
    def getRandomOceanTile(self):
        while True:
            retTile = self.getRandomTile(isWater = True)
            if isinstance(retTile, Ocean):
                return retTile
            
    def getRegions(self):
        return self.regions
    
    def addRegion(self, reg):
        self.regions.append(reg)
    
    def buildMap(self):
        ''' Oh here we go. '''
        
        # Read in template
        map_template = U.readTemplateFile(os.path.join("data", "templates", "world_map_test"))

        ocean_mask = U.twoDArray(C.WORLD_MAP_WIDTH, C.WORLD_MAP_HEIGHT, True)

        # Overlay template, add tiles
        for x in range(C.WORLD_MAP_WIDTH):
            for y in range(C.WORLD_MAP_HEIGHT):
                if map_template[y][x] == '=':
                    ocean_mask[x][y] = False
                    
                    # Ocean tile
                    newTile = Ocean(x, y)
                    self.addTile(newTile)
                else:
                    pass
                
        # Generate Voronoi map
        vmap = VMap(self.width, self.height, self.num_regions, mask = ocean_mask)

        vmap.generate_voronoi_map()
        
        regions = vmap.regions
        centerpoints = vmap.centerPoints
        adj = vmap.getAdjacency()

        
        i = 0
        # Create regions and tile objects
        for region in regions:
            i += 1
            
            newRegion = EriuRegion()
            self.addRegion(newRegion)
            newKingdom = Kingdom(name = str(i))
            newKingdom.addRegion(newRegion)
            
            tiletype = newRegion.getTileType() 
            
            for (x, y) in region.memberPoints:
                # Skip tiles we've already added
                if self.hasTile[x][y]: 
                    tile = self.getTile(x, y)
                    newRegion.addTile(tile)
                
                else:
                    newTile = tiletype(x, y)
                    newRegion.addTile(newTile)
                    self.addTile(newTile)
        
        self.buildTileArray()
        
        
        # Add rivers and other features
        for i in range(C.NUM_RIVERS):
            sourceTile = self.getRandomTile()
            destTile = self.getRandomOceanTile()
            
            sourcex, sourcey = sourceTile.getXY()
            reg = sourceTile.getRegion()
            
            # Add first river tile
            newRiverTile = River(sourcex, sourcey)
            reg.replaceTile(newRiverTile)
            self.replaceTile(newRiverTile)
            currentTile = newRiverTile
            
            riverCoords = [currentTile.getXY()]
            
            while True:
                # Sorta-random walk to the destination tile
                
                x = currentTile.getX()
                y = currentTile.getY()
                
                if x < destTile.getX(): dx = 1
                elif x > destTile.getX(): dx = -1
                else: dx = 0
                
                if y < destTile.getY(): dy = 1
                elif y > destTile.getY(): dy = -1
                else: dy = 0
                
                r = random.random()
                
                # Set one of dx or dy to 0 so that the river doesn't move diagonally
                
                if dx == 0 or dy == 0:
                    pass
                elif r < 1/2.:
                    # Only move in the x direction
                    dy = 0
                else:
                    # Only move in the y direction
                    dx = 0
            
                # Stop if we're adjacent to water
                nextToWater = False
                for j in (-1, 0, 1):
                    for k in (-1, 0, 1):
                        if j == 0 and k == 0: continue
                        if j != 0 and k != 0: continue
                        adjTile = self.getTile(x + j, y + k)
                        if adjTile.isWaterTile() and \
                           adjTile.getXY() not in riverCoords: 
                                nextToWater = True
                        
                if nextToWater: break;
                
                nextx, nexty = x + dx, y + dy
                nextTile = self.getTile(nextx, nexty)
                
                if not nextTile:
                    break
                
                reg = nextTile.getRegion()
                
                if nextTile.isWaterTile():
                    break
                else:
                    newRiverTile = River(nextx, nexty)
                    reg.replaceTile(newRiverTile)
                    self.replaceTile(newRiverTile)
                    currentTile = newRiverTile
                    riverCoords.append((nextx, nexty))
        
        
        for region in self.regions:
            # Add some towns to this region
            numTowns = random.randint(C.MIN_TOWNS_PER_REGION, C.MAX_TOWNS_PER_REGION)
            
            for i in range(numTowns):
                # Find a non-water tile
                while True:
                    tile = random.choice(region.mapTiles)
                    if tile.isWaterTile() or isinstance(tile, Town):
                        continue
                    break
            
                # More probably needs to happen here
                townx, towny = tile.getXY()
                newTownTile = Town(townx, towny)
                newRegion.replaceTile(newTownTile)
                self.replaceTile(newTownTile)
                

