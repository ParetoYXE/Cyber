import pygame, json, os,copy
from game_state import *
from npc import *
from scene import *
from building import *
from room import *
from pygame.locals import *
from crt_shader import Graphic_engine
from settings import *

# pygame initialize
pygame.init()
clock = pygame.time.Clock()

# Create a display surface and initialize OpenGL
display = pygame.display.set_mode(REAL_RES, DOUBLEBUF|OPENGL)
screen = pygame.Surface(VIRTUAL_RES).convert((255, 65282, 16711681, 0))

# Init shader class
crt_shader = Graphic_engine(screen)

height = VIRTUAL_RES[1] - 100
# Terminal variables
input_text = ''
output_lines = []

# Create a font
font = pygame.font.Font(None, 24)

# Player stats dictionary
player_stats = {
    "Strength": 20,
    "Dexterity": 15,
    "Intelligence": 17,
    "Constitution":15,
    "Charisma":14,
    "Hit Points": 50,
    "Max_Hit_Points":50,
    "Gold": 25,
    "Food": 50,
    "Inventory":[],
    "Weapon":None,
    "Armor":None
}


# # Load the JSON file
# with open('farmer.json', 'r') as file:
#     farmer_data = json.load(file)

# npc_farmer =  NPC(
#     name=farmer_data['name'],
#     description=farmer_data['description'],
#     dialog=farmer_data.get('dialog', []),
#     rumor=farmer_data.get('rumor', []),
#     goods=farmer_data.get('goods', [])
#     )




Sword_item = {"name":'Short Sword', "type":"Weapon", "damage":4}

player_stats['Inventory'].append(Sword_item)


building_dict = {}



mill_image = pygame.transform.scale(pygame.image.load("Mill_Front.png"),(450,200))
old_mill_room = Room("Main chamber")
old_mill = Building("Mill",rooms=[old_mill_room],image=mill_image)


wood_land_image = pygame.image.load("Wood_land.png")
wood_land_image = pygame.transform.scale(wood_land_image,(450,200))

moorland_image = pygame.transform.scale(pygame.image.load('Moorland.png'),(450,200))

camp_image = pygame.image.load("camp.png")


#Combat Vars
combat_timer = False
combat_lines = []

#Dialog Vars
dialog_lines = []
rumor_lines = []
buy_lines = []
inventory_lines = []
player_attack_lines = []
in_dialog = False
npc_in_dialog = None






def load_npcs_from_folder(folder_path):
    npc_dict = {}

    # Loop through all files in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            # Load the JSON data
            with open(file_path, 'r') as file:
                npc_data = json.load(file)
                
                npc_image = None

                if 'image' in npc_data:
                    npc_image = pygame.image.load(npc_data.get('image'))

                # Create an NPC object
                npc = NPC(
                    name=npc_data['name'],
                    description=npc_data['description'],
                    dialog=npc_data.get('dialog', []),
                    rumor=npc_data.get('rumor', []),
                    goods=npc_data.get('goods', []),
                    hostile=npc_data.get('hostile',False),
                    image=npc_image,
                    hp=npc_data.get('hp',10),
                    damage=npc_data.get('damage')
                )
                
                # Store the NPC object in the dictionary with the name as the key
                npc_dict[npc.name] = npc

    return npc_dict




def load_buildings_from_folder(folder_path):
    buildings_dict = {}

    # Loop through all files in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            # Load the JSON data
            with open(file_path, 'r') as file:
                building_data = json.load(file)

                # Assuming each JSON file contains a single building object
                building_name = building_data['name']


                #Load Image

                building_image = pygame.image.load(building_data['image'])


                # Create a building object (assuming you have a Building class)
                building = Building(
                    name=building_data['name'],
                    description=building_data['description'],
                    image=building_image
                )
                
                # Store the building object in the dictionary
                buildings_dict[building_name] = building

    return buildings_dict

