'''
Created on Mar 21, 2014

@author: dstuart
'''

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Boolean

from EriuMapTileClass import Forest, Field, Plain, Mountain, Town, Capital, Ocean, River, Lake, Bridge, Water
import Util as U
from VoronoiMap import VMap
from WorldMapClass import Region, WorldMap
import random
import Const as C
import os.path
import KingdomClass as K

class EriuRegion(Region, K.hasKingdom):
    __tablename__ = "regions"
    __table_args__ = {'extend_existing': True}
    
    def __init__(self, **kwargs):
        super(EriuRegion, self).__init__(**kwargs)
        self.kingdomName = kwargs.get('kingdomName', None)
        self.kingdom = K.getKingdomByName(self.kingdomName)
        self.centerX, self.centerY = kwargs['coords']
        self.tileType = kwargs.get('tileType', None)
        self.capitalRegion = kwargs.get('capitalRegion', False)
        
    kingdomName = Column(String)
    centerX = Column(Integer)
    centerY = Column(Integer)
    capitalRegion = Column(Boolean)
    
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

    def setCapital(self, cap):
        self.capitalRegion = cap
        
    def isCapital(self):
        return self.capitalRegion
        
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
    
    def isWaterInRadius(self, radius, x, y):
        return self.isTileTypeInRadius(radius, x, y, Water)
    
    def placePlayer(self, player):
        tile = self.getTile(25, 7)
        self.placeCreature(player, tile)
            
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

#         self.addKingdoms(regionAdjacency)
        self.addRivers()
        self.addTowns()
    
    def addRivers(self):
        
        # Add rivers and other features
        for i in range(C.NUM_RIVERS):
            sourceTile = None
            placeLake = True
            
            while True:
                sourceTile = self.getRandomTile()
                sourcex, sourcey = sourceTile.getXY()
                
                # Make sure we're not starting too close to another body of water
                if not self.isWaterInRadius(C.MIN_RIVER_LENGTH, sourcex, sourcey):
                    break
            
            # Does this river get a lake?
            lake_rand = random.random()
            if lake_rand > C.LAKE_CHANCE_PER_RIVER:
                placeLake = False
            
            destTile = self.getRandomOceanTile()
            sourcex, sourcey = sourceTile.getXY()
            
            # Add first river tile
            newRiverTile = River(sourcex, sourcey)
            self.replaceTile(newRiverTile)
            currentTile = newRiverTile
            
            riverCoords = [currentTile.getXY()]
            lakeCoords = []
            
            while True:
                # Sorta-random walk to the destination tile
                # Find the next tile to step to
                
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
                           adjTile.getXY() not in lakeCoords and \
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
                    # Decide whether to place a lake
                    if placeLake and (random.random() <= C.LAKE_CHANCE_PER_TILE) and (not self.isTileTypeInRadius(C.LAKE_RADIUS + 2, nextx, nexty, Ocean)):
                        
                        lakeFootprint = self.getRandomLake()
                        
                        xoffset = 0
                        yoffset = 0
                        # Determine the lake center
                        if dx == 0:
                            # Check if the previous river tile will actually connect to a lake tile
                            while True:
                                xoffset = random.choice([-1,0,1])
                                lakeCenterX, lakeCenterY = (nextx + xoffset, nexty + dy*C.LAKE_RADIUS)
                                
                                if dy == 1:
                                    inletx, inlety = (C.LAKE_RADIUS + xoffset, 0)
                                elif dy == -1:
                                    inletx, inlety = (C.LAKE_RADIUS + xoffset, C.LAKE_DIAMETER - 1)
                                
