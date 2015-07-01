'''
Created on Jun 23, 2015

@author: dstuart
'''

from QuestClass import Quest, QuestItemRequirement
import EriuGame
from ItemClass import MacGuffin
import ConversationClass as C

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
        
    def getConversation(self):
        firstNode = C.ConversationNode("We don't have much time. I need you to get that Mystic MacGuffin for me.")
        secondNode = C.ConversationNode("It's over there. Can you do it?")
        
        nodes = [firstNode, secondNode]
        
        firstNode.createOption("Go on...", secondNode)
        secondNode.createOption("Sure, no problem", None, self.startQuest)
        secondNode.createOption("Not happening, buddy")
        
        self.conversation = C.ConversationTree(nodes)
        return self.conversation




        