# Function to load all JSON files in the 'scenes' folder and create Scene objects
def load_scenes_from_folder(folder_path, npc_dict):
    scene_dict = {}

    # Loop through all files in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            # Load the JSON data
            with open(file_path, 'r') as file:
                scene_data = json.load(file)
                
                # Get NPC objects from the NPC names in the JSON
                npcs = [npc_dict[npc_name] for npc_name in scene_data.get('npcs', [])]
                
                random_encounter_npcs = []

                for i in scene_data['random_encounters']:
                    random_encounter_npcs.append(npc_dict[i['enemy']])


                scene_image = None

                buildings = []

                if 'buildings' in scene_data:
                    buildings = scene_data['buildings']
                if 'image' in scene_data:
                    scene_image = pygame.transform.scale(pygame.image.load(scene_data['image']),(450,200))


                # Create a Scene object
                scene = Scene(
                    name=scene_data['name'],
                    description=scene_data['description'],
                    npcs=npcs,
                    random_encounters=scene_data['random_encounters'],
                    random_encounter_npcs = random_encounter_npcs,
                    image=scene_image,
                    buildings=buildings
                )

                
                
                # Store the Scene object in the dictionary
                scene_dict[scene.name] = scene

    return scene_dict


def generate_map(scene_dict, grid_size=10):
    scene_names = list(scene_dict.keys())  # Get all available scene names
    game_map = []

    for _ in range(grid_size):
        row = []
        for _ in range(grid_size):
            # Select the default scene name
            selected_scene_name = "Moorland"
            # Deep copy the scene object to ensure it's an independent instance
            row.append(copy.deepcopy(scene_dict[selected_scene_name]))
        game_map.append(row)
    
    return game_map





# Load all NPCs from the 'npcs' folder
npc_folder_path = 'npcs'
npc_dict = load_npcs_from_folder(npc_folder_path)

# Load all Scenes from the 'scenes' folder
scene_folder_path = 'scenes'
scene_dict = load_scenes_from_folder(scene_folder_path, npc_dict)

building_folder_path = 'buildings'
building_dict = load_buildings_from_folder(building_folder_path)


game_map = generate_map(scene_dict, grid_size=10)



game_map[9][4] = scene_dict['Hill_land']
game_map[9][5] = scene_dict['Valley']
game_map[9][6] = scene_dict['Hill_land']
game_map[8][5] = scene_dict['Valley_2']
game_map[7][5] = scene_dict['Old_Mill']



for row in game_map:
    for region in row:
        region.description_index = random.randint(0,len(region.description) - 1)

game_state = Game_state(5,9,game_map)



def handle_event(event):
    global input_text, output_lines

    if event.type == KEYDOWN:
        if event.key == K_RETURN:
            #output_lines.append(input_text)
            parse_input()
            input_text = ''
        elif event.key == K_BACKSPACE:
            input_text = input_text[:-1]
        else:
            input_text += event.unicode




def render_graphics():
    if game_state.current_scene.image == None:
        screen.blit(moorland_image,(100,100))
    else:
        screen.blit(game_state.current_scene.image,(100,100))

    if game_state.current_scene.in_combat:
        npc_image = pygame.transform.scale(game_state.current_scene.npc_combat.image,(125,200))
        screen.blit(npc_image,(275,150))

    if game_state.current_scene.npcs != None:
        for npc in game_state.current_scene.npcs:
            if npc.hp > 0 and npc.hostile == False:
                npc_image = pygame.transform.scale(npc.image,(125,180))
                screen.blit(npc_image,(275,150))





def render_building():
    building = building_dict[game_state.building.name]

    screen.blit(building.image,(100,100))



def render_camp():
    screen.blit(camp_image,(100,100))




