'''
Created on Jun 23, 2015

@author: dstuart
'''

from __future__ import unicode_literals

from QuestClass import Quest, ItemQuest, KillQuest
import EriuGame
from ItemClass import MacGuffin
from CreatureClass import Orc
import ConversationClass as C
from EriuMapTileClass import Town, Forest
from AreaClass import StartingLevelBuildingThread

class EriuQuest(Quest):
    def setUpQuest(self):
        # Find an NPC in a town level to make the quest NPC
        game = EriuGame.game
        playerTile = game.getPlayer().getTile()
        townTile = game.getWorldMap().getNearestTile(playerTile, Town)
        t = townTile.getStartingLevel()
        
        print "Quest added to town level at", townTile.getXY()
        
        questNPC = t.getRandomNPC()
        self.setQuestGivingNPC(questNPC)
        self.setQuestReturnNPC(questNPC)
        
        print "Quest attached to NPC at", questNPC.getXY()

class EriuItemQuest(ItemQuest, EriuQuest):
    pass

class EriuKillQuest(KillQuest, EriuQuest):
    pass

class TestItemQuest(EriuItemQuest):
    
    def __init__(self):
        super(TestItemQuest, self).__init__([(MacGuffin, 3)])
        self.buildRequirements()
        self.questName = "MacGuffin Madness!"
        self.setUpQuest()
        
    def placeQuestItems(self):
        import Game as G

        random = G.getRandom()

        # Find a forest level to put the items in
        game = EriuGame.game
        currentX, currentY = game.getCurrentMapTile().getXY()
        possibleGoals = game.getWorldMap().getTilesInRange(20, 30, currentX, currentY, Forest)
        goalTile = random.choice(possibleGoals)
        goalArea = goalTile.getConnectedArea()
        print "Quest items added to level at", goalTile.getXY()
        
        items = []
        for req in self.getRequirements():
            itemType = req.getItemType()
            for dummy in range(req.getEventsRequired()):
                item = itemType(questItem=True)
                items.append(item)
                
        # Start thread to generate level and populate it with items
        print "Setting up thread"
        thread = StartingLevelBuildingThread(goalArea, items)
        thread.start()
        print "Thread running!"

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

class TestKillQuest(EriuKillQuest):
    
    def __init__(self):
        super(TestKillQuest, self).__init__([(Orc, 2)])
        self.buildRequirements()
        self.questName = "Orc oddity"
        self.setUpQuest()
    
    #TODO:
    def placeQuestCreatures(self):
        pass
    
    def getStartConversation(self):
        pass
#         if not self.startConversation:
#             firstNode = C.ConversationNode("We don't have much time. I need you to get those Mystic MacGuffins for me.")
#             secondNode = C.ConversationNode("They're all over the place. Can you do it?")
#             
#             nodes = [firstNode, secondNode]
#             
#             firstNode.createOption("Go on...", secondNode)
#             secondNode.createOption("Sure, no problem", None, self.startQuest)
#             secondNode.createOption("Not happening, buddy")
#             
#             self.startConversation = C.ConversationTree(nodes)
#         return self.startConversation

    def getProgressConversation(self):
        pass
#         if not self.progressConversation:
#             node = C.ConversationNode("Have you found those MacGuffins yet? They say they're Mystical as all get-out!")
#             node.createOption("OK")
#             self.progressConversation = C.ConversationTree([node])
#         return self.progressConversation
    
    def getCompletedConversation(self):
        pass
#         if not self.completedConversation:
#             node = C.ConversationNode("Thank you! Those are some Mystical MacGuffins!")
#             node.createOption("No problem", None, self.setReturned)
#             self.completedConversation = C.ConversationTree([node])
#         return self.completedConversation
        