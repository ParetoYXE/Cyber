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

# Sample player stats dictionary
player_stats = {
    "Health": 100,
    "Mana": 50,
    "Strength": 20,
    "Agility": 15,
    "Intelligence": 25,
    "Experience": 1200
}



npc_farmer = NPC('Farmer', 'humble peasent farmer toiling the fields')



scene = Scene("You stand on the wide Southern plains. The air is still.", [npc_farmer])
scene_2 = Scene("You've come upon a small woodland sprouting \n out from the prairie grass.")



game_map = [
            
            [scene],

            [scene_2]

            ]

game_state = Game_state(0,0,game_map)




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
    screen.fill((0, 0, 0))

    # Draw a green border around the screen
    pygame.draw.rect(screen, (0, 128, 0), screen.get_rect(), 2)
    output_lines = game_state.render_current_scene()
    output_lines = output_lines.splitlines()
    output_lines_2 = game_state.render_npcs().splitlines()

    # Render the output lines
    y = 100
    for line in output_lines:
        text_surface = font.render(line, True, (0, 128, 0))
        screen.blit(text_surface, (100, y))
        y += text_surface.get_height()
    for line in output_lines_2:
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
        stat_surface = font.render(f"{key}: {value}", True, (0, 128, 0))
        screen.blit(stat_surface, (x, y))
        y += stat_surface.get_height()



def parse_input():
    if not game_state.current_scene.in_combat:
        game_state.update_player_position(input_text)
    

# MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        handle_event(event)

    render_terminal()
    render_stats(screen, font, player_stats)

    # Render the shader
    crt_shader()

    clock.tick(FPS)
