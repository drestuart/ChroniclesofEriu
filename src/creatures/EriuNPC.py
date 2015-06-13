'''
Created on Jun 9, 2015

@author: dstuart
'''

import colors
import EriuGame
import NPCClass as NPC
import AIClass as AI

class EriuNPC(NPC.NPC):
    
    color = colors.lighterGrey
    
    def __init__(self, **kwargs):
        self.name = EriuGame.getMaleName()
        self.description = self.name
        super(EriuNPC, self).__init__(**kwargs)

    __mapper_args__ = {'polymorphic_identity': u'EriuNPC'}
