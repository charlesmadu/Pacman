from pacman import *
from ghosts import *
from maze import *
import sqlite3
import pygame
from pygame import mixer
pygame.init()


class singleplayer:
    def __init__(self, player_class):
        self.all_sprites = pygame.sprite.Group()
        self.maze_class = Maze()
        self.maze_class.random_fruit(self.maze_class.dots_list, self.maze_class.fruit_positions, self.maze_class.fruit_images)
        self.player_class = player_class
        self.pacman = Pacman((starting_position_x, starting_position_y), self.maze_class, "singleplayer", self)
        self.red_ghost = Ghost([pygame.image.load(os.path.join(ghost_images, "redghost_right_1.png")), pygame.image.load(os.path.join(ghost_images, "redghost_right_2.png"))], [pygame.image.load(os.path.join(ghost_images, "redghost_left_1.png")), pygame.image.load(os.path.join(ghost_images, "redghost_left_2.png"))], [pygame.image.load(os.path.join(ghost_images, "redghost_up_1.png")), pygame.image.load(os.path.join(ghost_images, "redghost_up_2.png"))], [pygame.image.load(os.path.join(ghost_images, "redghost_down_1.png")), pygame.image.load(os.path.join(ghost_images, "redghost_down_2.png"))], red_ghost_starting_position, self.pacman, "red", "singleplayer")
        self.blue_ghost = Ghost([pygame.image.load(os.path.join(ghost_images, "blueghost_right_1.png")), pygame.image.load(os.path.join(ghost_images, "blueghost_right_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blueghost_left_1.png")), pygame.image.load(os.path.join(ghost_images, "blueghost_left_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blueghost_up_1.png")), pygame.image.load(os.path.join(ghost_images, "blueghost_up_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blueghost_down_1.png")), pygame.image.load(os.path.join(ghost_images, "blueghost_down_2.png"))], blue_ghost_starting_position, self.pacman, "blue", "singleplayer")
        self.orange_ghost = Ghost([pygame.image.load(os.path.join(ghost_images, "orangeghost_right_1.png")), pygame.image.load(os.path.join(ghost_images, "orangeghost_right_2.png"))], [pygame.image.load(os.path.join(ghost_images, "orangeghost_left_1.png")), pygame.image.load(os.path.join(ghost_images, "orangeghost_left_2.png"))], [pygame.image.load(os.path.join(ghost_images, "orangeghost_up_1.png")), pygame.image.load(os.path.join(ghost_images, "orangeghost_up_2.png"))], [pygame.image.load(os.path.join(ghost_images, "orangeghost_down_1.png")), pygame.image.load(os.path.join(ghost_images, "orangeghost_down_2.png"))], orange_ghost_starting_position, self.pacman, "orange", "singleplayer")
        self.black_ghost = Ghost([pygame.image.load(os.path.join(ghost_images, "blackghost_right_1.png")), pygame.image.load(os.path.join(ghost_images, "blackghost_right_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blackghost_left_1.png")), pygame.image.load(os.path.join(ghost_images, "blackghost_left_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blackghost_up_1.png")), pygame.image.load(os.path.join(ghost_images, "blackghost_up_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blackghost_down_1.png")), pygame.image.load(os.path.join(ghost_images, "blackghost_down_2.png"))], black_ghost_starting_position, self.pacman, "black", "singleplayer")
        # CREATING NEW INSTANCES OF GHOSTS PACMAN AND MAZE

        self.all_sprites.add(self.red_ghost)
        self.all_sprites.add(self.blue_ghost)
        self.all_sprites.add(self.orange_ghost)
        self.all_sprites.add(self.black_ghost)
        self.all_sprites.add(self.pacman)
        # ADDS ALL SPRITES TO SPRITES LIST
        self.play_music_once = True

    # EVENTS
    def event_manager(self):

        ##### event_manager #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Controls entire game events
        ##########################

        if not self.pacman.get_is_paused():
            # IF THE GAME IS NOT PAUSED

            if not self.pacman.get_level_over():
                # IF THE PLAYER HAS NOT EATEN ALL THE DOTS

                if self.pacman.get_is_alive():
                    # IF THE PLAYER IS STILL ALIVE

                    if self.pacman.get_has_started():
                        # IF THE PLAYER HAS STARTED

                        if self.play_music_once:
                            mixer.music.load(os.path.join(music_folder, "background_music.ogg"))
                            mixer.music.play(-1)
                            self.play_music_once = False

                        self.player_class.movement(self.pacman)
                        # MOVE THE PLAYER

                # RED GHOST MOVEMENT

                        if self.red_ghost.get_is_frightened():
                            # IF THE RED GHOST IS FRIGHTENED

                            if self.red_ghost.get_is_alive():
                                # IF THE RED GHOST IS ALIVE

                                if (12*fps) >= self.pacman.get_timer():
                                    # IF IT HASN'T BEEN 12 SECONDS

                                    self.red_ghost.search((0, self.red_ghost.get_pixel_position(), self.red_ghost.get_pixel_position()), (28, 28), self.maze_class.walls)
                                    self.red_ghost.update_direction(self.red_ghost.direction_calculator(self.red_ghost.visited, self.red_ghost.get_direction(), self.pacman.get_pixel_position(), self.maze_class))
                                    # MAKE THE GHOST RUN TO ITS CORNER

                                    if self.pacman.get_timer() >= (10 * fps):
                                        # IF THE GHOST IS IN ITS REMAINING 2 SECONDS OF BEING FRIGHTENED

                                        self.red_ghost.update_sprite(self.red_ghost.flicker_mode_images, 0.15, 4, 4)
                                        # CHANGE THE IMAGE TO MAKE IT FLICKER

                                    else:
                                        self.red_ghost.update_sprite(self.red_ghost.frightened_mode_images, 0.15, 4, 4)
                                        # OR JUST KEEP THE IMAGE AS A FRIGHTENED GHOST

                                else:
                                    self.red_ghost.update_is_frightened(False)
                                    self.pacman.update_score(self.pacman.get_score() + 10)
                                    # ONCE 12 SECONDS HAS PASSED RETURN GHOST TO NORMAL STATE AND GIVE THE PLAYER 10 POINTS

                            else:
                                self.red_ghost.is_running(self.pacman.get_pixel_position(), self.maze_class.walls)
                                # WHEN THE PLAYER HAS EATEN THE GHOST MAKE IT RUN TO THE GHOST CHAMBER

                        if not self.red_ghost.get_is_frightened():
                            # IF THE RED GHOST IS NOT FRIGHTENED

                            self.red_ghost.search((0, self.red_ghost.get_pixel_position(), self.red_ghost.get_pixel_position()), self.pacman.get_pixel_position(), self.maze_class.walls)
                            self.red_ghost.update_direction(self.red_ghost.direction_calculator(self.red_ghost.visited, self.red_ghost.get_direction(), self.pacman.get_pixel_position(), self.maze_class))
                            # CHASE PLAYER

                # BLUE GHOST MOVEMENT

                        if self.blue_ghost.get_is_frightened():
                            # IF THE BLUE GHOST IS FRIGHTENED

                            if self.blue_ghost.get_is_alive():
                                # IF THE BLUE GHOST IS ALIVE

                                if self.pacman.get_score() >= 200:
                                    # IF THE PLAYER HAS GAINED MORE THAT 200 POINTS

                                    if (12 * fps) >= self.pacman.get_timer():
                                        # IF 12 SECONDS HAS NOT PASSED

                                        self.blue_ghost.search((0, self.blue_ghost.get_pixel_position(), self.blue_ghost.get_pixel_position()), (476, 560), self.maze_class.walls)
                                        self.blue_ghost.update_direction(self.blue_ghost.direction_calculator(self.blue_ghost.visited, self.blue_ghost.get_direction(), self.pacman.get_pixel_position(), self.maze_class))
                                        # BLUE GHOST WILL RUN TO ITS CORNER

                                        if self.pacman.get_timer() >= (10 * fps):
                                            # IF THE GHOST IS IN ITS REMAINING 2 SECONDS OF BEING FRIGHTENED

                                            self.blue_ghost.update_sprite(self.blue_ghost.flicker_mode_images, 0.15, 4, 4)
                                            # CHANGE THE IMAGE TO MAKE IT FLICKER

                                        else:
                                            self.blue_ghost.update_sprite(self.blue_ghost.frightened_mode_images, 0.15, 4, 4)
                                            # OR JUST KEEP THE IMAGE AS A FRIGHTENED GHOST

                                    else:
                                        self.blue_ghost.update_is_frightened(False)
                                        self.pacman.update_score(self.pacman.get_score() + 10)
                                        # ONCE 12 SECONDS HAS PASSED RETURN GHOST TO NORMAL STATE AND GIVE THE PLAYER 10 POINTS

                                else:
                                    self.blue_ghost.update_sprite(self.blue_ghost.right_images, 0.15, 4, 4)
                                    # IF THE GHOST HAS NOT BEEN ACTIVATED JUST GIVE A LOOKING RIGHT ANIMATION

                            else:
                                self.blue_ghost.is_running(self.pacman.get_pixel_position(), self.maze_class.walls)
                                # WHEN THE PLAYER HAS EATEN THE GHOST MAKE IT RUN TO THE GHOST CHAMBER

                        if not self.blue_ghost.get_is_frightened():
                            # IF THE BLUE GHOST IS NOT FRIGHTENED

                            if (self.pacman.get_score() >= 200) or self.blue_ghost.get_ghost_clock() >= (25 * fps):
                                # IF THE PLAYER HAS 200 OR MORE POINTS OR 25 SECONDS HAS PASSED

                                if len(self.pacman.maze_class.special_dots_list) >= 1:
                                    # IF THERE ARE STILL SPECIAL DOTS LEFT IN THE GAME

                                    if self.blue_ghost.closest_distance_calculator(self.pacman.get_pixel_position(), self.maze_class.special_dots_list) == self.blue_ghost.get_start_pos():
                                        # IF THE DOT THE GHOST IS AIMING FOR IS THE SAME DOT AS BEFORE

                                        if self.blue_ghost.closest_distance_calculator(self.pacman.get_pixel_position(), self.maze_class.special_dots_list) == self.blue_ghost.get_end_pos():
                                            # IF THE GHOST HAS ALREADY REACHED THIS DOT

                                            self.blue_ghost.update_direction(self.blue_ghost.random_movement(self.blue_ghost.get_direction(), self.maze_class))
                                            # MOVE RANDOMLY

                                        else:
                                            self.blue_ghost.search((0, self.blue_ghost.get_pixel_position(), self.blue_ghost.get_pixel_position()), self.blue_ghost.closest_distance_calculator(self.pacman.get_pixel_position(), self.maze_class.special_dots_list), self.maze_class.walls)
                                            self.blue_ghost.update_direction(self.blue_ghost.direction_calculator(self.blue_ghost.visited, self.blue_ghost.get_direction(), self.pacman.get_pixel_position(), self.maze_class))
                                            # OTHERWISE MOVE TO THE SPECIAL DOT THAT IS CLOSEST TO THE PLAYER

                                    else:
                                        self.blue_ghost.update_end_pos(None)
                                        # OTHERWISE RESET THE END POSITION

                                        self.blue_ghost.search((0, self.blue_ghost.get_pixel_position(), self.blue_ghost.get_pixel_position()), self.blue_ghost.closest_distance_calculator(self.pacman.get_pixel_position(), self.maze_class.special_dots_list), self.maze_class.walls)
                                        self.blue_ghost.update_direction(self.blue_ghost.direction_calculator(self.blue_ghost.visited, self.blue_ghost.get_direction(), self.pacman.get_pixel_position(), self.maze_class))
                                        # MOVE TO THE SPECIAL DOT THAT IS CLOSEST TO THE PLAYER

                                    self.blue_ghost.update_start_pos(self.blue_ghost.closest_distance_calculator(self.pacman.get_pixel_position(), self.maze_class.special_dots_list))
                                    # CALCULATE THE SPECIAL DOT THAT IS CLOSEST TO THE PLAYER AND ASSIGN START POS THAT VALUE

                                else:
                                    self.blue_ghost.update_direction(self.blue_ghost.random_movement(self.blue_ghost.get_direction(), self.maze_class))
                                    # IF THERE ARE NO MORE SPECIAL DOTS LEFT JUST MOVE RANDOMLY

                # BLACK GHOST MOVEMENT

                        if self.black_ghost.get_is_frightened():
                            # IF THE GHOST IS FRIGHTENED

                            if self.black_ghost.get_is_alive():
                                # IF THE BLACK GHOST IS ALIVE

                                if self.pacman.get_level() >= 3:
                                    # IF WE'RE PAST LEVEL 3

                                    if (12 * fps) >= self.pacman.get_timer():
                                        # IF WE'RE WITHIN 12 SECONDS

                                        self.black_ghost.search((0, self.black_ghost.get_pixel_position(), self.black_ghost.get_pixel_position()), (28, 560), self.maze_class.walls)
                                        self.black_ghost.update_direction(self.black_ghost.direction_calculator(self.black_ghost.visited, self.black_ghost.get_direction(), self.pacman.get_pixel_position(), self.maze_class))
                                        # CALCULATE THE SHORTEST DISTANCE TO THE CORNER AND MOVE THERE

                                        if self.pacman.get_timer() >= (10 * fps):
                                            # IF THE GHOST IS IN ITS REMAINING 2 SECONDS OF BEING FRIGHTENED
                                            self.black_ghost.update_sprite(self.black_ghost.flicker_mode_images, 0.15, 4, 4)
                                            # CHANGE THE IMAGE AND MAKE IT FLICKER

                                        else:
                                            # OTHERWISE KEEP IT THE SAME
                                            self.black_ghost.update_sprite(self.black_ghost.frightened_mode_images, 0.15, 4, 4)
                                    else:
                                        # IF ITS PAST 120 SECONDS

                                        self.black_ghost.update_is_frightened(False)
                                        self.pacman.update_score(self.pacman.get_score() + 10)
                                        # STOP THE GHOST FROM BEING FRIGHTENED AND GIVE THE PLAYER 10 POINTS

                                else:
                                    self.black_ghost.update_sprite(self.black_ghost.right_images, 0.15, 4, 4)
                                    # IF THE GHOST IS NOT ACTIVE USE LOOKING RIGHT ANIMATION

                            else:
                                self.black_ghost.is_running(self.pacman.get_pixel_position(), self.maze_class.walls)
                                # WHEN THE PLAYER HAS EATEN THE GHOST MAKE IT RUN TO THE GHOST CHAMBER

                        if not self.black_ghost.get_is_frightened():
                            # IF THE BLACK GHOST IS NOT FRIGHTENED

                            if self.pacman.get_level() >= 3:
                                # IF WE ARE ON OR PAST LEVEL THREE

                                if self.black_ghost.get_change_mode():
                                    # IF THE BLACK GHOST HAS CHANGED MODE

                                    if self.black_ghost.get_ghost_clock() >= (25 * fps):
                                        # IF 25 SECONDS HAS PASSED (15 SECONDS OF CHASING THE PLAYER)

                                        self.black_ghost.update_change_mode(False)
                                        self.black_ghost.update_ghost_clock(0)
                                        # CHANGE THE GHOST BACK AND RESET THE CLOCK

                                        self.black_ghost.update_direction((0, 0))
                                        self.black_ghost.rect.center = (self.black_ghost.get_pixel_position()[0] + (cell_width // 2), self.black_ghost.get_pixel_position()[1] + (cell_height // 2))

                                    else:
                                        self.black_ghost.search((0, self.black_ghost.get_pixel_position(), self.black_ghost.get_pixel_position()), self.pacman.get_pixel_position(), self.maze_class.walls)
                                        self.black_ghost.update_direction(self.black_ghost.direction_calculator(self.black_ghost.visited, self.black_ghost.get_direction(), self.pacman.get_pixel_position(), self.maze_class))
                                        # OTHERWISE MAKE THE GHOST CHASE THE PLAYER AND CHANGE THE IMAGE

                                else:
                                    if self.black_ghost.get_ghost_clock() >= (10 * fps):
                                        # IF 10 SECONDS HAS PASSED

                                        self.black_ghost.update_change_mode(True)
                                        # CHANGE MODE

                                        self.black_ghost.update_direction((0, 0))
                                        self.black_ghost.rect.center = (self.black_ghost.get_pixel_position()[0] + (cell_width // 2), self.black_ghost.get_pixel_position()[1] + (cell_height // 2))

                                    else:
                                        self.black_ghost.update_direction(self.black_ghost.random_movement(self.black_ghost.get_direction(), self.maze_class))
                                        # OTHERWISE THE GHOST MOVES RANDOMLY

                # ORANGE GHOST MOVEMENT

                        if self.orange_ghost.get_is_frightened():
                            # IF THE ORANGE GHOST IS FRIGHTENED

                            if self.orange_ghost.get_is_alive():
                                # IF THE GHOST IS ALIVE

                                if self.pacman.get_level() >= 4:
                                    # IF WE HAVE PASSED LEVEL 4

                                    if (12 * fps) >= self.pacman.get_timer():
                                        # IF 12 SECONDS HAS NOT PASSED

                                        self.orange_ghost.search((0, self.orange_ghost.get_pixel_position(), self.orange_ghost.get_pixel_position()), (476, 28), self.maze_class.walls)
                                        self.orange_ghost.update_direction(self.orange_ghost.direction_calculator(self.orange_ghost.visited, self.orange_ghost.get_direction(), self.pacman.get_pixel_position(), self.maze_class))
                                        # RUN TO GHOST CORNER

                                        if self.pacman.get_timer() >= (10 * fps):
                                            # IF THE GHOST HAS 2 SECONDS REMAINING OF BEING FRIGHTENED

                                            self.orange_ghost.update_sprite(self.orange_ghost.flicker_mode_images, 0.15, 4, 4)
                                            # UPDATE IMAGE TO FLICKER

                                        else:
                                            self.orange_ghost.update_sprite(self.orange_ghost.frightened_mode_images, 0.15, 4, 4)
                                            # OTHERWISE KEEP AS A FRIGHTENED GHOST

                                    else:
                                        # 12 SECONDS HAS PASSED

                                        self.orange_ghost.update_is_frightened(False)
                                        self.pacman.update_score(self.pacman.get_score() + 10)
                                        # GHOST IS NO LONGER FRIGHTENED AND GIVE PLAYER 10 POINTS

                                else:
                                    self.orange_ghost.update_sprite(self.orange_ghost.right_images, 0.15, 4, 4)
                                    # IF THE GHOST HAS NOT BEEN ACTIVATED GIVE IT THE MOVING RIGHT ANIMATION

                            else:
                                self.orange_ghost.is_running(self.pacman.get_pixel_position(), self.maze_class.walls)
                                # WHEN THE PLAYER HAS EATEN THE GHOST MAKE IT RUN TO THE GHOST CHAMBER

                        if not self.orange_ghost.get_is_frightened():
                            # IF THE ORANGE GHOST IS NOT FRIGHTENED

                            if self.pacman.get_level() >= 4:
                                # IF WE ARE PAST LEVEL 3

                                if self.orange_ghost.get_ghost_clock() > (0 * fps):
                                    # IF 10 SECONDS HAS PASSED

                                    self.orange_ghost.search((0, self.orange_ghost.get_pixel_position(), self.orange_ghost.get_pixel_position()), self.orange_ghost.orange_ghost_movement(self.pacman.get_pixel_position(), self.maze_class.maze_pixel_list, self.pacman), self.maze_class.walls)
                                    self.orange_ghost.update_direction(self.orange_ghost.direction_calculator(self.orange_ghost.visited, self.orange_ghost.get_direction(), self.pacman.get_pixel_position(), self.maze_class))
                                    # MAKE THE GHOST CHASE TWO POSITIONS AHEAD OF PACMAN

                        self.pacman.update_timer(self.pacman.get_timer() + 1)
                        # ADD ONE TO PLAYER TIMER

                else:
                    # IF THE PLAYER DIES

                    if self.pacman.get_lives() >= 1:
                        # IF THE PLAYER STILL HAS LIVES REMAINING

                        self.reset()
                        # MOVE ALL ENTITIES TO THEIR STARTING POS AND CHANGE DIRECTION TO NEUTRAL

                        if self.pacman.get_timer() <= 420:
                            # IF THE ANIMATION HAS NOT RUN LONG ENOUGH RUN AGAIN

                            self.pacman.update_sprite(self.pacman.death_images, 0.06, 5, 5)
                            # MAKE IMAGE LOOK ANIMATED

                    else:
                        # PLAYER HAS RUN OUT OF LIVES AND THE GAME IS OVER
                        self.red_ghost.update_direction((0, 0))
                        self.blue_ghost.update_direction((0, 0))
                        self.black_ghost.update_direction((0, 0))
                        self.orange_ghost.update_direction((0, 0))
                        self.pacman.update_update_direction((0, 0))
                        self.pacman.update_direction((0, 0))
                        # FREEZE ALL ENTITIES
                        database = sqlite3.connect("database/players.db")
                        # CONNECT TO DATABASE

                        cursor = database.cursor()
                        # CREATE CURSOR
                        try:
                            get_score = 'SELECT highscore FROM user WHERE username = ?'
                            # SQL QUERY TO GET PLAYERS SCORE

                            cursor.execute(get_score, [self.player_class.login.username])
                            # GETS PLAYERS SCORE

                            if cursor.fetchall()[0][0] < self.pacman.get_score():
                                # IF THE PLAYERS GAME SCORE IS GREATER THAN THE ONE ON THE DATABASE

                                update_data = 'UPDATE user SET highscore = ? WHERE username = ?;'
                                # SQL QUERY TO UPDATE THEIR SCORE

                                cursor.execute(update_data, [self.pacman.get_score(), self.player_class.login.username])
                                # EXECUTE SQL QUERY AND UPDATE SCORE
                        except:
                            print("UNABLE TO SAVE DATA AN UNNEXPECTED ERROR OCCURED")

                        database.commit()
                        # CLOSE DATABASE CONNECTION

                        cursor.close()
                        # CLOSE CURSOR

                        self.player_class.state = "gameover_singleplayer"
                        # DISPLAY IMAGE ON SCREEN

            else:
                # IF THE PLAYER COMPLETES THE LEVEL

                self.reset()
                self.maze_class.reset()
                # RESET ALL ENTITIES AND THE MAZE
        else:
            mixer.music.stop()
            self.play_music_once = True
            self.red_ghost.force_pause()
            self.blue_ghost.force_pause()
            self.blue_ghost.force_pause()
            self.orange_ghost.force_pause()
            self.pacman.force_pause()

        self.all_sprites.update()
        # UPDATE ALL SPRITES

# DRAWING SCREEN

    def draw_screen(self, screen, game_background, game_over_image):

        ##### draw_screen #######
        # Parameters : screen:Canvas, game_background:Image, game_over_image, Image
        # Return Type : None
        # Purpose :- Controls entire screen for singleplayer game
        ##########################

        screen.fill(BLACK)

        screen.blit(game_background, (11, 0))
        # DRAW GAME MAZE ON SCREEN

        for each_coin in self.maze_class.dots_list:
            screen.blit(self.player_class.dot_image, (each_coin[0] + 10, each_coin[1] + 10))
        # DRAW ALL THE DOTS ON THE SCREEN

        for each_special_coin in self.maze_class.special_dots_list:
            screen.blit(self.player_class.special_dot_image, (each_special_coin[0] + 2, each_special_coin[1] + 2))
        # DRAW THE SPECIAL DOTS ON SCREEN

        for each_fruit in self.maze_class.fruit_positions:
            fruit_im = pygame.transform.scale(self.player_class.fruit_images[self.maze_class.fruit_images[self.maze_class.fruit_positions.index(each_fruit)]], (15, 15))
            screen.blit(fruit_im, (each_fruit[0] + 4, each_fruit[1] + 5))
        # DRAW FRUIT ON SCREEN

        x_value = 460
        for each_image in self.maze_class.fruit_images:
            image = pygame.transform.scale(self.player_class.fruit_images[each_image], (10, 10))
            screen.blit(image, (x_value, 604))
            x_value += 15
        # DRAW THE ACCORDING FRUIT

        self.all_sprites.draw(screen)
        # DRAW ALL THE PLAYERS AND GHOSTS

        if not self.pacman.get_has_started() and self.pacman.get_lives() >= 1:
            # IF THE GAME HAST STARTED, THE PLAYER IS NOT WAITING AND THEY STILL HAVE LIVES REMAINING

            self.pacman.update_timer(self.pacman.get_timer() + 1)
            # INCREASE THEIR TIME

            if self.pacman.get_timer() < 120:
                self.player_class.text(menu_font, 20, WHITE, "3", BLACK, screen, 265, 270)
            if 120 <= self.pacman.get_timer() < 240:
                self.player_class.text(menu_font, 20, WHITE, "2", BLACK, screen, 265, 270)
            if 240 <= self.pacman.get_timer() < 360:
                self.player_class.text(menu_font, 20, WHITE, "1", BLACK, screen, 265, 270)
            if 360 <= self.pacman.get_timer() < 420:
                self.player_class.text(menu_font, 20, WHITE, "GO!", BLACK, screen, 265, 270)
            if self.pacman.get_timer() == 420:
                # TIME TO START

                if not self.pacman.get_is_alive():
                    # IF THE PLAYER HAD DIED

                    self.pacman.reset((starting_position_x, starting_position_y))
                    self.pacman.update_lives(self.pacman.get_lives() - 1)
                    self.play_music_once = True
                    # PLAYER LOSES A LIFE RESET PLAYER

                if self.pacman.get_level_over():
                    # IF THE PLAYER COMPLETED THE LEVEL

                    self.pacman.reset((starting_position_x, starting_position_y))
                    self.maze_class.random_fruit(self.maze_class.dots_list, self.maze_class.fruit_positions, self.maze_class.fruit_images)
                    self.play_music_once = True
                    # RESET POSITIONS AND MAZE

                self.pacman.update_timer(0)
                self.pacman.update_has_started(True)
                # UPDATE VARIABLES

        self.player_class.text(arialbold_font, 14, WHITE, "LIVES: ", BLACK, screen, 40, 10)
        # LIVES TEXT HEADING ON SCREEN

        self.player_class.text(arialbold_font, 14, WHITE, "SCORE: {}".format(self.pacman.get_score()), BLACK, screen, (screen_width-width_buffer)-len("SCORE: {}".format(self.pacman.get_score()))-20, 10)
        # SCORE TEXT ON SCREEN AS WELL AS SCORE

        self.player_class.draw_lives(65, 20, screen, self.pacman.get_lives(), self.pacman.heart_image)
        # DRAW LIVES AS PACMAN IMAGES

        self.player_class.text(arialbold_font, 14, WHITE, "LEVEL: {} ".format(self.pacman.get_level()), BLACK, screen, screen_width//2, 10)
        # LEVEL TEXT ON SCREEN AS WELL AS LEVEL

        if self.player_class.state == "gameover_singleplayer":
            # IF THE GAME IS OVER
            mixer.music.stop()
            # STOP MUSIC
            self.play_music_once = True
            screen.blit(self.player_class.grey_screen, (0, 0))
            # MAKE THE SCREEN GRAY

            screen.blit(game_over_image, (92, 100))
            # DRAW GAME OVER IMAGE OVER THE GAME

            self.player_class.button(60, 131, 400, 35, WHITE, GRAY, screen, menu_font, 20, BLACK, "MENU SCREEN", "menu")
            # MENU BUTTON

            self.player_class.button(343, 131, 400, 35, WHITE, GRAY, screen, menu_font, 20, BLACK, "PLAY AGAIN", "singleplayer")
            # PLAY AGAIN BUTTON

            if self.player_class.state != "gameover_singleplayer":
                self.reset_game()
                # RESET ALL ENTITIES AND MAZE

        if self.pacman.get_is_paused():
            # IF THE PLAYER PAUSED THE GAME

            screen.blit(self.player_class.grey_screen, (0, 0))
            self.player_class.button(202, 131, 300, 35, LIGHT_MAZE_BLUE, DARK_MAZE_BLUE, screen, menu_font, 20, BLACK, "MENU SCREEN", "menu")
            self.player_class.button(202, 131, 368, 35, LIGHT_MAZE_BLUE, DARK_MAZE_BLUE, screen, menu_font, 20, BLACK, "RESUME GAME", "resume")
            self.player_class.button(202, 131, 436, 35, LIGHT_MAZE_BLUE, DARK_MAZE_BLUE, screen, menu_font, 20, BLACK, "QUIT", "quit")
            # DRAW ON SCREEN

            key_pressed = pygame.key.get_pressed()
            # GET KEY PRESSED

            if key_pressed[pygame.K_r] or self.player_class.state == "resume":
                # IF THE PLAYER PRESSES RESUME OR R

                self.player_class.state = "singleplayer"
                self.pacman.update_is_paused(False)
                self.pacman.update_has_started(False)
                # RESUME GAME

            if self.player_class.state == "menu":
                # IF THE PLAYER WANTS TO GO TO THE MENU

                pygame.mixer.stop()
                self.reset_game()
                # STOP MUSIC AND RESET GAME

        pygame.display.flip()
        # UPDATE THE SCREEN

    def reset(self):

        ##### reset #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Resets all entities to their starting positions
        ##########################

        # RESET FUNCTION

        mixer.music.stop()
        self.red_ghost.reset(red_ghost_starting_position)
        self.blue_ghost.reset(blue_ghost_starting_position)
        self.black_ghost.reset(black_ghost_starting_position)
        self.orange_ghost.reset(orange_ghost_starting_position)
        self.pacman.update_direction((0, 0))
        self.pacman.update_update_direction((0, 0))
        self.pacman.rect.center = ((starting_position_x, starting_position_y))
        self.pacman.update_pixel_position(vector((self.pacman.rect.each_line // cell_width) * cell_width, (self.pacman.rect.y // cell_width) * cell_width))
        # RESETS ALL ENTITIES TO STARTING POSITIONS AND MAKES THEM   STATIONARY

    def reset_game(self):
        ##### reset_game #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Resets entire game back to the start
        ##########################

        # RESET GAME FUNCTION

        self.pacman.reset_game((starting_position_x, starting_position_y))
        self.red_ghost.reset_game(red_ghost_starting_position)
        self.blue_ghost.reset_game(blue_ghost_starting_position)
        self.black_ghost.reset_game(black_ghost_starting_position)
        self.orange_ghost.reset_game(orange_ghost_starting_position)
        self.maze_class.reset()
        # RESETS ALL ENTITIES AND MAZES TO THEIR ORIGINAL VALUE


