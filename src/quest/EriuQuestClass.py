'''
Created on Jun 23, 2015

@author: dstuart
'''

from QuestClass import Quest, ItemQuest, QuestItemRequirement
import EriuGame
from ItemClass import MacGuffin
import ConversationClass as C

class EriuQuest(Quest):
    pass

class EriuItemQuest(ItemQuest):
    pass

class TestQuest(EriuItemQuest):
    
    def __init__(self):
        super(TestQuest, self).__init__([(MacGuffin, 3)])
        self.buildRequirements()
    
    def placeQuestItems(self):
        for req in self.getRequirements():
            itemType = req.getItemType()
            for dummy in range(req.getEventsRequired()):
                item = itemType(questItem=True)
                currentLevel = EriuGame.game.ui.getCurrentLevel()
                currentLevel.placeItemAtRandom(item)

    def getStartConversation(self):
        if not self.startConversation:
            firstNode = C.ConversationNode("We don't have much time. I need you to get those Mystic MacGuffins for me.")
            secondNode = C.ConversationNode("They're all over the place. Can you do it?")
            
            nodes = [firstNode, secondNode]
            
            firstNode.createOption("Go on...", secondNode)
            secondNode.createOption("Sure, no problem", None, self.startQuest)
            secondNode.createOption("Not happening, buddy")
            
            self.startConversation = C.ConversationTree(nodes)
        return self.startConversation

    def getProgressConversation(self):
        if not self.progressConversation:
            node = C.ConversationNode("Have you found those MacGuffins yet? They say they're Mystical as all get-out!")
            node.createOption("OK")
            self.progressConversation = C.ConversationTree([node])
        return self.progressConversation
    
    def getCompletedConversation(self):
        if not self.completedConversation:
            node = C.ConversationNode("Thank you! Those are some Mystical MacGuffins!")
            node.createOption("No problem", None, self.setReturned)
            self.completedConversation = C.ConversationTree([node])
        return self.completedConversation

        