class Room():
	def __init__(self,name, description = "Its a room", image=None, doors = {}):
		self.name = name
		self.description = description
		self.image = image
		self.doors = doors