class NPC():
	def __init__(self, name, description='A NPC', hostile=False, dialog = [], rumor = [], goods = [],hp=10):
		self.name = name
		self.description = description
		self.hostile = hostile
		self.hp = hp
		self.dialog = dialog
		self.rumor = rumor
		self.goods = goods

	