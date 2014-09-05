'''
Created on Sep 3, 2014

@author: dstuart

Eriu-specific subclasses of the wang-tile map generators and associated classes
'''

from WangTileClass import SquareWangTile, HorzWangTile, VertWangTile, SquareWangTileSet, RectWangTileSet
from WangTileMap import SquareWangTileMap, HerringboneWangTileMap
from LevelClass import DungeonLevel, TownLevel
import os

os.chdir("/Users/dstuart/workspace/ChroniclesofEriu")

class TownWangTile(SquareWangTile):
    defaultConstraint = None

class dungeonHTile(HorzWangTile):
    pass

class dungeonVTile(VertWangTile):
    pass

class TownMap(SquareWangTileMap):
    tileset = SquareWangTileSet(TownWangTile)
    tileset.readFromFile(os.path.join("data", "templates", "towntiles.txt"))
        
    def __init__(self, *args):
        super(TownMap, self).__init__(*args)
        
        
class DungeonMap(HerringboneWangTileMap):
    tileset = RectWangTileSet(dungeonVTile, dungeonHTile)
    tileset.readFromFile(os.path.join("data", "templates", "dungeon_vtiles.txt"))
    
    def __init__(self, *args, **kwargs):
        super(DungeonMap, self).__init__(*args, **kwargs)
        
class EriuTownLevel(TownLevel):
    __mapper_args__ = {'polymorphic_identity': 'eriu town level'}
    MapBuilderType = TownMap


class EriuDungeonLevel(DungeonLevel):
    __mapper_args__ = {'polymorphic_identity': 'eriu dungeon level'}
    MapBuilderType = DungeonMap


def main():
    townMap = TownMap(3, 3)
    townMap.printMap()

    print
    
    dungeonMap = DungeonMap(3, 3, margin = 1)
    dungeonMap.printMap()
    
if __name__ == "__main__":
    main()