from sprite_object_class import *
import pygame
from pygame import mixer
pygame.init()
vector = pygame.math.Vector2


class Pacman(pygame.sprite.Sprite, moving_object):

    def __init__(self, starting_position, maze, gamemode, gamemode_class):
        super().__init__()
        self.heart_image = pygame.image.load(os.path.join(pacman_images, "pacman_left_1.png"))
        self.heart_image = pygame.transform.scale(self.heart_image, (15, 15))
        self.right_images = [pygame.image.load(os.path.join(pacman_images, "pacman_start_image.png")), pygame.image.load(os.path.join(pacman_images, "pacman_right_1.png")), pygame.image.load(os.path.join(pacman_images, "pacman_right_2.png"))]
        self.left_images = [pygame.image.load(os.path.join(pacman_images, "pacman_start_image.png")), pygame.image.load(os.path.join(pacman_images, "pacman_left_1.png")), pygame.image.load(os.path.join(pacman_images, "pacman_left_2.png"))]
        self.up_images = [pygame.image.load(os.path.join(pacman_images, "pacman_start_image.png")), pygame.image.load(os.path.join(pacman_images, "pacman_up_1.png")), pygame.image.load(os.path.join(pacman_images, "pacman_up_2.png"))]
        self.down_images = [pygame.image.load(os.path.join(pacman_images, "pacman_start_image.png")), pygame.image.load(os.path.join(pacman_images, "pacman_down_1.png")), pygame.image.load(os.path.join(pacman_images, "pacman_down_2.png"))]
        self.death_images = [pygame.image.load(os.path.join(pacman_images, "pacman_start_image.png")), pygame.image.load(os.path.join(pacman_images, "pacman_death_1.png")), pygame.image.load(os.path.join(pacman_images, "pacman_death_2.png")), pygame.image.load(os.path.join(pacman_images, "pacman_death_3.png")), pygame.image.load(os.path.join(pacman_images, "pacman_death_4.png")), pygame.image.load(os.path.join(pacman_images, "pacman_death_5.png")), pygame.image.load(os.path.join(pacman_images, "pacman_death_6.png")), pygame.image.load(os.path.join(pacman_images, "pacman_death_7.png")), pygame.image.load(os.path.join(pacman_images, "pacman_death_8.png")), pygame.image.load(os.path.join(pacman_images, "pacman_death_9.png"))]
        # LOAD IN ANIMATION IMAGES

        self.gamemode = gamemode
        self.maze_class = maze
        self.image_loop = 0
        self.image = self.right_images[self.image_loop]
        self.image = pygame.transform.scale(self.image, (cell_width-5, cell_height-5))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (starting_position[0], starting_position[1])
        self.__pixel_position = vector(starting_position[0] - cell_width//2, starting_position[1]-cell_height//2)
        self.__direction = vector(0, 0)
        self.__update_direction = (0, 0)
        self.__lives = 3
        self.__score = 0
        self.__level = 1
        self.__orientation = None
        self.__timer = 0
        self.__is_alive = True
        self.__level_over = False
        self.__gamemode_class = gamemode_class
        self.__is_paused = False
        self.__has_started = False
        # PACMAN VARIABLES

    def update(self):

        ##### update #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Updates the pacman
        ##########################

        # UPDATE PACMAN FUNCTION

        self.update_pixel_position(vector((self.rect.each_line // cell_width) * cell_width, (self.rect.y // cell_width) * cell_width))
        # UPDATE PACMAN PIXEL POSITION

        if self.gamemode == "singleplayer":
            # IF THE GAMEMODE IS FOR SINGLEPLAYER

            self.sinlgeplayer_update()
            # RUN UPDATE FUNCTION FOR SINGLEPLAYER

        if self.gamemode == "multiplayer":
            # IF THE GAMEMODE IS FOR SINGLEPLAYER

            self.multiplayer_update()
            # RUN UPDATE FUNCTION FOR SINGLEPLAYER

# ANIMATIONS

    def move_right(self):

        ##### move_right #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Update pacman direction to move right
        ##########################

        # MOVE RIGHT

        self.update_direction((1, 0))
        # UPDATE DIRECTION

    def move_left(self):

        ##### move_left #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Update pacman direction to move left
        ##########################

        # MOVE LEFT

        self.update_direction((-1, 0))
        # UPDATE DIRECTION

    def move_up(self):

        ##### move_up #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Update pacman direction to move up
        ##########################

        # MOVE UP

        self.update_direction((0, -1))
        # UPDATE DIRECTION

    def move_down(self):

        ##### move_down #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Update pacman direction to move down
        ##########################

        # MOVE DOWN

        self.update_direction((0, 1))
        # UPDATE DIRECTION

    def reset(self, starting_position):

        ##### reset #######
        # Parameters : starting_position:Tuple
        # Return Type : None
        # Purpose :- Resets position and game variables
        ##########################

        self.rect.center = (starting_position[0], starting_position[1])
        self.update_pixel_position(vector((self.rect.each_line // cell_width) * cell_width, (self.rect.y // cell_width) * cell_width))
        self.update_direction((0, 0))
        self.update_update_direction((0, 0))
        self.update_is_alive(True)
        self.update_orientation(None)
        self.update_timer(0)
        self.update_is_paused(False)
        # RESET ALL POSITIONS AND VARIABLES

        if self.get_level_over():
            # IF THE LEVEL IS OVER

            if self.get_lives() <= 4 and self.get_level() >= 3:
                # IF THE PLAYER HAS LESS THAN 5 LIVES AND IS PAST LEVEL THREE

                self.update_lives(self.get_lives() + 1)
                print("done")
                # GIVE THEM ANOTHER LIFE

            self.update_level(self.get_level() + 1)
            # INCREASE THE PLAYERS LEVEL

            self.update_level_over(False)
            # CHANGE LEVEL OVER VARIABLE BACK TO DEFAULT

    def reset_game(self, starting_position):

        ##### reset_game #######
        # Parameters : starting_position:Tuple
        # Return Type : None
        # Purpose :- Reset entire game back to beginning
        ##########################

        self.reset(starting_position)
        self.image_loop = 0
        self.update_lives(3)
        self.update_score(0)
        self.update_level(1)
        self.update_has_started(False)
        # RESET ALL PLAYER VARIABLES BACK TO DEFAULT

    def sinlgeplayer_update(self):

        ##### singleplayer_update #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Update logic for a singlepayer game
        ##########################

        if self.get_is_alive():
            # IF THE PLAYER IS ALIVE

            self.orientation_images(self.get_direction(), self.right_images, self.left_images, self.up_images, self.down_images, 0.15, 5, 5)
            # UPDATE IMAGE DEPENDING ON ORIENTATION

        if not self.get_is_paused() and self.get_has_started():
            # IF THE PLAYER IS NOT PAUSED AND THE GAME HAS STARTED

            self.move()
            # MOVE THE PLAYER

            if self.get_pixel_position() in self.maze_class.dots_list:
                # IF THE PLAYER COLLIDES WITH A PACDOT

                self.maze_class.dots_list.remove(self.get_pixel_position())
                self.update_score(self.get_score() + 5)
                waka_waka = mixer.Sound(os.path.join(music_folder, "wakawaka.ogg"))
                waka_waka.set_volume(0.15)
                waka_waka.play()
                # PLAY MUSIC AND REMOVE THAT DOT FROM SCREEN

            if self.get_pixel_position() in self.maze_class.special_dots_list:
                # IF THE PLAYER COLLIDES WITH A LARGE PAC DOT

                self.maze_class.special_dots_list.remove(self.get_pixel_position())
                self.update_score(self.get_score() + 20)
                self.__gamemode_class.red_ghost.update_is_frightened(True)
                self.__gamemode_class.blue_ghost.update_is_frightened(True)
                self.__gamemode_class.black_ghost.update_is_frightened(True)
                self.__gamemode_class.orange_ghost.update_is_frightened(True)
                self.update_timer(0)
                # REMOVE THAT DOT FROM THE SCREEN AND MAKE ALL THE GHOST FRIGHTENED

            if self.get_pixel_position() in self.maze_class.fruit_positions:
                # IF THE PLAYER EATS A FRUIT

                self.maze_class.fruit_images.remove(self.maze_class.fruit_images[self.maze_class.fruit_positions.index(self.get_pixel_position())])
                self.maze_class.fruit_positions.remove(self.get_pixel_position())
                self.update_score(self.get_score() + 15)
                # GIVE THEM 15 POINTS AND REMOVE FRUIT FROM SCREEN

            if len(self.maze_class.dots_list) == 0 and len(self.maze_class.special_dots_list) == 0:
                # IF THE PLAYER HAS EATEN ALL THE DOTS

                self.update_level_over(True)
                self.update_has_started(False)
                self.update_timer(0)
                # THE LEVEL IS OVER

    def multiplayer_update(self):

        ##### multiplayer_update #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Update logic for a multiplayer game
        ##########################

        if not self.get_is_paused() and self.get_has_started():
            # IF THE PLAYER IS NOT PAUSED AND THE GAME HAS STARTED

            self.move()
            # MOVE

        # UPDATE ANIMATIONS

        if self.get_is_alive():
            # IF THE PLAYER IS ALIVE

            self.orientation_images(self.get_direction(), self.right_images, self.left_images, self.up_images, self.down_images, 0.15, 5, 5)
            # ANIMATE THEIR IMAGE DEPENDING ON ORIENTATION

    def move(self):

        ##### move #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Move the player on the screen and check for walls
        ##########################

        self.rect.center += vector(self.get_update_direction())
        # MOVE THE PLAYER

        if self.get_direction() == vector(-self.get_update_direction()[0], -self.get_update_direction()[1]):
            # IF THE PLAYER ATTEMPTS TO MOVE IN THE OPPOSITE DIRECTION

            self.update_update_direction(self.get_direction())
            # UPDATE RIGHT AWAY

        if (self.rect.center[0] - cell_width // 2) % cell_width == 0 and (self.rect.center[1] - cell_width // 2) % cell_height == 0:
            # IF THE PLAYER IS IN THE MIDDLE OF THE CELL

            if self.get_direction() != vector(0, 0):
                # IF THEIR DIRECTION IS NOT 0
                tempA, tempB = self.wall_check(self.get_direction(), self.maze_class.walls, self.rect)
                self.update_update_direction(tempA)
                self.update_pixel_position(tempB)
                # RUN WALL CHECK METHOD AND UPDATE DIRECTION

        if self.get_update_direction() == (1, 0):
            self.update_orientation("right")
            # UPDATE ORIENTATION

        elif self.get_update_direction() == (-1, 0):
            self.update_orientation("left")
            # UPDATE ORIENTATION

        elif self.get_update_direction() == (0, -1):
            self.update_orientation("up")
            # UPDATE ORIENTATION

        elif self.get_update_direction() == (0, 1):
            self.update_orientation("down")
            # UPDATE ORIENTATION

    def force_pause(self):

        ##### force_pause #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Stops the player where it is and resets time
        ##########################

        self.rect.center = (self.get_pixel_position()[0] + (cell_width//2), self.get_pixel_position()[1] + (cell_height//2))
        self.update_update_direction((0, 0))
        self.update_timer(0)
        # FREEZE THE PLAYER IN PLACE

    def get_lives(self):

        ##### get_lives #######
        # Parameters : None
        # Return Type : __lives:int
        # Purpose :- Get amount of lives
        ##########################

        return self.__lives

    def update_lives(self, new_lives):

        ##### update_lives #######
        # Parameters : new_lives:int
        # Return Type : None
        # Purpose :- Update __lives variable
        ##########################

        self.__lives = new_lives

    def get_score(self):

        ##### get_score #######
        # Parameters : None
        # Return Type : __score:int
        # Purpose :- Get player score
        ##########################

        return self.__score

    def update_score(self, new_score):

        ##### update_score #######
        # Parameters : new_score:int
        # Return Type : None
        # Purpose :- Update player score
        ##########################

        self.__score = new_score

    def get_level(self):

        ##### get_level #######
        # Parameters : None
        # Return Type : __level:int
        # Purpose :- Get player level
        ##########################

        return self.__level

    def update_level(self, new_level):

        ##### update_level #######
        # Parameters : new_level:int
        # Return Type : None
        # Purpose :- Update player level
        ##########################

        self.__level = new_level

    def get_timer(self):

        ##### get_timer #######
        # Parameters : None
        # Return Type : __timer:int
        # Purpose :- Get player timer variable
        ##########################

        return self.__timer

    def update_timer(self, timer):

        ##### update_timer #######
        # Parameters : timer:int
        # Return Type : None
        # Purpose :- Update player timer variable
        ##########################

        self.__timer = timer

    def get_is_alive(self):

        ##### get_is_alive #######
        # Parameters : None
        # Return Type : __is_alive:Boolean
        # Purpose :- Get is_alive
        ##########################

        return self.__is_alive

    def update_is_alive(self, alive):

        ##### update_is_alive #######
        # Parameters : alive:Boolean
        # Return Type : None
        # Purpose :- Update is_alive variable
        ##########################

        self.__is_alive = alive

    def get_level_over(self):

        ##### get_level_over #######
        # Parameters : None
        # Return Type : __level_over: Boolean
        # Purpose :- Gets level_over variable
        ##########################

        return self.__level_over

    def update_level_over(self, level_over):

        ##### update_level_over #######
        # Parameters : level_over:Boolean
        # Return Type : None
        # Purpose :- Update level_over variable
        ##########################

        self.__level_over = level_over

    def get_is_paused(self):

        ##### get_is_paused #######
        # Parameters : None
        # Return Type : __is_paused:Boolean
        # Purpose :- Get is_paused variable
        ##########################

        return self.__is_paused

    def update_is_paused(self, is_paused):

        ##### update_is_paused #######
        # Parameters : is_paused:Boolean
        # Return Type : None
        # Purpose :- Update is_paused variable
        ##########################

        self.__is_paused = is_paused

    def get_orientation(self):

        ##### get_orientation #######
        # Parameters : None
        # Return Type : __orientation:String
        # Purpose :- Get player orientation
        ##########################

        return self.__orientation

    def update_orientation(self, orientation):

        ##### update_orientation #######
        # Parameters : orientation:String
        # Return Type : None
        # Purpose :- Update orientation variable
        ##########################

        self.__orientation = orientation

    def get_has_started(self):

        ##### get_has_started #######
        # Parameters : None
        # Return Type : has_started:Boolean
        # Purpose :- Get has_started variable
        ##########################

        return self.__has_started

    def update_has_started(self, has_started):

        ##### update_has_started #######
        # Parameters : has_started:Boolean
        # Return Type : None
        # Purpose :- Update has_started variable
        ##########################

        self.__has_started = has_started

    def get_update_direction(self):

        ##### get_update_direction #######
        # Parameters :- None
        # Return Type :- __update_direction:Tuple
        # Purpose :- Get update direction variable
        ##########################

        return self.__update_direction

    def update_update_direction(self, update_direction):

        ##### update_update_direction #######
        # Parameters : update_direction:Tuple
        # Return Type : None
        # Purpose :- Update update_direction variable
        ##########################

        self.__update_direction = update_direction

    def get_direction(self):

        ##### get_direction #######
        # Parameters : None
        # Return Type : __direction:Tuple
        # Purpose :- Get direction variable
        ##########################

        return self.__direction

    def update_direction(self, direction):

        ##### update_direction #######
        # Parameters : direction:Tuple
        # Return Type : None
        # Purpose :- Update direction variable
        ##########################

        self.__direction = direction

    def get_pixel_position(self):

        ##### get_pixel_position #######
        # Parameters : None
        # Return Type : __pixel_position:Tuple
        # Purpose :- Gets pixel_position variable
        ##########################

        return self.__pixel_position

    def update_pixel_position(self, pixel_position):

        ##### update_pixel_position #######
        # Parameters : pixel_position:Tuple
        # Return Type : None
        # Purpose :- Update pixel_position variable
        ##########################

        self.__pixel_position = pixel_position



