'''
Created on Jun 23, 2015

@author: dstuart
'''

from QuestClass import Quest, QuestItemRequirement
import EriuGame
from ItemClass import MacGuffin

class EriuQuest(Quest):
    pass

class testQuest(EriuQuest):
    
    def __init__(self):
        self.buildRequirements()
        self.placeQuestItems()
    
    def buildRequirements(self):
        # Add one requirement for a MacGuffin
        req = QuestItemRequirement(MacGuffin, 1, self)
        self.addRequirement(req)
    
    def placeQuestItems(self):
        mg = MacGuffin(questItem=True)
        currentLevel = EriuGame.game.ui.getCurrentLevel()
        currentLevel.placeItemAtRandom(mg)
        