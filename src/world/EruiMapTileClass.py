'''
Created on May 14, 2014

@author: dstuart
'''

import MapTileClass as M
import delvelib.src.database.database as db
import world.KingdomClass as K

Base = db.saveDB.getDeclarativeBase()

class EriuMapTile(M.MapTile, K.hasKingdom):
    
    def __init__(self, **kwargs):
        super(EriuMapTile, self).__init__(**kwargs)
        self.kingdomName = kwargs.get('kingdomName', None)
        self.kingdom = K.getKingdomByName(self.kingdomName)
    
    
    __mapper_args__ = {'polymorphic_identity': 'eriumaptile'}
    
    def getBackgroundColor(self):
        if self.kingdom:
            return self.kingdom.color
        return super(EriuMapTile, self).getBackgroundColor()
        