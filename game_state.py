class Game_state():


	def __init__(self, overworld_x, overworld_y,over_world_map):
		self.overworld_x = overworld_x
		self.overworld_y = overworld_y
		self.over_world = over_world_map
		self.current_scene = over_world_map[self.overworld_y][self.overworld_x]



	def update_player_position(self,direction):
		if direction.upper() == 'NORTH':
			self.overworld_y -= 1
		elif direction.upper() == 'EAST':
			self.overworld_x += 1
		elif direction.upper() == 'SOUTH':
			self.overworld_y += 1
		elif direction.upper() == 'WEST':
			self.overworld_x -= 1

		self.update_current_scene()



	def update_current_scene(self):
		self.current_scene = self.over_world[self.overworld_y][self.overworld_x]

	def render_current_scene(self):
		output_lines = self.current_scene.description

		return output_lines 


	def render_npcs(self):
		output_lines = self.current_scene.check_encounter()

		return output_lines

	def check_encounters(self):
		self.current_scene.check_encounter()