def render_terminal():
    global combat_timer, combat_lines, player_attack_lines

    screen.fill((0, 0, 0))

    # Draw a green border around the screen
    pygame.draw.rect(screen, (0, 128, 0), screen.get_rect(), 2)
    output_lines = game_state.render_current_scene(player_stats)




    if(game_state.current_scene.in_combat and combat_timer):
        combat_lines = game_state.current_scene.combat(player_stats)
        player_attack_lines = []
        combat_timer = False

    if(game_state.in_camp):
        output_lines.append("You are in camp. A small fire roars and brings heat and brief comfort.")
    # Render the output lines
    y = 350

    for line in output_lines:
        text_surface = font.render(line, True, (0, 128, 0))
        screen.blit(text_surface, (100, y))
        y += text_surface.get_height()

    for line in combat_lines:
        text_surface = font.render(line, True, (0, 128, 0))
        screen.blit(text_surface, (100, y))
        y += text_surface.get_height()
    for line in player_attack_lines:
        text_surface = font.render(line, True, (0, 128, 0))
        screen.blit(text_surface, (100, y))
        y += text_surface.get_height()

    if dialog_lines != []:
        for line in dialog_lines:
            text_surface = font.render(line, True, (0, 128, 0))
            screen.blit(text_surface, (100, y))
            y += text_surface.get_height()

    if rumor_lines != []:
        for line in rumor_lines:
            text_surface = font.render(line, True, (0, 128, 0))
            screen.blit(text_surface, (100, y))
            y += text_surface.get_height()

    if buy_lines != []:
        for line in buy_lines:
            text_surface = font.render(line, True, (0, 128, 0))
            screen.blit(text_surface, (100, y))
            y += text_surface.get_height()

    if inventory_lines != []:
        for line in inventory_lines:
            text_surface = font.render(line, True, (0, 128, 0))
            screen.blit(text_surface, (100, y))
            y += text_surface.get_height()

    
    # Render the input line
    input_surface = font.render(input_text, True, (0, 128, 0))
    screen.blit(input_surface, (100, height - input_surface.get_height()))


def render_stats(screen, font, stats):
    x = VIRTUAL_RES[0] - 200  # Position the stats on the right side of the screen
    y = 100
    stats["X"] = game_state.overworld_x
    stats["Y"] = game_state.overworld_y
    for key, value in stats.items():
        if key != "Inventory" and key != "Weapon":
            stat_surface = font.render(f"{key}: {value}", True, (0, 128, 0))
            screen.blit(stat_surface, (x, y))
            y += stat_surface.get_height()
        elif key == "Weapon":
            if value != None:
                stat_surface = font.render(f"{key}: {value['name']}", True, (0, 128, 0))
            else:
                stat_surface = font.render(f"{key}: {value}", True, (0, 128, 0))
            
            screen.blit(stat_surface, (x, y))
            y += stat_surface.get_height()

