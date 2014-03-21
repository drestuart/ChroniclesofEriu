'''
Created on Mar 21, 2014

@author: dstuart
'''

from WorldMapClass import *
import LevelClass as L
from MapTileClass import Forest, Field, Plain, Mountain, Town
import Util as U
from VoronoiMap import VMap
import database as db
import random
import Const as C

class EriuWorldMap(WorldMap):
    __mapper_args__ = {'polymorphic_identity':'eriu_world_map'}

    def __init__(self, **kwargs):
        super(EriuWorldMap, self).__init__(**kwargs)
        
    def buildMap(self):
        ''' Oh here we go. '''
        
        vmap = VMap(self.width, self.height, self.num_regions)

        vmap.generate_voronoi_map()
        
        regions = vmap.regions
        centerpoints = vmap.centerPoints
        adj = vmap.getAdjacency()
        
        # Overlay template, add tiles
        
        
        # Add rivers and other features
        
        
        
        # Create regions and tile objects
        for region in regions:
            newRegion = Region()
            
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
            townTiles = random.sample(newRegion.mapTiles, numTowns)
            
            for tile in townTiles:
                # More probably needs to happen here
                townx, towny = tile.getXY()
                newTownTile = Town(townx, towny)
                newRegion.replaceTile(newTownTile)
                self.replaceTile(newTownTile)
                


        # Finish up
        self.buildTileArray()
#         db.saveDB.save(self)