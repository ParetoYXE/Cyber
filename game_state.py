import random

class Game_state():


	def __init__(self, overworld_x, overworld_y,over_world_map):
		self.overworld_x = overworld_x
		self.overworld_y = overworld_y
		self.over_world = over_world_map
		self.current_scene = over_world_map[self.overworld_y][self.overworld_x]
		self.game_over = False


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


	def player_attack(self,npc):
		self.current_scene.in_combat = True
		
		self.current_scene.npc_combat = npc

		npc.hostile = True

		npc.hp -= random.randint(1,3)
		
		print("You hit " + npc.name)



	def update_current_scene(self):
		self.current_scene = self.over_world[self.overworld_y][self.overworld_x]



	def render_current_scene(self,player_stats):
		output_lines = []

		output_lines = self.current_scene.description.splitlines()

		if player_stats['Hit Points'] <= 0:
			self.game_over = True
		if not self.current_scene.in_combat and self.current_scene.npcs != None:
			for npc in self.current_scene.npcs:
				if(npc.hp > 0):
					output_lines.append("You see a " + npc.description)



		return output_lines 



	def buy(self,npc,item=None):
		output_lines = []

		if item == None:
			output_lines.append("The " + npc.name + " has these goods for sale")
			for item in npc.goods:
				print(item)
				output_lines.append(item['name'] + ": " + str(item['cost']))

		return output_lines

	def talk(self, npc):
		output_lines = []


		if npc.dialog != []:
			output_lines = npc.dialog

		return output_lines

	def rumor(self, npc):
		output_lines = []

		if npc.rumors != []:
			output_lines = npc.rumors

	def render_npcs(self):
		output_lines = self.current_scene.check_encounter()

		return output_lines

	def check_encounters(self):
		self.current_scene.check_encounter()