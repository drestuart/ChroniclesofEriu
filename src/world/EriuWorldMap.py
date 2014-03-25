'''
Created on Mar 21, 2014

@author: dstuart
'''

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer

from WorldMapClass import Region, WorldMap
from MapTileClass import Forest, Field, Plain, Mountain, Town, Ocean
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
    regions = relationship("Region", backref=backref("worldMap", uselist=False), primaryjoin="EriuWorldMap.id==Region.worldMapId")
        
    __mapper_args__ = {'polymorphic_identity':'eriu_world_map',
                       }
    
    
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
        
        vmap = VMap(self.width, self.height, self.num_regions, mask = ocean_mask)

        vmap.generate_voronoi_map()
        
        regions = vmap.regions
        centerpoints = vmap.centerPoints
        adj = vmap.getAdjacency()
        
        

        
        
        # Add rivers and other features
        
        
        i = 0
        # Create regions and tile objects
        for region in regions:
            i += 1
            
            newRegion = EriuRegion()
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
            
            # Add some towns to this region
            numTowns = random.randint(C.MIN_TOWNS_PER_REGION, C.MAX_TOWNS_PER_REGION)
            
            for i in range(numTowns):
                # Find a non-water tile
                while True:
                    tile = random.sample(newRegion.mapTiles, 1)[0]
                    if tile.isWaterTile():
                        continue
                    break
            
                # More probably needs to happen here
                townx, towny = tile.getXY()
                newTownTile = Town(townx, towny)
                newRegion.replaceTile(newTownTile)
                self.replaceTile(newTownTile)
                


        # Finish up
        self.buildTileArray()
#         db.saveDB.save(self)