class NPC():
	def __init__(self, name, description='A NPC', hostile=False, dialog = [], rumor = [], goods = [],hp=10, image = None,damage=[2,5]):
		self.name = name
		self.description = description
		self.hostile = hostile
		self.max_hp = hp
		self.hp = hp
		self.dialog = dialog
		self.rumor = rumor
		self.goods = goods
		self.image = image
		self.damage = damage

	