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
        super(EriuNPC, self).__init__(**kwargs)
        self.name = EriuGame.getMaleName()
        self.description = self.name
