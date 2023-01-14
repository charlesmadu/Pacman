import os


game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder, "images")
fonts_folder = os.path.join(game_folder, "fonts")
music_folder = os.path.join(game_folder, "music")
pacman_images = os.path.join(image_folder, "pacman")
ghost_images = os.path.join(image_folder, "ghosts")
fruit_images = os.path.join(image_folder, "fruit")
about_images = os.path.join(image_folder, "about")
# FOLDERS

BLACK = 0, 0, 0
YELLOW = 150, 150, 0
LIGHT_YELLOW = 255, 255, 0
WHITE = 255, 255, 255
GRAY = 170, 170, 170
RED = 150, 0, 0
LIGHT_RED = 255, 0, 0
BLUE = 0, 0, 150
LIGHT_BLUE = 0, 0, 255
GREEN = 0, 150, 0
LIGHT_GREEN = 0, 255, 0
LIGHT_MAZE_BLUE = 0, 128, 248
DARK_MAZE_BLUE = 0, 90, 174
# COLOURS

screen_width = 534
screen_length = 616
width_buffer = 26
length_buffer = 15
# SCREEN SIZE

starting_position_x = 266
starting_position_y = 350
# SINGLEPLAYER STARTING POSITION

multiplayer_starting_positions = [[294, 350], [238, 350]]
# MULTIPLAYER STARTING POSITIONS

red_ghost_starting_position = 252, 224
blue_ghost_starting_position = 224, 280
black_ghost_starting_position = 280, 280
orange_ghost_starting_position = 252, 280
# GHOST STARTING POS

game_title = "Pacman"
# GAME TITLE


menu_font = os.path.join(fonts_folder, "a_font.ttf")
arial_font = os.path.join(fonts_folder, "b_font.ttf")
arialbold_font = os.path.join(fonts_folder, "arial_bold.ttf")
# FONTS


cell_width = 28
cell_height = 28
# CELL WIDTH AND HEIGHT

fps = 120
# FPS


