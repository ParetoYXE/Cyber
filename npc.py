class NPC():
	def __init__(self, name, description='A NPC', hostile=False, dialog = [], rumor = []):
		self.name = name
		self.description = description
		self.hostile = hostile
		self.hp = 10
		self.dialog = dialog
		self.rumor = rumor

	