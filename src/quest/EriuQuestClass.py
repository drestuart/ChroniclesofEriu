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
        super(testQuest, self).__init__()
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
        
    def getStartConversation(self):
        if not self.startConversation:
            firstNode = C.ConversationNode("We don't have much time. I need you to get that Mystic MacGuffin for me.")
            secondNode = C.ConversationNode("It's over there. Can you do it?")
            
            nodes = [firstNode, secondNode]
            
            firstNode.createOption("Go on...", secondNode)
            secondNode.createOption("Sure, no problem", None, self.startQuest)
            secondNode.createOption("Not happening, buddy")
            
            self.startConversation = C.ConversationTree(nodes)
        return self.startConversation

    def getProgressConversation(self):
        if not self.progressConversation:
            node = C.ConversationNode("Have you found that MacGuffin yet? They say it's Mystical as all get-out!")
            node.createOption("OK")
            self.progressConversation = C.ConversationTree([node])
        return self.progressConversation
    
    def getCompletedConversation(self):
        if not self.completedConversation:
            node = C.ConversationNode("Thank you! That is one Mystical MacGuffin!")
            node.createOption("No problem")
            self.completedConversation = C.ConversationTree([node])
        return self.completedConversation


        