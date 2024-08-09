import pygame
from game_state import *
from npc import *
from scene import *
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
    "Cyber":14,
    "Hit Points": 50,
    "Gold": 25,
    "Food": 50,
    "Inventory":[],
    "Weapon":None,
    "Armor":None
}




npc_farmer = NPC('Farmer', 'humble peasent farmer toiling the fields',dialog=["Hello humble traveller."], rumor=["Far to the North there is rumors of a spirit that haunts the forest."],
    goods = [{"name":"Bread", "cost":5, 'type':'Food', 'value':3}])



Sword_item = {"name":'Short Sword', "type":"Weapon"}

player_stats['Inventory'].append(Sword_item)



scene = Scene("You stand on the wide Southern plains. The air is still.", [npc_farmer])
scene_2 = Scene("You've come upon a small woodland sprouting \n out from the prairie grass.")




game_map = [
            
            [scene],

            [scene_2]

            ]

game_state = Game_state(0,0,game_map)



#Combat Vars
combat_timer = False
combat_lines = []

#Dialog Vars
dialog_lines = []
rumor_lines = []
buy_lines = []
inventory_lines = []
in_dialog = False
npc_in_dialog = None

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


def render_terminal():
    global combat_timer, combat_lines

    screen.fill((0, 0, 0))

    # Draw a green border around the screen
    pygame.draw.rect(screen, (0, 128, 0), screen.get_rect(), 2)
    output_lines = game_state.render_current_scene(player_stats)




    if(game_state.current_scene.in_combat and combat_timer):
        combat_lines = game_state.current_scene.combat(player_stats)
        combat_timer = False
    
    # Render the output lines
    y = 100

    for line in output_lines:
        text_surface = font.render(line, True, (0, 128, 0))
        screen.blit(text_surface, (100, y))
        y += text_surface.get_height()

    for line in combat_lines:
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
    x = VIRTUAL_RES[0] - 150  # Position the stats on the right side of the screen
    y = 100
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
    global dialog_lines, in_dialog, npc_in_dialog, rumor_lines, buy_lines, inventory_lines

    commands = input_text.split(" ")


    if not game_state.current_scene.in_combat:
        if(commands[0].upper() == "MOVE"):
            game_state.update_player_position(commands[1])
            #Once you move you need to reset any dialog/npc interactions
            dialog_lines = []
            rumor_lines = []
            inventory_lines = []
            npc_in_dialog = None
            in_dialog = False

    if commands[0].upper() == "ATTACK" and len(commands) > 1:
        for npc in game_state.current_scene.npcs:
            if(commands[1].upper() == npc.name.upper()):
                game_state.player_attack(npc)

    if commands[0].upper() == "TALK" and len(commands) > 1:
        for npc in game_state.current_scene.npcs:
            if(commands[1].upper() == npc.name.upper()):
                print(npc.dialog)
                dialog_lines = game_state.talk(npc)
                in_dialog = True
                npc_in_dialog = npc

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
        inventory_lines.append("--------------------------------------")
        for i in player_stats["Inventory"]:
            inventory_lines.append(i['name'])
        inventory_lines.append("--------------------------------------")

    if commands[0].upper() == "EQUIP" and len(commands) > 1:
        if len(commands) == 3:
            item_equip  = commands[1].upper() + " " + commands[2].upper()
        else:
            item_equip = commands[1].upper()

        print(item_equip)
        for item in player_stats['Inventory']:
            if item['name'].upper() == item_equip:
                item_type = item['type']
                if item_type in player_stats:
                    player_stats[item_type] = item

        




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
# Initialize timers
timer_1_last_tick = pygame.time.get_ticks()
timer_food_consumption = pygame.time.get_ticks()




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




        # Check timers
        current_time = pygame.time.get_ticks()



        if current_time - timer_1_last_tick >= TIMER_1_INTERVAL:
            combat_timer = True
            timer_1_last_tick = current_time  # Reset the timer

        if current_time - timer_food_consumption >= TIMER_FOOD_CONSUMPTION:
            game_state.eat(player_stats)
            timer_food_consumption = current_time



        #Game logic per scene.
        game_state.current_scene.check_encounter(player_stats)
    else:
        game_over_screen()

    
    # Render the shader
    crt_shader()

    clock.tick(FPS)
