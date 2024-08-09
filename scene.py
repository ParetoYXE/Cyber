import random

class Scene():

	def __init__(self, name,description, npcs = None):
		self.name = name
		self.description = description
		self.npcs = npcs
		self.in_combat = False
		self.npc_combat = None

	def check_encounter(self,player_stats):
		if self.npcs != None:
			for npc in self.npcs:
				if npc.hp > 0:
					if npc.hostile:
						self.in_combat = True
						self.npc_combat = npc
					else:
						return "There is a " + npc.description
		else:
			return "You are alone."

	def combat(self,player_stats):
		enemy = self.npc_combat
		
		output_lines = []
		
		if(enemy.hp > 0):

			output_lines.append("You are in combat with a " + enemy.description)
			
			damage = random.randint(1,5)

			player_stats['Hit Points'] -= damage

			output_lines.append("They hit you for " + str(damage) + " damage!")
		
		else:
			self.in_combat = False
		
		return output_lines