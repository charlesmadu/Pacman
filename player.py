from singleplayer import *
from multiplayer import *
import tkinter as tk
from log_in import *
import pygame
pygame.init()


class Player:
    # INITIALIZE GAME
    def __init__(self):
        self.game_loop = True
        self.screen = None
        self.singleplayer = None
        self.multiplayer = None
        self.login = None
        self.clock = pygame.time.Clock()
        self.state = "log_in_screen"
        self.grey_screen = None
        self.menu_background = self.background_load(os.path.join(image_folder, "menu_screen.png"), screen_width, screen_length)
        self.game_background = self.background_load(os.path.join(image_folder, "maze.png"), screen_width - width_buffer, screen_length - length_buffer)
        self.game_over_image = self.background_load(os.path.join(pacman_images, "game_over.png"), 350, 150)
        self.coin_image = pygame.image.load(os.path.join(image_folder, "coins.jpg"))
        self.dot_image = pygame.transform.scale(self.coin_image, (5, 5))
        self.special_dot_image = pygame.transform.scale(self.coin_image, (20, 20))
        self.fruit_images = [pygame.image.load(os.path.join(fruit_images, "a.png")), pygame.image.load(os.path.join(fruit_images, "b.png")), pygame.image.load(os.path.join(fruit_images, "c.png")), pygame.image.load(os.path.join(fruit_images, "d.png")), pygame.image.load(os.path.join(fruit_images, "e.png")), pygame.image.load(os.path.join(fruit_images, "f.png")), pygame.image.load(os.path.join(fruit_images, "g.png")), pygame.image.load(os.path.join(fruit_images, "h.png"))]
        self.wasd = self.background_load(os.path.join(about_images, "wasd.png"), 250, 250)
        self.udlr = self.background_load(os.path.join(about_images, "udlr.jpg"), 200, 200)
        self.red_ghost_image = self.background_load(os.path.join(ghost_images, "redghost_right_1.png"), 30, 30)
        self.blue_ghost_image = self.background_load(os.path.join(ghost_images, "blueghost_right_1.png"), 30, 30)
        self.black_ghost_image = self.background_load(os.path.join(ghost_images, "blackghost_right_1.png"), 30, 30)
        self.white_ghost_image = self.background_load(os.path.join(ghost_images, "whiteghost_right_1.png"), 30, 30)
        self.orange_ghost_image = self.background_load(os.path.join(ghost_images, "orangeghost_right_1.png"), 30, 30)
        self.esc = self.background_load(os.path.join(about_images, "esc.png"), 100, 100)
        # VARIABLES

