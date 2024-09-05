import random

class Game_state():


	def __init__(self, overworld_x, overworld_y,over_world_map):
		self.overworld_x = overworld_x
		self.overworld_y = overworld_y
		self.over_world = over_world_map
		self.current_scene = over_world_map[self.overworld_y][self.overworld_x]
		self.game_over = False
		self.in_camp = False
		self.in_building = False
		self.building = None


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


	def update_player_position_building(self,direction):
		#TO DO
		#This function needs to be setup so that when the player is moving within a building it will move them to the corresponding room
		#Assuming there is a door to it and it is unlocked.
		pass


	def player_attack(self,npc,player_stats):
		self.current_scene.in_combat = True
		
		self.current_scene.npc_combat = npc

		npc.hostile = True

		damage = random.randint(1, round(player_stats['Strength'] / 5))

		if player_stats['Weapon'] != None:
			damage += player_stats['Weapon']['damage']

		npc.hp -= damage
		

		return ["You hit " + npc.name + " for " + str(damage)]

	def update_current_scene(self):
		self.current_scene = self.over_world[self.overworld_y][self.overworld_x]
		print(self.current_scene.name)
		self.current_scene.random_encounter()


	def render_current_scene(self,player_stats):
		output_lines = []
		output_lines = self.current_scene.description[self.current_scene.description_index].splitlines()

		if player_stats['Hit Points'] <= 0:
			self.game_over = True
		if not self.current_scene.in_combat and self.current_scene.npcs != None:
			for npc in self.current_scene.npcs:
				if(npc.hp > 0):
					output_lines.append("You see a " + npc.description)




		return output_lines 



	def buy(self,npc,player_stats,item_command=None):
		output_lines = []

		if item_command == None:
			output_lines.append("The " + npc.name + " has these goods for sale")
			for item in npc.goods:
				print(item)
				output_lines.append(item['name'] + ": " + str(item['cost']))
		else:
			for item in npc.goods:
				if item['name'].upper() == item_command.upper():
					if player_stats['Gold'] >= item['cost']:
						player_stats['Gold'] -= item['cost']
						player_stats['Inventory'].append(item)
		
		return output_lines

	def talk(self, npc):
		output_lines = []


		if npc.dialog != []:
			output_lines = npc.dialog

		return output_lines


	def eat(self,player_stats):
		if(player_stats['Food'] > 0):
			player_stats['Food'] -= 1
		else:
			player_stats['Hit Points'] -= random.randint(0,1)



	def rumor(self, npc):
		output_lines = []

		if npc.rumors != []:
			output_lines = npc.rumors

	def render_npcs(self):
		output_lines = self.current_scene.check_encounter()

		return output_lines

	def check_encounters(self):
		self.current_scene.check_encounter()

	def camp(self):
		pass