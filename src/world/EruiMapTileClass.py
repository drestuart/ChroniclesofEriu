'''
Created on May 14, 2014

@author: dstuart
'''

import MapTileClass as M
import delvelib.src.database.database as db
from sqlalchemy.types import String
from sqlalchemy.schema import Column
import world.KingdomClass as K

Base = db.saveDB.getDeclarativeBase()

class EriuMapTile(M.MapTile):
    
    def __init__(self, **kwargs):
        super(EriuMapTile, self).__init__(**kwargs)
        self.kingdomName = kwargs.get('kingdomName', None)
        self.kingdom = K.getKingdomByName(self.kingdomName)
    
    kingdomName = Column(String)
    
    __mapper_args__ = {'polymorphic_identity': 'eriumaptile'}
    
    def getKingdom(self):
        if self.kingdom:
            return self.kingdom
        self.kingdom = K.getKingdomByName(self.kingdomName)
        return self.kingdom
    
    def getBackgroundColor(self):
        if self.kingdom:
            return self.kingdom.color
        return super(EriuMapTile, self).getBackgroundColor()
        