# EVENT MANAGER
    def close_game_event(self):

        ##### close_game_event #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Close game if close button pressed
        ##########################

        for each_event in pygame.event.get():
            if each_event.type == pygame.QUIT:
                # IF THE PLAYER CLICKS THE CLOSE BUTTON

                self.game_loop = False
                # END LOOP

    def end_program(self):

        ##### end_program #######
        # Parameters : None
        # Return Type : None
        # Purpose :- End program
        ##########################

        self.game_loop = False
        # END LOOP

    def menu_draw_screen(self):

        ##### menu_draw_screen #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Display the menu screen as well as buttons for the user
        ##########################

        self.screen.blit(self.menu_background, (0, 0))
        self.button(100, 131, 300, 35, LIGHT_RED, RED, self.screen, menu_font, 20, BLACK, "SINGLEPLAYER", "singleplayer")
        self.button(257, 131, 368, 35, WHITE, GRAY, self.screen, menu_font, 20, BLACK, "MULTIPLAYER", "multiplayer")
        self.button(40, 131, 460, 35, LIGHT_YELLOW, YELLOW, self.screen, menu_font, 20, BLACK, "LEADERBOARD", "leaderboard")
        self.button(370, 131, 550, 35, LIGHT_GREEN, GREEN, self.screen, menu_font, 20, BLACK, "ABOUT", "about")
        # DRAW ON MENU SCREEN

        pygame.display.flip()

    def log_in_screen(self):

        ##### log_in_screen #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Control the player logging in
        ##########################

        log_in_screen = tk.Tk()
        self.login = Login(log_in_screen)
        # CREATE NEW INSTANCE OF LOG IN

        log_in_screen.protocol("WM_DELETE_WINDOW", self.end_program())
        # IF THE PLAYER CLOSES THE GAME WINDOW

        self.login.screen.mainloop()
        # LOOP THE SCREEN

        if self.login.logged_in:
            # IF THE PLAYER LOGGED IN

            self.screen = pygame.display.set_mode((screen_width, screen_length))
            pygame.display.set_caption(game_title)
            pygame.display.set_icon(pygame.image.load(os.path.join(image_folder, "pacman_image.png")))
            self.singleplayer = singleplayer(self)
            self.multiplayer = multiplayer(self)
            self.state = "menu"
            self.game_loop = True
            self.grey_screen = pygame.Surface((screen_width, screen_length)).convert_alpha()
            self.grey_screen.fill((0, 0, 0, 150))
            # CREATED WINDOW SCREEN

    def singleplayer_event_manager(self):

        ##### singleplayer_event_manager #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Runs singleplayer event manager method
        ##########################

        self.singleplayer.event_manager()

    # DRAWING MAZE
    def singleplayer_draw_screen(self):

        ##### singleplayer_draw_screen #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Runs singleplayer draw screen method
        ##########################

        self.singleplayer.draw_screen(self.screen, self.game_background, self.game_over_image)

    def multiplayer_event_manager(self):

        ##### multiplayer_event_manager #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Runs multiplayer event manager method
        ##########################

        self.multiplayer.event_manager()

    def multiplayer_draw_screen(self):

        ##### multiplayer_draw_screen #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Runs multiplayer draw screen method
        ##########################

        self.multiplayer.draw_screen(self.screen, self.game_background, self.game_over_image)

    def leaderboard_draw_screen(self):

        ##### leaderboard_draw_screen #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Display leaderboard of the top 10 players
        ##########################

        y_pos_odd = 162

        y_pos_even = 202

        self.text(menu_font, 50, WHITE, "TOP SCORES", BLACK, self.screen, screen_width//2, 40)
        # HEADING

        pygame.draw.rect(self.screen, WHITE, (150, 60, 240, 10))
        # UNDERLINE

        pygame.draw.rect(self.screen, WHITE, (0, 100, screen_length, 40))
        pygame.draw.rect(self.screen, GRAY, (0, 140, screen_length, 40))
        pygame.draw.rect(self.screen, WHITE, (0, 180, screen_length, 40))
        pygame.draw.rect(self.screen, GRAY, (0, 220, screen_length, 40))
        pygame.draw.rect(self.screen, WHITE, (0, 260, screen_length, 40))
        pygame.draw.rect(self.screen, GRAY, (0, 300, screen_length, 40))
        pygame.draw.rect(self.screen, WHITE, (0, 340, screen_length, 40))
        pygame.draw.rect(self.screen, GRAY, (0, 380, screen_length, 40))
        pygame.draw.rect(self.screen, WHITE, (0, 420, screen_length, 40))
        pygame.draw.rect(self.screen, GRAY, (0, 460, screen_length, 40))
        pygame.draw.rect(self.screen, WHITE, (0, 500, screen_length, 40))
        pygame.draw.rect(self.screen, BLACK, (90, 100, 3, 570))
        pygame.draw.rect(self.screen, BLACK, (360, 100, 3, 570))
        self.text(menu_font, 24, BLACK, "#", WHITE, self.screen, 34, 122)
        self.text(menu_font, 24, BLACK, "USERNAME", WHITE, self.screen, 230, 122)
        self.text(menu_font, 24, BLACK, "SCORE", WHITE, self.screen, 450, 122)
        # DRAW ON SCREEN

        for each_number in range(1, 10, 2):
            self.text(menu_font, 24, BLACK, "{}".format(each_number), GRAY, self.screen, 34, y_pos_odd)
            y_pos_odd += 80

        for each_number in range(2, 11, 2):
            self.text(menu_font, 24, BLACK, "{}".format(each_number), WHITE, self.screen, 34, y_pos_even)
            y_pos_even += 80

        database = sqlite3.connect("database/players.db")
        # CONNECT TO DATABASE

        db_cursor = database.cursor()
        # CREATE CURSOR

        get_players = 'SELECT username, highscore FROM user ORDER BY highscore DESC'

        db_cursor.execute(get_players)
        # GET ALL PLAYERS IN DATABASE AND ORDER FROM HIGHEST TO LOWEST

        leaderboard_players = db_cursor.fetchall()

        if len(leaderboard_players) > 10:
            # IF THERE ARE MORE THAN 10 PLAYERS IN THE DATABASE

            leaderboard_players = leaderboard_players[:10]
            # GET THE TOP TEN

        y_pos_odd = 162

        y_pos_even = 202

        for each_player in range(0, len(leaderboard_players), 2):
            self.text(menu_font, 24, BLACK, "{}".format(leaderboard_players[each_player][0]), GRAY, self.screen, 215, y_pos_odd)
            self.text(menu_font, 24, BLACK, "{}".format(leaderboard_players[each_player][1]), GRAY, self.screen, 440, y_pos_odd)
            y_pos_odd += 80
        for each_player in range(1, len(leaderboard_players), 2):
            self.text(menu_font, 24, BLACK, "{}".format(leaderboard_players[each_player][0]), WHITE, self.screen, 215, y_pos_even)
            self.text(menu_font, 24, BLACK, "{}".format(leaderboard_players[each_player][1]), WHITE, self.screen, 440, y_pos_even)
            y_pos_even += 80
        self.button(30, 131, 570, 35, WHITE, GRAY, self.screen, menu_font, 20, BLACK, "MENU SCREEN", "menu")
        self.button(380, 131, 570, 35, GRAY, WHITE, self.screen, menu_font, 20, BLACK, "QUIT", "quit")
        # DRAW PLAYERS ON SCREEN

        pygame.display.flip()

    def about_draw_screen(self):

        ##### about_draw_screen #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Screen to show players how to play the game
        ##########################

        self.screen.fill(WHITE)
        self.screen.blit(self.udlr, (290, 20))
        self.screen.blit(self.wasd, (11, 0))
        self.text(menu_font, 25, BLACK, "To move around click these keys", WHITE, self.screen, 280, 200)
        self.screen.blit(self.red_ghost_image, (11, 240))
        self.text(menu_font, 15, BLACK, "The red ghost will follow you around the maze chasing your exact position.", WHITE, self.screen, 280, 250)
        self.screen.blit(self.blue_ghost_image, (11, 300))
        self.text(menu_font, 15, BLACK, "The blue ghost will hover around the closest large pac dot to your location.", WHITE, self.screen, 280, 310)
        self.screen.blit(self.black_ghost_image, (11, 360))
        self.text(menu_font, 13, BLACK, "The black ghost will move around randomly for 10 seconds then turn to the white ghost.", WHITE, self.screen, 290, 370)
        self.screen.blit(self.white_ghost_image, (11, 420))
        self.text(menu_font, 14, BLACK, "The white ghost will chase your exact location for 15 seconds", WHITE, self.screen, 250, 430)
        self.text(menu_font, 14, BLACK, " then turn to the black ghost again.", WHITE, self.screen, 190, 450)
        self.screen.blit(self.orange_ghost_image, (11, 480))
        self.text(menu_font, 15, BLACK, "The orange ghost attemps to cut you off aiming two spaces ahead", WHITE,self.screen, 250, 490)

        self.screen.blit(self.esc, (0, 520))
        self.text(menu_font, 20, BLACK, "Press the esc key to pause the game", WHITE, self.screen, 250, 550)
        self.button(400, 131, 570, 35, WHITE, GRAY, self.screen, menu_font, 20, BLACK, "MENU SCREEN", "menu")
        # DRAW ON SCREEN

        pygame.display.flip()

    def movement(self, player):

        ##### movement #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Controls what happens when user presses certain keys
        ##########################

        key_pressed = pygame.key.get_pressed()
        # GET THE KEY PRESSED

        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            # IF THE PLAYER PRESSES D OR RIGHT

            player.move_right()
            # MOVE RIGHT

        elif key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            # IF THE PLAYER PRESSES LEFT OR A

            player.move_left()
            # MOVE LEFT

        elif key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            # IF THE PLAYER PRESSES W OR UP

            player.move_up()
            # MOVE UP

        elif key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            # IF THE PLAYER PRESSES DOWN OR S

            player.move_down()
            # MOVE DOWN

        elif key_pressed[pygame.K_ESCAPE]:
            # IF THE PLAYER PRESSES ESCAPE TO PAUSE THE GAME

            player.update_is_paused(True)
            # PAUSE GAME

    def draw_lives(self, x_value, increment_value, screen, player_lives, player_heart_image):

        ##### draw_lives #######
        # Parameters :- x_value:int, increment_value:int, screen:Canvas, player_lives:int, player_heart_image:Image
        # Return Type :- None
        # Purpose :- Draws pacman image on screen depending on the amount of lives the player has left
        ##########################

        # FUNCTION THAT DRAWS SMALL PACMAN IMAGES THAT REPRESENT THE AMOUNT OF LIVES THE PLAYER HAS LEFT

        for eachLife in range(0, player_lives):
            # FOR EACH LIFE THAT THE PLAYER HAS

            screen.blit(player_heart_image, (x_value, 2))
            x_value += increment_value
            # DRAW THE PACMAN IMAGE ON THE SCREEN AND INCREASE THE X POSITION OF THE IMAGE

    def background_load(self, photo_name, image_x_length, image_y_length):

        ##### background_load #######
        # Parameters : photo_name:String, image_x_length:int, image_y_length:int
        # Return Type : background:Image
        # Purpose :- Loads in an image and changes image size
        ##########################

        # LOADS IN THE BACKGROUND PHOTO

        background = pygame.image.load(photo_name)
        background = pygame.transform.scale(background, (image_x_length, image_y_length))
        return background

    def text(self, font, size, colour, message, background_colour, screen, x_position, y_position):

        ##### text #######
        # Parameters : font:Font, size:int, colour:Tuple, message:String, background_colour:Tuple, screen:Canvas, x_position:int, y_position:int
        # Return Type : None
        # Purpose :- Writes text on screen
        ##########################

        font_variable = pygame.font.Font(font, size)
        message_variable = font_variable.render(message, True, colour, background_colour)
        text_rectangle = message_variable.get_rect()
        text_rectangle.center = (x_position, y_position)

        screen.blit(message_variable, text_rectangle)
        # DRAW TEXT ON SCREEN

    def button(self, start_x_position, increment_x, start_y_position, increment_y, dark_colour, light_colour, screen, font, font_size, font_colour, message, game_state):

        ##### button #######
        # Parameters :  start_x_position:int, increment_x:int, start_y_position:int, increment_y:int, dark_colour:Tuple, light_colour:Tuple, screen:Canvas, font:Font, font_size:int, font_colour:Tuple, message:String, game_state:String
        # Return Type : None
        # Purpose :- Creates a clickable button on the screen
        ##########################

        mouse = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        if start_x_position + increment_x > mouse[0] > start_x_position and start_y_position + increment_y > mouse[1] > start_y_position:
            pygame.draw.rect(screen, light_colour, (start_x_position, start_y_position, increment_x, increment_y))
            self.text(font, font_size, font_colour, message, light_colour, screen, start_x_position + int(increment_x / 2), start_y_position + int(increment_y / 2))
            if mouse_clicked[0] == 1:
                self.state = game_state
        else:
            pygame.draw.rect(screen, dark_colour, (start_x_position, start_y_position, increment_x, increment_y))
            self.text(font, font_size, font_colour, message, dark_colour, screen, start_x_position + int(increment_x / 2), start_y_position + int(increment_y / 2))

        # CREATE A BUTTON