#                                 print "checkx, checky:", checkx, checky
                                
                                if lakeFootprint[inlety][inletx] == '0':
                                    break
                                
                            # Find a water tile for the lake outlet
                            # Logic is opposite of the above since we're on the opposite side of the lake
                            while True:
                                xoffset = random.choice([-1,0,1])
                                if dy == 1:
                                    outletx, outlety = (C.LAKE_RADIUS + xoffset, C.LAKE_DIAMETER - 1)
                                elif dy == -1:
                                    outletx, outlety = (C.LAKE_RADIUS + xoffset, 0)
                                     
                                if lakeFootprint[outlety][outletx] == '0':
                                    break
                                
                        elif dy == 0:
                            # Check if the previous river tile will actually connect to a lake tile
                            while True:
                                yoffset = random.choice([-1,0,1])
                                lakeCenterX, lakeCenterY = (nextx + dx*C.LAKE_RADIUS, nexty + yoffset)
                                
                                if dx == 1:
                                    inletx, inlety = (0, C.LAKE_RADIUS + yoffset)
                                elif dx == -1:
                                    inletx, inlety = (C.LAKE_DIAMETER - 1, C.LAKE_RADIUS + yoffset)
                                    
#                                 print "checkx, checky:", checkx, checky
                                
                                if lakeFootprint[inlety][inletx] == '0':
                                    break
                            
                            # Find a water tile for the lake outlet
                            # Logic is opposite of the above since we're on the opposite side of the lake
                            while True:
                                yoffset = random.choice([-1,0,1])
                                if dx == 1:
                                    outletx, outlety = (C.LAKE_DIAMETER - 1, C.LAKE_RADIUS + yoffset)
                                elif dx == -1:
                                    outletx, outlety = (0, C.LAKE_RADIUS + yoffset)
                                     
                                if lakeFootprint[outlety][outletx] == '0':
                                    break
                        
                        # Place lake tiles
                        for lakei in range(len(lakeFootprint)):
                            row = lakeFootprint[lakei]
                            for lakej in range(len(row)):
                                lakeChar = row[lakej]
                                if lakeChar == 'x': continue
                                lakex, lakey = lakeCenterX - C.LAKE_RADIUS + lakei, lakeCenterY - C.LAKE_RADIUS + lakej
                                
                                newLakeTile = Lake(lakex, lakey)
                                self.replaceTile(newLakeTile)
                                lakeCoords.append((lakex, lakey))
                        
                        # Make sure not to place more than one per river
                        placeLake = False
                        
                        # Place a new river tile on the other side of the lake to generate from on the next loop
                        nextx, nexty = lakeCenterX - C.LAKE_RADIUS + outletx + dx, lakeCenterY - C.LAKE_RADIUS +  outlety + dy
#                         
                        newRiverTile = River(nextx, nexty)
                        self.replaceTile(newRiverTile)
                        currentTile = newRiverTile
                        riverCoords.append((nextx, nexty))

                    
                    else:
                        # Place the next river tile
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
                    # Check that we're on a river tile
                    oldTile = self.getTile(bridgex, bridgey)
                    if not isinstance(oldTile, River): 
                        continue
                    
                    # Check that we're far enough from the other bridges
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
    
    def getRandomLake(self):
        lakes = [
                 ['x000x',
                  '00000',
                  '00000',
                  '00000',
                  'x000x'],
                 ['xx0xx',
                  'x000x',
                  '00000',
                  'x000x',
                  'xx0xx'],
                 ['xx0xx',
                  'x000x',
                  '0000x',
                  '00000',
                  'xx0xx'],
                 ['xx00x',
                  '0000x',
                  '00000',
                  'x0000',
                  'x00xx'],
                 ['x00xx',
                  'x0000',
                  '00000',
                  '0000x',
                  'xx00x'],
                 ['xx0xx',
                  'x0000',
                  '00000',
                  'x0000',
                  'xx00x'],
                 ]
        
        return random.choice(lakes)
        
        
            
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
            chosenRegion.setCapital(True)
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
            
            if not (centerTile.isWaterTile() or isinstance(centerTile, Bridge)):
                # If this is the capital region of this kingdom, get the kingdom's capital name
                name = None
                if region.isCapital():
                    name = region.getKingdom().getCapitalName()
                
                newTownTile = Capital(centerX, centerY, name = name)
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
                        name = None
                        if region.isCapital():
                            name = region.getKingdom().getCapitalName()
                        newTownTile = Capital(x, y, name = name)
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
                
                
