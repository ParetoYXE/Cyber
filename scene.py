import random

class Scene():

	def __init__(self, name,description, npcs = None, random_encounters = None, random_encounter_npcs = None):
		self.name = name
		self.description = description
		self.description_index = 0
		self.npcs = npcs
		self.in_combat = False
		self.npc_combat = None
		self.random_encounters = random_encounters
		self.random_encounter_npcs = random_encounter_npcs
		self.random_encounter_trigger = False

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


	def random_encounter(self):
		for i in self.random_encounters:
			check = random.randint(1,100)
			enemy = None
			for j in self.random_encounter_npcs:
				if i['enemy'] == j.name:
					enemy = j
					enemy.hp = enemy.max_hp

			if check <= i['chance']:
				if enemy.hostile:
						self.in_combat = True
						self.npc_combat = enemy
						self.npcs.append(enemy)




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
			self.npc_combat = None
		
		return output_lines