def parse_input():
    global dialog_lines, in_dialog, npc_in_dialog, rumor_lines, buy_lines, inventory_lines, player_attack_lines

    commands = input_text.split(" ")


    if not game_state.current_scene.in_combat:
        if(commands[0].upper() == "MOVE"):
            game_state.in_camp = False
            game_state.update_player_position(commands[1])
            #Once you move you need to reset any dialog/npc interactions
            dialog_lines = []
            rumor_lines = []
            inventory_lines = []
            player_attack_lines = []
            npc_in_dialog = None
            in_dialog = False

    if commands[0].upper() == "ATTACK" and len(commands) > 1:
        for npc in game_state.current_scene.npcs:
            if(commands[1].upper() == npc.name.upper() and npc.hp > 0):
                player_attack_lines = game_state.player_attack(npc,player_stats)

    if commands[0].upper() == "TALK" and len(commands) > 1:
        for npc in game_state.current_scene.npcs:
            if(commands[1].upper() == npc.name.upper()):
                print(npc.dialog)
                dialog_lines = game_state.talk(npc)
                in_dialog = True
                npc_in_dialog = npc

    if commands[0].upper() == "ENTER" and len(commands) > 1:
        if len(commands) > 2:
            building_name = commands[1] + " " + commands[2]
        else:
            building_name = commands[1]


        
        for building in game_state.current_scene.buildings:
            if(building_name.upper() == building.upper()):
                game_state.in_building = True
                print(game_state.building)
                print(building_dict)
                game_state.building = building_dict[building_name]


    if commands[0].upper() == "RUMOR" and in_dialog == True:
        if npc_in_dialog.rumor != []:
            rumor_lines = npc_in_dialog.rumor

    if commands[0].upper() == "BUY" and in_dialog == True:
        if npc_in_dialog.goods != []:
            if len(commands) == 1:
                buy_lines = game_state.buy(npc_in_dialog,player_stats)
            else:
                buy_lines = game_state.buy(npc_in_dialog,player_stats,commands[1])

    if commands[0].upper() == "INVENTORY":
        for i in player_stats["Inventory"]:
            inventory_lines.append(i['name'])
    
    if commands[0].upper() == "EAT" and len(commands) > 1:
        if len(commands) > 2:
            food = commands[1].upper() + " " + commands[2].upper()
        else:
            food = commands[1].upper()

        for item in player_stats["Inventory"]:
            if item['name'].upper() == food and item['type'] == "Food":
                if game_state.in_camp:
                    player_stats['Food'] += item['value']
                    if player_stats['Hit Points'] < player_stats['Max_Hit_Points']:
                        player_stats['Hit Points'] += item['value']
                    player_stats['Inventory'].remove(item)
                else:
                    player_stats['Food'] += item['value']
                    player_stats['Inventory'].remove(item)

    if commands[0].upper() == "EQUIP" and len(commands) > 1:
        if len(commands) == 3:
            item_equip  = commands[1].upper() + " " + commands[2].upper()
        else:
            item_equip = commands[1].upper()

        for item in player_stats['Inventory']:
            if item['name'].upper() == item_equip:
                item_type = item['type']
                if item_type in player_stats:
                    player_stats[item_type] = item

    if commands[0].upper() == "LOOT":
        if len(commands) > 1:
            npc_loot = commands[1]
            for npc in game_state.current_scene.npcs:
                if npc.name.upper() == npc_loot.upper() and npc.hp <= 0:
                    inventory_lines.append("--------------------------------------")
                    inventory_lines.append("You loot " + npc_loot + " and receive")
                    
                    for item in npc.goods:
                        inventory_lines.append(item['name'])
                        player_stats['Inventory'].append(item)
                    inventory_lines.append("--------------------------------------")


        else:
            for npc in game_state.current_scene.npcs:
                if npc.hp <= 0:
                    inventory_lines.append("--------------------------------------")
                    inventory_lines.append("Lootable NPCS")
                    inventory_lines.append(npc.name)
    
    if commands[0].upper() == "CAMP":
        if game_state.current_scene.in_combat == False:
            game_state.in_camp = not game_state.in_camp



        




def game_over_screen():

    screen.fill((0, 0, 0))

    # Draw a green border around the screen
    pygame.draw.rect(screen, (0, 128, 0), screen.get_rect(), 2)


    # Render the output lines
    y = 100
    text_surface = font.render("YOU HAVE DIED.", True, (0, 128, 0))
    screen.blit(text_surface, (100, y))


    # Render the input line
    input_surface = font.render(input_text, True, (0, 128, 0))
    screen.blit(input_surface, (100, height - input_surface.get_height()))


# Define timers
TIMER_1_INTERVAL = 5000  # Timer interval in milliseconds (e.g., 5000ms = 5 seconds)
TIMER_FOOD_CONSUMPTION = 10000
TIMER_RANDOM_ENCOUNTER = 5000



# Initialize timers
timer_1_last_tick = pygame.time.get_ticks()
timer_food_consumption = pygame.time.get_ticks()
timer_random_encounter = pygame.time.get_ticks()




# MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        handle_event(event)




    if not game_state.game_over:

        
        render_terminal()
        render_stats(screen, font, player_stats)
        render_graphics()

        if(game_state.in_building):
            render_building()
        if(game_state.in_camp):
            render_camp()


        # Check timers
        current_time = pygame.time.get_ticks()



        if current_time - timer_1_last_tick >= TIMER_1_INTERVAL:
            combat_timer = True
            timer_1_last_tick = current_time  # Reset the timer

          

        if current_time - timer_food_consumption >= TIMER_FOOD_CONSUMPTION:
            game_state.eat(player_stats)
            timer_food_consumption = current_time

        # if current_time - timer_random_encounter >= TIMER_RANDOM_ENCOUNTER:
        #     game_state.current_scene.random_encounter()
        #     timer_random_encounter = current_time





        #Game logic per scene.
        game_state.current_scene.check_encounter(player_stats)
    else:
        game_over_screen()

    
    # Render the shader
    crt_shader()

    clock.tick(FPS)
