'''
Created on Mar 21, 2014

@author: dstuart
'''

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer

from EriuMapTileClass import Forest, Field, Plain, Mountain, Town, Capital, Ocean, River, Bridge
import Util as U
from VoronoiMap import VMap
from WorldMapClass import Region, WorldMap
import random
import Const as C
import os.path
import KingdomClass as K
import database as db

class EriuRegion(Region, K.hasKingdom):
    __tablename__ = "regions"
    __table_args__ = {'extend_existing': True}
    
    def __init__(self, **kwargs):
        super(EriuRegion, self).__init__(**kwargs)
        self.kingdomName = kwargs.get('kingdomName', None)
        self.kingdom = K.getKingdomByName(self.kingdomName)
        self.centerX, self.centerY = kwargs['coords']
        self.tileType = kwargs.get('tileType', None)
        
    kingdomName = Column(String)
    centerX = Column(Integer)
    centerY = Column(Integer)
    
    def setKingdom(self, k):
        self.kingdom = k
        if k:
            self.kingdomName = k.getName()
                     
        for tile in self.mapTiles:
            if not isinstance(tile, Ocean):
                tile.setKingdom(k)
            
    def getCoords(self):
        return self.centerX, self.centerY
    
    def addTile(self, tile):
        super(EriuRegion, self).addTile(tile)
        tile.setKingdom(self.getKingdom())
        
    def replaceTile(self, oldtile, newtile):
        super(EriuRegion, self).replaceTile(oldtile, newtile)
        newtile.setKingdom(self.getKingdom())
#         print self.getKingdom(), oldtile.getKingdom(), newtile.getKingdom()
        
    __mapper_args__ = {'polymorphic_identity': 'eriu_region'}
    
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
            
    def isTileTypeInRadius(self, radius, x, y, tiletype):
        tileFound = False
        nearbyTiles = self.getTilesInRadius(radius, x, y)
        for nt in nearbyTiles:
            if isinstance(nt, tiletype):
                tileFound = True
                break
        return tileFound
            
    def getRegions(self):
        return self.regions
    
    def addRegion(self, reg):
        self.regions.append(reg)
    
    def buildMap(self):
        ''' Oh here we go. '''

        # Read in template
#         map_template = U.readTemplateFile(os.path.join("data", "templates", "world_map_test"))
        map_template = U.readTemplateImage(os.path.join("data", "templates", "eriu_map.bmp"),
                                           {(63, 72, 204) : '=', # Blue
                                            (34, 177, 76) : '.', # Green
                                            })
         
#         for row in map_template:
#             print ' '.join(row)

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
#         centerpoints = vmap.centerPoints
        adj = vmap.getAdjacency()
        
        vmapToEriuRegions = dict()
        
        i = 0
        # Create regions and tile objects
        for region in regions:
            i += 1
            
            regionTiletype = random.choice([Forest, Field, Plain, Mountain])
            newRegion = EriuRegion(coords = region.centerPoint, tileType = regionTiletype)
            self.addRegion(newRegion)
            
            # Store correspondence between VMapRegions and EriuRegions so we can
            # rebuild the adjacency graph later
            vmapToEriuRegions[region] = newRegion
            
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
        
        # rebuild the adjacency graph
        # TODO: actually implement this as a many-to-many on the regions table
        regionAdjacency = dict()
        for reg, aregs in adj.items():
            region = vmapToEriuRegions[reg]
            adjRegions = []
            for ar in aregs:
                adjRegions.append(vmapToEriuRegions[ar])
            
            regionAdjacency[region] = adjRegions
        
        self.buildTileArray()

        self.addKingdoms(regionAdjacency)
        self.addRivers()
        self.addTowns()
    
    def addRivers(self):
        
        # Add rivers and other features
        for i in range(C.NUM_RIVERS):
            sourceTile = self.getRandomTile()
            destTile = self.getRandomOceanTile()
            
            sourcex, sourcey = sourceTile.getXY()
            
            # Add first river tile
            newRiverTile = River(sourcex, sourcey)
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
                        if x + j < 0 or y + k < 0: continue
                        adjTile = self.getTile(x + j, y + k)
                        if adjTile.isWaterTile() and \
                           adjTile.getXY() not in riverCoords: 
                                nextToWater = True
                        
                if nextToWater: break;
                
                nextx, nexty = x + dx, y + dy
                nextTile = self.getTile(nextx, nexty)
                
                if not nextTile:
                    break
                
                if nextTile.isWaterTile():
                    break
                else:
                    newRiverTile = River(nextx, nexty)
                    self.replaceTile(newRiverTile)
                    currentTile = newRiverTile
                    riverCoords.append((nextx, nexty))
            
            # Add a bridge to a random spot on the river
            rlen = len(riverCoords)
            numBridges = int(rlen/C.RIVER_TILES_PER_BRIDGE)
            bridgeCoords = []
            for dummyi in range(numBridges):
                while True:
                    (bridgex, bridgey) = random.choice(riverCoords[1:-1]) # Not the first or last tile, because really.
                    
                    badTile = False
                    for (x,y) in bridgeCoords:
                        dist = self.coordinateDistance(x, bridgex, y, bridgey)
                        if dist <= C.BRIDGE_SPACING:
                            badTile = True
                            break

                    if badTile: continue
                    
                    newBridgeTile = Bridge(bridgex, bridgey)
                    self.replaceTile(newBridgeTile)
                    bridgeCoords.append((bridgex, bridgey))
                    break
            
    def addKingdoms(self, adjacency):
        regionsByKingdom = dict()
        
        # Assign first region for each kingdom
        for k in K.allKingdoms:
            # Set starting regions
            kx, ky = k.getCoords()
            smallestdist = None
            chosenRegion = None
             
            for region in self.regions:
                rx, ry = region.getCoords()
                dist = self.coordinateDistance(rx, kx, ry, ky)
                 
                if chosenRegion is None or dist < smallestdist:
                    chosenRegion = region
                    smallestdist = dist
                     
            chosenRegion.setKingdom(k)
            regionsByKingdom[k] = [chosenRegion]
