class NPC():
	def __init__(self, name, description='A NPC', hostile=True):
		self.name = name
		self.description = description
		self.hostile = hostile
		self.hp = 10

	