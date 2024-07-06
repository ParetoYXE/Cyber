class Scene():

	def __init__(self, description, npcs = None):
		self.description = description
		self.npcs = npcs
		self.in_combat = False

	def check_encounter(self):
		if self.npcs != None:
			for npc in self.npcs:
				if npc.hp > 0:
					if npc.hostile:
						return self.combat(npc)
					else:
						return "There is a " + npc.description
		else:
			return "You are alone."

	def combat(self,npc):
		self.in_combat = True
		
		return "You are in combat with a " + npc.description