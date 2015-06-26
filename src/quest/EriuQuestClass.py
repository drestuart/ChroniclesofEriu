'''
Created on Jun 23, 2015

@author: dstuart
'''

from QuestClass import Quest
import EriuGame
from ItemClass import MacGuffin

class EriuQuest(Quest):
    pass



class testQuest(EriuQuest):
    
    def placeQuestItems(self):
        mg = MacGuffin(questItem=True)
        currentLevel = EriuGame.getCurrentLevel()
        currentLevel.placeItemAtRandom(mg)
        