#             print "Placing", k, chosenRegion.kingdom

        # Grow each kingdom by adding an adjacent region
        for dummy in range(C.REGIONS_PER_KINGDOM - 1): # Each kingdom already has one region!
            for k in K.allKingdoms:
                for reg in regionsByKingdom[k]:
                    # Look at all the regions adjacent to this one
                    adjRegs = adjacency[reg]
                    foundRegion = None
                    for ar in adjRegs:
                        if ar.getKingdom():
                            continue
                        ar.setKingdom(k)
                        
                        foundRegion = ar
                        break
                    
                    if foundRegion:
                        break
                    
                if foundRegion:
                    regionsByKingdom[k].append(foundRegion)
#                 else:
#                     print "Couldn't add a region to", k
                
        # Sanitas check
#         print C.REGIONS_PER_KINGDOM
#         for k in K.allKingdoms:
#             print k.name, len(regionsByKingdom[k])
                
    
        
    def addTowns(self):
        # Add some towns to each region
        
        ############
        #
        # TODO: Place town at region center
        #
        ############

        for region in self.regions:
            
            numTiles = len(region.mapTiles)
            numTowns = numTiles/C.REGION_TILES_PER_CITY
            
            # Enforce max and min
            numTowns = max(numTowns, C.MIN_TOWNS_PER_REGION)
            numTowns = min(numTowns, C.MAX_TOWNS_PER_REGION)
            
            townsPlaced = 0
            spacing = C.STARTING_TOWN_SPACING
            
            # Try to place a capital town at the region center
            centerX, centerY = region.getCoords()
            centerTile = self.getTile(centerX, centerY)
            
            if not centerTile.isWaterTile() or isinstance(centerTile, Bridge):
                newTownTile = Capital(centerX, centerY)
                self.replaceTile(newTownTile)
                placedTown = True
                townsPlaced += 1
            
            while townsPlaced < numTowns:
                # Find a non-water tile at the right distance from any other towns
                
                placedTown = False
                # Start by shuffling self.mapTiles and picking tiles off the top
                random.shuffle(region.mapTiles)
                for tile in region.mapTiles:
                    # Skip water tiles and tiles that already have towns
                    if tile.isWaterTile() or isinstance(tile, Town) or isinstance(tile, Bridge):
                        continue
                    
                    x, y = tile.getXY()
                    if self.isTileTypeInRadius(spacing, x, y, Town): continue
                    
                    if townsPlaced == 0:  # Place a regional capital if we haven't already
                        newTownTile = Capital(x, y)
                    else:
                        newTownTile = Town(x, y)
                        
                    newTownTile.setKingdom(region.getKingdom())
                    self.replaceTile(newTownTile)
                    placedTown = True
                    townsPlaced += 1
                    
                    break
                
                if not placedTown:
                    spacing -= 1
                    
                    if spacing < C.MIN_TOWN_SPACING:
                        break
                    else:
                        continue
                
                
