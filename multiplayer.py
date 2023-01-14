from pacman import *
from ghosts import *
from maze import *
from client_network import *
import json

vector = pygame.math.Vector2


class multiplayer:
    def __init__(self, player_class):
        self.maze = Maze()
        self.all_sprites = pygame.sprite.Group()
        self.player_class = player_class
        self.client_variable = client()
        player_one = json.loads(self.client_variable.return_data())
        self.player_one = Pacman((player_one[0][0], player_one[0][1]), self.maze, "multiplayer", self)
        self.player_one.update_update_direction((player_one[0][2], player_one[0][3]))
        self.player_one.score = player_one[0][4]
        self.player = player_one[0][5]
        self.time = player_one[1]
        self.is_paused_time = 30 * 120
        self.is_waiting = player_one[2]
        self.player_two = Pacman((294, 350), self.maze, "multiplayer", self)
        self.red_ghost = Ghost([pygame.image.load(os.path.join(ghost_images, "redghost_right_1.png")), pygame.image.load(os.path.join(ghost_images, "redghost_right_2.png"))], [pygame.image.load(os.path.join(ghost_images, "redghost_left_1.png")), pygame.image.load(os.path.join(ghost_images, "redghost_left_2.png"))], [pygame.image.load(os.path.join(ghost_images, "redghost_up_1.png")), pygame.image.load(os.path.join(ghost_images, "redghost_up_2.png"))], [pygame.image.load(os.path.join(ghost_images, "redghost_down_1.png")), pygame.image.load(os.path.join(ghost_images, "redghost_down_2.png"))], red_ghost_starting_position, self.player_one, "red", "multiplayer")
        self.blue_ghost = Ghost([pygame.image.load(os.path.join(ghost_images, "blueghost_right_1.png")), pygame.image.load(os.path.join(ghost_images, "blueghost_right_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blueghost_left_1.png")), pygame.image.load(os.path.join(ghost_images, "blueghost_left_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blueghost_up_1.png")), pygame.image.load(os.path.join(ghost_images, "blueghost_up_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blueghost_down_1.png")), pygame.image.load(os.path.join(ghost_images, "blueghost_down_2.png"))], blue_ghost_starting_position, self.player_one, "blue", "multiplayer")
        self.orange_ghost = Ghost([pygame.image.load(os.path.join(ghost_images, "orangeghost_right_1.png")), pygame.image.load(os.path.join(ghost_images, "orangeghost_right_2.png"))], [pygame.image.load(os.path.join(ghost_images, "orangeghost_left_1.png")), pygame.image.load(os.path.join(ghost_images, "orangeghost_left_2.png"))], [pygame.image.load(os.path.join(ghost_images, "orangeghost_up_1.png")), pygame.image.load(os.path.join(ghost_images, "orangeghost_up_2.png"))], [pygame.image.load(os.path.join(ghost_images, "orangeghost_down_1.png")), pygame.image.load(os.path.join(ghost_images, "orangeghost_down_2.png"))], orange_ghost_starting_position, self.player_one, "orange", "multiplayer")
        self.black_ghost = Ghost([pygame.image.load(os.path.join(ghost_images, "blackghost_right_1.png")), pygame.image.load(os.path.join(ghost_images, "blackghost_right_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blackghost_left_1.png")), pygame.image.load(os.path.join(ghost_images, "blackghost_left_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blackghost_up_1.png")), pygame.image.load(os.path.join(ghost_images, "blackghost_up_2.png"))], [pygame.image.load(os.path.join(ghost_images, "blackghost_down_1.png")), pygame.image.load(os.path.join(ghost_images, "blackghost_down_2.png"))], black_ghost_starting_position, self.player_one, "black", "multiplayer")

        # CREATING NEW INSTANCES OF GHOSTS PACMAN AND MAZE

        self.all_sprites.add(self.red_ghost)
        self.all_sprites.add(self.blue_ghost)
        self.all_sprites.add(self.orange_ghost)
        self.all_sprites.add(self.black_ghost)
        self.all_sprites.add(self.player_one)
        self.all_sprites.add(self.player_two)
        # ADDS ALL SPRITES TO SPRITES LIST

    def event_manager(self):

        ##### event_manager #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Controls entire game events
        ##########################

        if self.is_waiting:
            waiting = json.loads(self.client_variable.send_data(json.dumps("wait")))
            self.is_waiting = waiting
        if not self.is_waiting:
            player_two = json.loads(self.client_variable.send_data(json.dumps((self.player_one.rect.center[0], self.player_one.rect.center[1], int(self.player_one.get_direction()[0]), int(self.player_one.get_direction()[1]), int(self.player_one.get_score()), self.player_one.get_is_paused()))))
            # SENDS OWN DATA TO SERVER AND GETS OTHER PLAYERS DATA AS WELL AS SOME GLOBAL VARIABLES

            self.player_two.rect.center = (player_two[0][0], player_two[0][1])
            self.player_two.update_direction((player_two[0][2], player_two[0][3]))
            self.player_two.update_score(player_two[0][4])
            self.player_two.update_is_paused(player_two[0][6])
            self.time = player_two[2]
            self.player_one.update_level(player_two[6])
            self.player_one.update_is_alive(player_two[4])
            self.player_two.update_is_alive(player_two[4])
            self.player_one.update_lives(player_two[3])
            self.player_one.update_has_started(player_two[7])
            # ASSIGN ALL THE VARIABLES

        # GAME
            if not self.player_one.get_is_paused() and not self.player_two.get_is_paused():

                if not player_two[5]:
                    # IF THE LEVEL IS NOT OVER

                    if player_two[4]:
                        # IF BOTH PLAYERS ARE STILL ALIVE

                        if player_two[7]:

                            self.player_class.movement(self.player_one)
                            # MAKE THE PLAYER MOVE

                        # RED GHOST
                            if player_two[1][0][6]:
                                # IF THE RED GHOST IS FRIGHTENED

                                if self.red_ghost.get_pixel_position() == self.player_one.get_pixel_position() or self.red_ghost.get_pixel_position() == self.player_two.get_pixel_position():
                                    # IF ANY OF THE PLAYERS COLLIDE DURING THE GHOST BEING FRIGHTENED

                                    self.red_ghost.update_is_alive(False)
                                    # RED GHOST IS NO LONGER ALIVE
                                else:
                                    # IF THE PLAYER HAS NOT COLLIDED WITH THE GHOST

                                    if player_two[1][0][7]:
                                        # IF THE RED GHOST IS ALIVE

                                        if (12 * fps) >= self.time:
                                            # IF IT HAS NOT BEEN 12 SECONDS

                                            if self.player == 0:
                                                # IF IT IS PLAYER 0

                                                self.player_zero_function(player_two, (28, 28), self.red_ghost, 0)
                                                # CALCULATE THE SHORTEST PATH TO CORNER AND MOVE THERE

                                            if self.time >= (10 * fps):
                                                # IF THE GHOST HAS 2 SECONDS REMAINING OF BEING FRIGHTENED

                                                self.red_ghost.update_sprite(self.red_ghost.flicker_mode_images, 0.15, 4, 4)
                                                # UPDATE IMAGE TO FLICKER

                                            else:
                                                self.red_ghost.update_sprite(self.red_ghost.frightened_mode_images, 0.15, 4, 4)
                                                # OTHERWISE KEEP IMAGE AS A FRIGHTENED GHOST
                                        else:
                                            # IF ITS PAST 12 SECONDS

                                            if self.player == 0:
                                                # IF IT IS PLAYER 0

                                                self.red_ghost.update_is_frightened(False)
                                                self.player_one.update_score(self.player_one.get_score() + 10)
                                                # GHOST IS NO LONGER FRIGHTENED AND GIVE PLAYER 10 POINTS

                                            if self.player == 1:
                                                # IF IT IS PLAYER 1

                                                self.player_one.update_score(self.player_one.get_score() + 10)
                                                # GIVE PLAYER 10 POINTS

                                    else:
                                        self.red_ghost.is_running(None, self.maze.walls)
                                        # WHEN THE PLAYER HAS EATEN THE GHOST MAKE IT RUN TO THE GHOST CHAMBER
                    # BLUE GHOST

                            if player_two[1][1][6]:
                                # IF THE BLUE GHOST IS FRIGHTENED

                                if self.blue_ghost.get_pixel_position() == self.player_one.get_pixel_position() or self.blue_ghost.get_pixel_position() == self.player_two.get_pixel_position():
                                    # IF ANY OF THE PLAYERS COLLIDE DURING THE GHOST BEING FRIGHTENED

                                    self.blue_ghost.update_is_alive(False)
                                    # GHOST IS NO LONGER ALIVE

                                else:
                                    # IF THE PLAYER HAS NOT COLLIDED WITH THE GHOST

                                    if player_two[1][1][7]:
                                        # IF THE BLUE GHOST IS ALIVE

                                        if (self.player_one.get_score() + self.player_two.get_score()) >= 200:
                                            # IF THE PLAYERS SCORES ARE GREATER THAN OR EQUAL TO 200 COLLECTIVELY

                                            if (12 * fps) >= self.time:
                                                # IF IT HAS NOT BEEN 12 SECONDS

                                                if self.player == 0:
                                                    # IF IT IS PLAYER 0

                                                    self.player_zero_function(player_two, (476, 560), self.blue_ghost, 1)
                                                    # CALCULATE THE SHORTEST PATH TO CORNER AND MOVE THERE

                                                if self.time >= (10 * fps):
                                                    # IF THE GHOST HAS 2 SECONDS REMAINING OF BEING FRIGHTENED

                                                    self.blue_ghost.update_sprite(self.blue_ghost.flicker_mode_images, 0.15, 4, 4)
                                                    # UPDATE IMAGE TO FLICKER

                                                else:
                                                    self.blue_ghost.update_sprite(self.blue_ghost.frightened_mode_images, 0.15, 4, 4)
                                                    # OTHERWISE KEEP IMAGE AS A FRIGHTENED GHOST

                                            else:
                                                # IF ITS PAST 12 SECONDS

                                                if self.player == 0:
                                                    # IF IT IS PLAYER 0

                                                    self.blue_ghost.update_is_frightened(False)
                                                    self.player_one.update_score(self.player_one.get_score() + 10)
                                                    # GHOST IS NO LONGER FRIGHTENED AND GIVE PLAYER 10 POINTS

                                                if self.player == 1:
                                                    # IF IT IS PLAYER 1

                                                    self.player_one.update_score(self.player_one.get_score() + 10)
                                                    # GIVE PLAYER 10 POINTS

                                        else:
                                            self.blue_ghost.update_sprite(self.blue_ghost.right_images, 0.15, 4, 4)
                                            # IF THE GHOST IS NOT ACTIVE GIVE IT THE MOVING RIGHT ANIMATION
                                    else:
                                        if self.player == 0:
                                            # IF IT IS PLAYER 0

                                            closest_player_blue_ghost = self.blue_ghost.closest_distance_calculator((player_two[1][1][0], player_two[1][1][1]),[self.player_one.get_pixel_position(), self.player_two.get_pixel_position()])
                                            self.blue_ghost.is_running(closest_player_blue_ghost, self.maze.walls)
                                            # WHEN THE PLAYER HAS EATEN THE GHOST MAKE IT RUN TO THE GHOST CHAMBER

                    # BLACK GHOST

                            if player_two[1][2][6]:
                                # IF THE BLACK GHOST IS FRIGHTENED

                                if self.black_ghost.get_pixel_position() == self.player_one.get_pixel_position() or self.black_ghost.get_pixel_position() == self.player_two.get_pixel_position():
                                    # IF ANY OF THE PLAYERS COLLIDE DURING THE GHOST BEING FRIGHTENED

                                    self.black_ghost.update_is_alive(False)
                                    # GHOST IS NO LONGER ALIVE

                                else:
                                    # IF THE PLAYER HAS NOT COLLIDED WITH THE GHOST

                                    if player_two[1][2][7]:
                                        # IF THE BLACK GHOST IS ALIVE

                                        if self.player_one.get_level() >= 3:
                                            # IF WE'RE PAST LEVEL 3

                                            if (12 * fps) >= self.time:
                                                # IF WE'RE WITHIN 12 SECONDS

                                                if self.player == 0:
                                                    # IF IT IS PLAYER 0

                                                    self.player_zero_function(player_two, (28, 560), self.black_ghost, 2)
                                                    # CALCULATE THE SHORTEST PATH TO CORNER AND MOVE THERE

                                                if self.time >= (10 * fps):
                                                    # IF THE GHOST HAS 2 SECONDS REMAINING OF BEING FRIGHTENED

                                                    self.black_ghost.update_sprite(self.black_ghost.flicker_mode_images, 0.15, 4, 4)
                                                    # UPDATE IMAGE TO FLICKER

                                                else:
                                                    self.black_ghost.update_sprite(self.black_ghost.frightened_mode_images, 0.15, 4, 4)
                                                    # OTHERWISE KEEP IMAGE AS A FRIGHTENED GHOST

                                            else:
                                                # IF ITS PAST 12 SECONDS

                                                if self.player == 0:
                                                    # IF IT IS PLAYER 0

                                                    self.black_ghost.update_is_frightened(False)
                                                    self.player_one.update_score(self.player_one.get_score() + 10)
                                                    # GHOST IS NO LONGER FRIGHTENED AND GIVE PLAYER 10 POINTS

                                                if self.player == 1:
                                                    # IF IT IS PLAYER 1

                                                    self.player_one.update_score(self.player_one.get_score() + 10)
                                                    # GIVE PLAYER 10 POINTS

                                        else:
                                            self.black_ghost.update_sprite(self.black_ghost.right_images, 0.15, 4, 4)
                                            # IF THE GHOST IS NOT ACTIVE GIVE IT THE MOVING RIGHT ANIMATION

                                    else:
                                        self.black_ghost.is_running(None, self.maze.walls)
                                        # WHEN THE PLAYER HAS EATEN THE GHOST MAKE IT RUN TO THE GHOST CHAMBER

                    # ORANGE GHOST

                            if player_two[1][3][6]:
                                # IF THE ORANGE GHOST IS FRIGHTENED

                                if self.orange_ghost.get_pixel_position() == self.player_one.get_pixel_position() or self.orange_ghost.get_pixel_position() == self.player_two.get_pixel_position():
                                    # IF ANY OF THE PLAYERS COLLIDE DURING THE GHOST BEING FRIGHTENED

                                    self.orange_ghost.update_is_alive(False)
                                    # GHOST IS NO LONGER ALIVE

                                else:
                                    # IF THE PLAYER HAS NOT COLLIDED WITH THE GHOST

                                    if player_two[1][3][7]:
                                        # IF THE ORANGE GHOST IS ALIVE

                                        if self.player_one.get_level() >= 4:
                                            # IF WE HAVE PASSED LEVEL FIVE

                                            if (12 * fps) >= self.time:
                                                # IF IT HAS NOT BEEN 12 SECONDS

                                                if self.player == 0:
                                                    # IF IT IS PLAYER 0

                                                    self.player_zero_function(player_two, (476, 28), self.orange_ghost, 3)
                                                    # CALCULATE THE SHORTEST PATH TO CORNER AND MOVE THERE

                                                if self.time >= (10 * fps):
                                                    # IF THE GHOST HAS 2 SECONDS REMAINING OF BEING FRIGHTENED

                                                    self.orange_ghost.update_sprite(self.orange_ghost.flicker_mode_images, 0.15, 4, 4)
                                                    # UPDATE IMAGE TO FLICKER

                                                else:
                                                    self.orange_ghost.update_sprite(self.orange_ghost.frightened_mode_images, 0.15, 4, 4)
                                                    # OTHERWISE KEEP IMAGE AS A FRIGHTENED GHOST

                                            else:
                                                # IF 12 SECONDS HAS PASSED

                                                if self.player == 0:
                                                    # IF IT IS PLAYER 0

                                                    self.orange_ghost.update_is_frightened(False)
                                                    self.player_one.update_score(self.player_one.get_score() + 10)
                                                    # GHOST IS NO LONGER FRIGHTENED AND GIVE PLAYER 10 POINTS

                                                if self.player == 1:
                                                    # IF IT IS PLAYER 1

                                                    self.player_one.update_score(self.player_one.get_score() + 10)
                                                    # GIVE PLAYER 10 POINTS

                                        else:
                                            self.orange_ghost.update_sprite(self.orange_ghost.right_images, 0.15, 4, 4)
                                            # IF THE GHOST IS NOT ACTIVE GIVE IT THE MOVING RIGHT ANIMATION

                                    else:
                                        self.orange_ghost.is_running(None, self.maze.walls)
                                        # WHEN THE PLAYER HAS EATEN THE GHOST MAKE IT RUN TO THE GHOST CHAMBER

                    # CHECK TO UPDATE MAZE AND SEE IF ANY PLAYER HAS EATEN THE SPECIAL DOT

                            self.dot_check(self.player_one)
                            # CHECK IF PLAYER ONE IS ON AND DOTS OR SPECIAL DOTS

                            self.dot_check(self.player_two)
                            # CHECK IF PLAYER TWO IS ON AND DOTS OR SPECIAL DOTS

                            if self.player == 0:
                                # IF IT IS PLAYER 0

                                closest_player_red_ghost = self.red_ghost.closest_distance_calculator((player_two[1][0][0], player_two[1][0][1]), [self.player_one.get_pixel_position(), self.player_two.get_pixel_position()])
                                closest_player_blue_ghost = self.blue_ghost.closest_distance_calculator((player_two[1][1][0], player_two[1][1][1]), [self.player_one.get_pixel_position(), self.player_two.get_pixel_position()])
                                closest_player_black_ghost = self.black_ghost.closest_distance_calculator((player_two[1][2][0], player_two[1][2][1]), [self.player_one.get_pixel_position(), self.player_two.get_pixel_position()])
                                closest_player_orange_ghost = self.orange_ghost.closest_distance_calculator((player_two[1][3][0], player_two[1][3][1]), [self.player_one.get_pixel_position(), self.player_two.get_pixel_position()])
                                # CALCULATE THE CLOSEST PLAYER TO EACH INDIVIDUAL GHOST

                                if closest_player_orange_ghost == self.player_one.get_pixel_position():
                                    # IF THE CLOSEST PLAYER TO THE ORANGE GHOST IS PLAYER ONE

                                    orange_closest_player = self.player_one
                                    # ASSIGN ORANGE CLOSEST PLAYER AS PLAYER ONE

                                if closest_player_orange_ghost == self.player_two.get_pixel_position():
                                    # IF THE CLOSEST PLAYER TO THE ORANGE GHOST IS PLAYER TWO

                                    orange_closest_player = self.player_two
                                    # ASSIGN ORANGE CLOSEST PLAYER AS PLAYER TWO

                        # RED GHOST MOVEMENT

                                if not player_two[1][0][6]:
                                    # IF THE RED GHOST IS NOT FRIGHTENED

                                    self.pacman_dead_check(self.red_ghost)
                                    # CHECK TO SEE IF A PLAYER HAS COLLIDED WITH GHOST

                                    self.player_zero_function(player_two, closest_player_red_ghost, self.red_ghost, 0)
                                    # FIND SHORTEST PATH TO CLOSEST PLAYER AND MOVE THERE

                        # BLUE GHOST MOVEMENT

                                if not player_two[1][1][6]:
                                    # IF THE BLUE GHOST IS NOT FRIGHTENED

                                    if (self.player_one.get_score() + self.player_two.get_score()) >= 200:
                                        # IF THE SCORE IS GREATER THAN OR EQUAL TO 200 COLLECTIVELY

                                        self.pacman_dead_check(self.blue_ghost)
                                        # CHECK TO SEE IF A PLAYER HAS COLLIDED WITH GHOST

                                        if len(self.maze.special_dots_list) >= 1:
                                            # IF THERE ARE STILL SPECIAL DOTS LEFT IN THE GAME

                                            if self.blue_ghost.closest_distance_calculator(closest_player_blue_ghost, self.maze.special_dots_list) == self.blue_ghost.get_start_pos():
                                                # IF THE DOT THE GHOST IS AIMING FOR IS THE SAME DOT AS BEFORE

                                                if self.blue_ghost.closest_distance_calculator(closest_player_blue_ghost, self.maze.special_dots_list) == self.blue_ghost.get_end_pos():
                                                    # IF THE GHOST HAS ALREADY REACHED THIS DOT

                                                    self.blue_ghost.update_direction(self.blue_ghost.random_movement(self.blue_ghost.get_direction(), self.maze))
                                                    # MOVE RANDOMLY

                                                else:
                                                    self.player_zero_function(player_two, self.blue_ghost.closest_distance_calculator(closest_player_blue_ghost, self.maze.special_dots_list), self.blue_ghost, 1)
                                                    # OTHERWISE MOVE TO THE SPECIAL DOT THAT IS CLOSEST TO THE PLAYER

                                            else:
                                                self.blue_ghost.update_end_pos(None)
                                                # OTHERWISE RESET THE END POSITION

                                                self.player_zero_function(player_two, self.blue_ghost.closest_distance_calculator(closest_player_blue_ghost, self.maze.special_dots_list), self.blue_ghost, 1)
                                                # MOVE TO THE SPECIAL DOT THAT IS CLOSEST TO THE PLAYER

                                            self.blue_ghost.update_start_pos(self.blue_ghost.closest_distance_calculator(closest_player_blue_ghost, self.maze.special_dots_list))
                                            # CALCULATE THE SPECIAL DOT THAT IS CLOSEST TO THE PLAYER AND ASSIGN START POS THAT VALUE

                                        else:
                                            self.blue_ghost.update_direction(self.blue_ghost.random_movement(self.blue_ghost.get_direction(), self.maze))
                                            # IF THERE ARE NO MORE SPECIAL DOTS LEFT JUST MOVE RANDOMLY

                        # BLACK GHOST MOVEMENT

                                if not player_two[1][2][6]:
                                    # IF THE BLACK GHOST IS NOT FRIGHTENED

                                    if self.player_one.get_level() >= 3:
                                        # IF WE ARE ON OR PAST LEVEL THREE

                                        self.pacman_dead_check(self.black_ghost)
                                        # CHECK TO SEE IF A PLAYER HAS COLLIDED WITH GHOST

                                        if self.black_ghost.get_change_mode():
                                            # IF THE BLACK GHOST HAS CHANGED MODE

                                            if self.black_ghost.get_ghost_clock() >= (25 * fps):
                                                # IF 25 SECONDS HAS PASSED (15 SECONDS OF CHASING THE PLAYER)

                                                self.black_ghost.update_change_mode(False)
                                                self.black_ghost.update_ghost_clock(0)
                                                # CHANGE THE GHOST BACK AND RESET THE CLOCK

                                            else:
                                                self.player_zero_function(player_two, closest_player_black_ghost, self.black_ghost, 2)
                                                # OTHERWISE MAKE THE GHOST CHASE THE PLAYER AND CHANGE THE IMAGE

                                        else:
                                            if self.black_ghost.get_ghost_clock() >= (10 * fps):
                                                # IF 10 SECONDS HAS PASSED

                                                self.black_ghost.update_change_mode(True)
                                                # CHANGE MODE

                                            else:
                                                self.black_ghost.update_direction(self.black_ghost.random_movement(self.black_ghost.get_direction(), self.maze))
                                                # OTHERWISE THE GHOST MOVES RANDOMLY

                        # ORANGE GHOST MOVEMENT

                                if not player_two[1][2][6]:
                                    # IF THE ORANGE GHOST IS NOT FRIGHTENED

                                    if self.player_one.get_lives() >= 4:
                                        # IF WE ARE PASSED LEVEL FIVE

                                        if self.orange_ghost.get_ghost_clock() > (10 * fps):
                                            # IF 10 SECONDS HAS PASSED

                                            self.pacman_dead_check(self.orange_ghost)
                                            # CHECK TO SEE IF A PLAYER HAS COLLIDED WITH GHOST

                                            self.player_zero_function(player_two, self.orange_ghost.orange_ghost_movement(closest_player_orange_ghost, self.maze.maze_pixel_list, orange_closest_player), self.orange_ghost, 3)
                                            # MAKE THE GHOST CHASE TWO POSITIONS AHEAD OF PACMAN

                                if len(self.maze.special_dots_list) == 0 and len(self.maze.dots_list) == 0:
                                    # IF THE THERE ARE NO MORE DOTS LEFT IN THE MAZE
                                    self.player_one.update_level_over(True)
                                    self.player_one.update_timer(0)
                                    self.player_one.update_has_started(False)
                                    # THE GAME IS OVER

                                self.player_one.update_timer(self.player_one.get_timer() + 1)
                                # INCREASE TIME BY ONE

                    else:
                        # IF A PLAYER DIES

                        if self.player_one.get_lives() >= 1:
                            # IF THE PLAYERS STILL HAS LIVES REMAINING

                            self.reset(player_two[0][5])
                            # MOVE ALL ENTITIES TO THEIR STARTING POS AND CHANGE DIRECTION TO NEUTRAL

                            self.player_one.update_sprite(self.player_one.death_images, 0.06, 5, 5)
                            self.player_two.update_sprite(self.player_two.death_images, 0.06, 5, 5)
                            # MAKE IMAGE LOOK ANIMATED

                        else:
                            # PLAYER HAS RUN OUT OF LIVES AND THE GAME IS OVER

                            self.red_ghost.update_direction((0, 0))
                            self.blue_ghost.update_direction((0, 0))
                            self.black_ghost.update_direction((0, 0))
                            self.orange_ghost.update_direction((0, 0))
                            self.player_one.update_update_direction((0, 0))
                            self.player_one.update_direction((0, 0))
                            self.player_class.state = "gameover_multiplayer"
                            # FREEZE ALL ENTITIES AND DISPLAY IMAGE ON SCREEN

                else:
                    # IF THE PLAYER COMPLETES THE LEVEL

                    self.reset(player_two[0][5])
                    self.maze.reset()
                    # RESET ALL ENTITIES AND THE MAZE

                if self.player == 0:
                    # IF PLAYER IS PLAYER 0

                    if not self.player_one.get_has_started() and not self.is_waiting and self.player_one.get_lives() >= 1:
                        # IF THE PLAYER HAS NOT STARTED BUT THEY ARE NOT WAITING AND THE PLAYER IS STILL ALIVE

                        self.player_one.update_timer(self.player_one.get_timer() + 1)
                        # INCREASE THE TIME

                        if self.time == 420:
                            # IF IT IS TIME TO START

                            self.player_one.update_timer(0)
                            self.player_one.update_has_started(True)
                            # RESET VARIABLES

                            if not self.player_one.get_is_alive():
                                # IF THE PLAYER DIED

                                self.player_one.reset(multiplayer_starting_positions[player_two[0][5]])
                                self.player_one.update_lives(self.player_one.get_lives() - 1)
                                # RESET VARIABLES

                            if self.player_one.get_level_over():
                                # IF THE LEVEL IS OVER

                                self.player_one.reset(multiplayer_starting_positions[player_two[0][5]])
                                # RESET POSITION
                    self.client_variable.send_data_no_return(json.dumps((((self.red_ghost.get_pixel_position()[0], self.red_ghost.get_pixel_position()[1], self.red_ghost.get_direction()[0], self.red_ghost.get_direction()[1], self.red_ghost.rect.center[0], self.red_ghost.rect.center[1], self.red_ghost.get_is_frightened(), self.red_ghost.get_is_alive(), 0), (self.blue_ghost.get_pixel_position()[0], self.blue_ghost.get_pixel_position()[1], self.blue_ghost.get_direction()[0], self.blue_ghost.get_direction()[1], self.blue_ghost.rect.center[0], self.blue_ghost.rect.center[1], self.blue_ghost.get_is_frightened(), self.blue_ghost.get_is_alive(), 1), (self.black_ghost.get_pixel_position()[0], self.black_ghost.get_pixel_position()[1], self.black_ghost.get_direction()[0], self.black_ghost.get_direction()[1], self.black_ghost.rect.center[0], self.black_ghost.rect.center[1], self.black_ghost.get_is_frightened(), self.black_ghost.get_is_alive(), 2), (self.orange_ghost.get_pixel_position()[0], self.orange_ghost.get_pixel_position()[1], self.orange_ghost.get_direction()[0], self.orange_ghost.get_direction()[1], self.orange_ghost.rect.center[0], self.orange_ghost.rect.center[1], self.orange_ghost.get_is_frightened(), self.orange_ghost.get_is_alive(), 3)), self.player_one.get_timer(), self.player_one.get_lives(), self.player_one.get_level(), self.player_one.get_is_alive(), self.player_one.get_level_over(), self.player_one.get_has_started())))
                    # SEND GHOST DATA AS WELL AS GLOBAL VARIABLES TO THE SERVER

                if self.player == 1:
                    # IF PLAYER 1

                    if not self.player_one.get_has_started() and not self.is_waiting and self.player_one.get_lives() >= 1:
                        # IF THE PLAYER HAS NOT STARTED BUT THEY ARE NOT WAITING AND THE PLAYER IS STILL ALIVE

                        if self.time == 420:
                            # IF IT IS TIME TO START

                            self.player_one.reset(multiplayer_starting_positions[player_two[0][5]])
                            # RESET THE PLAYER

                    self.player_one_function(player_two, self.red_ghost, 0)
                    self.player_one_function(player_two, self.blue_ghost, 1)
                    self.player_one_function(player_two, self.black_ghost, 2)
                    self.player_one_function(player_two, self.orange_ghost, 3)
                    # UPDATE GHOST POSITIONS AND VARIABLES DEPENDING ON DATA FROM SERVER

                if self.is_paused_time != 30 * 120:
                    # IF THE TIME IS INCORRECT

                    self.is_paused_time = 30 * 120
                    # RESET TIME

            else:
                self.red_ghost.force_pause()
                self.red_ghost.update_direction((0, 0))
                self.blue_ghost.force_pause()
                self.blue_ghost.update_direction((0, 0))
                self.black_ghost.force_pause()
                self.black_ghost.update_direction((0, 0))
                self.orange_ghost.force_pause()
                self.orange_ghost.update_direction((0, 0))
                self.player_one.force_pause()
                self.is_paused_time -= 2
                # PAUSE ALL ENTITIES AND REDUCE TIME

                if self.player_one.get_is_paused():
                    # IF THE PLAYER PAUSED THE GAME

                    key_pressed = pygame.key.get_pressed()
                    # GET THE KEY PRESSED

                    if key_pressed[pygame.K_r]:
                        # IF THE PRESS R

                        self.player_one.update_is_paused(False)
                        self.player_one.update_has_started(False)
                        self.client_variable.send_data_no_return(json.dumps((self.player_one.get_has_started(), 0)))
                        # SEND DATA TO DATABASE

                if self.is_paused_time == 0:
                    # IF THEY RUN OUT OF TIME

                    self.player_one.update_is_paused(False)
                    self.player_one.update_has_started(False)
                    self.client_variable.send_data_no_return(json.dumps((self.player_one.get_has_started(), 0)))
                    # SEND DATA TO DATABASE

        self.all_sprites.update()
        # UPDATES ALL SPRITES

    def draw_screen(self, screen, game_background, game_over_image):

        ##### draw_screen #######
        # Parameters : screen:Canvas, game_background:Image, game_over_image, Image
        # Return Type : None
        # Purpose :- Controls entire screen for multiplayer game
        ##########################

        # DRAW SCREEN FUNCTION

        screen.blit(game_background, (11, 0))
        # DRAW GAME MAZE ON SCREEN

        for each_coin in self.maze.dots_list:
            screen.blit(self.player_class.dot_image, (each_coin[0] + 10, each_coin[1] + 10))
        # DRAW ALL THE DOTS ON THE SCREEN

        for each_special_coin in self.maze.special_dots_list:
            screen.blit(self.player_class.special_dot_image, (each_special_coin[0] + 2, each_special_coin[1] + 2))
        # DRAW THE SPECIAL DOTS ON SCREEN

        self.all_sprites.draw(screen)
        # DRAW ALL THE PLAYERS AND GHOSTS

        if self.is_waiting:
            # IF THE GAME HAS NOT STARTED YET

            screen.blit(self.player_class.grey_screen, (0, 0))
            if self.time < 120:
                self.player_class.text(menu_font, 25, LIGHT_BLUE, "Waiting For Player 2.", BLACK, screen, 284, 125)
            if 120 <= self.time < 240:
                self.player_class.text(menu_font, 25, LIGHT_BLUE, "Waiting For Player 2..", BLACK, screen, 283, 125)
            if 240 <= self.time < 360:
                self.player_class.text(menu_font, 25, LIGHT_BLUE, "Waiting For Player 2...", BLACK, screen, 282, 125)
            if self.time == 360:
                self.time = 0
            self.time += 1
            # DRAW ON SCREEN WITH ANIMATED IMAGE

        if not self.player_one.get_has_started() and not self.is_waiting and self.player_one.get_lives() >= 1:
            # IF THE GAME HAST STARTED, THE PLAYER IS NOT WAITING AND THEY STILL HAVE LIVES REMAINING

            if self.time < 120:
                self.player_class.text(menu_font, 20, BLUE, "3", BLACK, screen, 265, 270)
            if 120 <= self.time < 240:
                self.player_class.text(menu_font, 20, BLUE, "2", BLACK, screen, 265, 270)
            if 240 <= self.time < 360:
                self.player_class.text(menu_font, 20, BLUE, "1", BLACK, screen, 265, 270)
            if 360 <= self.time < 420:
                self.player_class.text(menu_font, 20, BLUE, "GO!", BLACK, screen, 265, 270)
            # DRAW 3 2 1 ON THE SCREEN

        self.player_class.text(arialbold_font, 14, WHITE, "LIVES: ", BLACK, screen, 40, 10)
        # LIVES TEXT HEADING ON SCREEN

        self.player_class.draw_lives(65, 20, screen, self.player_one.get_lives(), self.player_one.heart_image)
        # DRAW LIVES AS PACMAN IMAGES

        self.player_class.text(arialbold_font, 14, WHITE, "LEVEL: {} ".format(self.player_one.get_level()), BLACK, screen, screen_width//2, 10)
        # LEVEL TEXT ON SCREEN AS WELL AS LEVEL

        self.player_class.text(arialbold_font, 14, WHITE, "THEIR SCORE: {}".format(self.player_two.get_score()), BLACK, screen, (screen_width-width_buffer)-len("YOUR SCORE: {}".format(self.player_two.get_score()))-30, 610)
        # SCORE TEXT ON SCREEN AS WELL AS SCORE

        self.player_class.text(arialbold_font, 14, WHITE, "MY SCORE: {}".format(self.player_one.get_score()), BLACK, screen, (len("YOUR SCORE: {}".format(self.player_two.get_score())) + 50), 610)
        # SCORE TEXT ON SCREEN AS WELL AS SCORE

        if self.player_one.get_is_paused():
            # IF YOU PAUSED THE GAME

            screen.blit(self.player_class.grey_screen, (0, 0))
            self.player_class.text(menu_font, 25, LIGHT_BLUE, "Press R To Resume Game", BLACK, screen, 284, 125)
            self.player_class.text(arialbold_font, 14, WHITE, "TIME: {} s".format(self.is_paused_time//120), BLACK, screen, (screen_width - width_buffer) - len("TIME: {}".format(self.is_paused_time)) - 20, 10)
            self.player_class.button(202, 131, 368, 35, LIGHT_MAZE_BLUE, DARK_MAZE_BLUE, screen, menu_font, 20, BLACK, "MENU SCREEN", "menu")
            self.player_class.button(202, 131, 436, 35, LIGHT_MAZE_BLUE, DARK_MAZE_BLUE, screen, menu_font, 20, BLACK, "QUIT", "quit")
            # DISPLAY THIS ON SCREEN

        if self.player_two.get_is_paused():
            # IF THE OTHER PLAYER PAUSED THE GAME

            screen.blit(self.player_class.grey_screen, (0, 0))
            self.player_class.text(arialbold_font, 14, WHITE, "TIME: {} s".format(self.is_paused_time//120), BLACK, screen, (screen_width - width_buffer) - len("TIME: {}".format(self.is_paused_time)) - 20, 10)
            self.player_class.text(menu_font, 25, LIGHT_BLUE, "Player 2 Has Paused The Game", BLACK, screen, 284, 125)
            self.player_class.button(202, 131, 368, 35, LIGHT_MAZE_BLUE, DARK_MAZE_BLUE, screen, menu_font, 20, BLACK, "MENU SCREEN", "menu")
            self.player_class.button(202, 131, 436, 35, LIGHT_MAZE_BLUE, DARK_MAZE_BLUE, screen, menu_font, 20, BLACK, "QUIT", "quit")
            # DISPLAY THIS ON SCREEN

        if self.player_class.state == "gameover_multiplayer":
            # IF THE GAME IS OVER

            screen.blit(self.player_class.grey_screen, (0, 0))
            # MAKE THE SCREEN GRAY

            screen.blit(game_over_image, (92, 100))
            # DRAW GAME OVER IMAGE OVER THE GAME

            self.player_class.button(60, 131, 400, 35, WHITE, GRAY, screen, menu_font, 20, BLACK, "MENU SCREEN", "menu")
            # MENU BUTTON

            self.player_class.button(343, 131, 400, 35, WHITE, GRAY, screen, menu_font, 20, BLACK, "QUIT", "quit")
            # PLAY AGAIN BUTTON

        pygame.display.flip()
        # UPDATE DISPLAY

    def player_zero_function(self, input_player, position, ghost, ghost_identifier):

        ##### player_zero_function #######
        # Parameters : input_player:int, position:Tuple, ghost:object, ghost_identifier:int
        # Return Type : None
        # Purpose :- Calculates shortest distance the ghost must travel to its end position
        ##########################

        # FUNCTION FOR PLAYER 0

        ghost.search((0, (input_player[1][ghost_identifier][0], input_player[1][ghost_identifier][1]), (input_player[1][ghost_identifier][0], input_player[1][ghost_identifier][1])), position, self.maze.walls)
        ghost.update_direction(ghost.direction_calculator(ghost.visited, ghost.get_direction(), position, self.maze))
        # FINDS SHORTEST PATH TO A POSITION AND MOVES THERE

    def player_one_function(self, input_player, ghost, ghost_identifier):

        ##### player_one_function #######
        # Parameters : input_player:int, ghost:object, ghost_identifier:int
        # Return Type : None
        # Purpose :- Updates all of the ghost’s variables depending on the data received from the server
        ##########################

        # FUNCTION FOR PLAYER 1

        ghost.update_direction((input_player[1][ghost_identifier][2], input_player[1][ghost_identifier][3]))
        ghost.rect.center = (input_player[1][ghost_identifier][4], input_player[1][ghost_identifier][5])
        ghost.update_is_frightened(input_player[1][ghost_identifier][6])
        ghost.update_is_alive(input_player[1][ghost_identifier][7])
        # UPDATE THE GHOSTS POSITION

    def reset(self, player_id):

        ##### reset #######
        # Parameters : player_id:int
        # Return Type : None
        # Purpose :- Resets all the positions and variables for the ghosts and pacman including their direction
        ##########################

        # RESET FUNCTION

        self.red_ghost.reset(red_ghost_starting_position)
        self.blue_ghost.reset(blue_ghost_starting_position)
        self.black_ghost.reset(black_ghost_starting_position)
        self.orange_ghost.reset(orange_ghost_starting_position)
        self.player_one.update_direction((0, 0))
        self.player_one.update_update_direction((0, 0))
        self.player_one.rect.center = multiplayer_starting_positions[player_id]
        self.player_one.update_pixel_position(vector((self.player_one.rect.each_line // cell_width) * cell_width, (self.player_one.rect.y // cell_width) * cell_width))
        # RESETS ALL ENTITIES TO STARTING POSITIONS AND MAKES THEM STATIONARY

    def reset_game(self, player_id):

        ##### reset_game #######
        # Parameters : player_id:int
        # Return Type : None
        # Purpose :- Entirely reset all the players , ghosts and maze back to default
        ##########################

        # RESET GAME FUNCTION

        self.player_one.reset_game(multiplayer_starting_positions[player_id])
        self.red_ghost.reset_game(red_ghost_starting_position)
        self.blue_ghost.reset_game(blue_ghost_starting_position)
        self.black_ghost.reset_game(black_ghost_starting_position)
        self.orange_ghost.reset_game(orange_ghost_starting_position)
        self.maze.reset()
        # RESETS ALL ENTITIES AND MAZES TO THEIR ORIGINAL VALUE

    def pacman_dead_check(self, ghost):

        ##### pacman_dead_check #######
        # Parameters : ghost:object
        # Return Type : None
        # Purpose :- Checks to see if either of the players have collided with any ghosts.
        ##########################

        # CHECKS IF EITHER PLAYER HAS COLLIDED WITH GHOST

        if self.player_one.get_pixel_position() == ghost.get_pixel_position() or self.player_two.get_pixel_position() == ghost.get_pixel_position():
            # COLLISION WITH GHOST

            self.player_one.update_is_alive(False)
            self.player_one.update_timer(0)
            self.player_one.update_has_started(False)
            # PLAYERS ARE NO LONGER ALIVE AND PLAYER TIMER RESTARTS

    def dot_check(self, player):

        ##### dot_check #######
        # Parameters : player:object
        # Return Type : None
        # Purpose :- Checks if either player has eaten a pac dot or a special dot
        ##########################

    # DOT CHECK FUNCTION

        if player.get_pixel_position() in self.maze.dots_list:
            # IF THE PLAYER IS ON A DOT

            self.maze.dots_list.remove(player.get_pixel_position())
            # REMOVE THAT DOT FROM THE LIST

            player.update_score(player.get_score() + 5)
            # GIVE THEM 5 POINTS

        if player.get_pixel_position() in self.maze.special_dots_list:
            # IF THE PLAYER IS ON A SPECIAL DOT

            self.red_ghost.update_is_frightened(True)
            self.blue_ghost.update_is_frightened(True)
            self.black_ghost.update_is_frightened(True)
            self.orange_ghost.update_is_frightened(True)
            # MAKE ALL GHOSTS FRIGHTENED AND RESET HIS TIMER

            self.maze.special_dots_list.remove(player.get_pixel_position())
            # REMOVE SPECIAL DOT FROM LIST

            player.update_score(player.get_score() + 20)
            # GIVES PLAYER 20 POINTS

            self.player_one.update_timer(0)
            self.player_two.update_timer(0)
            # SETS TIME TO 0
