import random
from sprite_object_class import *

vector = pygame.math.Vector2


class Ghost(pygame.sprite.Sprite, moving_object):
    def __init__(self, right_images, left_images, up_images, down_images, starting_position, pacman, colour, gamemode):
        super().__init__()
        # Initialize Sprite Class
        self.right_images = right_images
        self.left_images = left_images
        self.up_images = up_images
        self.down_images = down_images
        self.frightened_mode_images = [pygame.image.load(os.path.join(ghost_images, "frightenedmode_1.png")), pygame.image.load(os.path.join(ghost_images, "frightenedmode_2.png"))]
        self.flicker_mode_images = [pygame.image.load(os.path.join(ghost_images, "frightenedmode_1.png")), pygame.image.load(os.path.join(ghost_images, "frightenedmode_2.png")), pygame.image.load(os.path.join(ghost_images, "ghostdeath_1.png")), pygame.image.load(os.path.join(ghost_images, "ghostdeath_2.png"))]
        self.right_eye = [pygame.image.load(os.path.join(ghost_images, "ge_r.png"))]
        self.left_eye = [pygame.image.load(os.path.join(ghost_images, "ge_l.png"))]
        self.up_eye = [pygame.image.load(os.path.join(ghost_images, "ge_u.png"))]
        self.down_eye = [pygame.image.load(os.path.join(ghost_images, "ge_d.png"))]
        self.white_right = [pygame.image.load(os.path.join(ghost_images, "whiteghost_right_1.png")), pygame.image.load(os.path.join(ghost_images, "whiteghost_right_2.png"))]
        self.white_left = [pygame.image.load(os.path.join(ghost_images, "whiteghost_left_1.png")), pygame.image.load(os.path.join(ghost_images, "whiteghost_left_2.png"))]
        self.white_up = [pygame.image.load(os.path.join(ghost_images, "whiteghost_up_1.png")), pygame.image.load(os.path.join(ghost_images, "whiteghost_up_2.png"))]
        self.white_down = [pygame.image.load(os.path.join(ghost_images, "whiteghost_down_1.png")), pygame.image.load(os.path.join(ghost_images, "whiteghost_down_2.png"))]
        self.image_loop = 0
        self.image = self.right_images[self.image_loop]
        self.image = pygame.transform.scale(self.image, (cell_width - 4, cell_height - 4))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (starting_position[0] + cell_width // 2, starting_position[1] + cell_height // 2)
        self.movement = []
        self.priority_queue = []
        self.visited = []
        self.pacman = pacman
        self.__pixel_position = vector(starting_position)
        self.__direction = (0, 0)
        self.__colour = colour
        self.__old_direction = False
        self.__end_pos = None
        self.__start_pos = None
        self.__ghost_clock = 0
        self.__is_alive = True
        self.__is_frightened = False
        self.__change_mode = None
        self.__gamemode = gamemode
        # GHOST VARIABLES

    def update(self):

        ##### update #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Updates the ghost
        ##########################

        if self.__gamemode == "singleplayer":
            # IF THE GAME MODE IS SINGLEPLAYER

            self.singleplayer_update()
            # RUN THE SINLGEPLAYER UPDATE METHOD

        if self.__gamemode == "multiplayer":
            # IF THE GAME MODE IS MULTIPLAYER

            self.multiplayer_update()
            # RUN MULTIPLAYER METHOD

        self.priority_queue = []
        self.visited = []
        # EMPTY PRIORITY QUEUE AND VISITED LISTS

    def search(self, cell_to_check, end_location, walls):

        ##### search #######
        # Parameters : cell_to_check:List, end_location:Tuple, walls:List
        # Return Type : None
        # Purpose :- Uses A* Search algorithm and recursion to find the path
        ##########################

        if cell_to_check[1] == end_location:
            # IF THE CELL IS THE THE END LOCATION

            if len(self.priority_queue) == 0:
                # IF THERE ARE NO POSITIONS IN PRIORITY QUEUE

                self.visited.append(cell_to_check[1])
                # ADD THIS POSITION TO PRIORITY QUEUE

            else:
                # IF PRIORITY QUEUE IS NOT EMPTY

                for each_position in self.priority_queue:
                    # FOR EACH POSITION IN THE PRIORITY QUEUE

                    self.visited.append(each_position)
                    # ADD THIS POSITION TO VISITED

        else:
            # IF THIS POSITION IS NOT THE END POSITION

            for each_position in self.adjacent_search(cell_to_check, end_location, walls):
                # RUN ADJACENT_SEARCH METHOD AND FOR EACH POSITION YOU GET

                self.priority_queue.append(each_position)
                # ADD THAT POSITION TO PRIORITY QUEUE

            self.priority_queue.sort(reverse=True)
            # SORT THE PRIORITY QUEUE IN SIZE ORDER

            if cell_to_check in self.priority_queue:
                # IF THE POSITION WE HAVE CHECKED IS IN PRIORITY QUEUE

                self.priority_queue.remove(cell_to_check)
                # REMOVE THIS POSITION FROM PRIORITY QUEUE

            self.visited.append(cell_to_check)
            # ADD THIS POSITION TO VISITED LIST

            self.search(self.priority_queue[-1], end_location, walls)
            # RUN THE FUNCTION AGAIN WITH THE CLOSEST POSITION

    def movement_function(self, visited_positions):

        ##### movement_function #######
        # Parameters : visited_position:List
        # Return Type : None
        # Purpose :- Backtracks visiting where each cell came from to find the shortest path
        ##########################

        shortest_path = []
        position = visited_positions[-1]
        shortest_path.append(position[1])
        # ASSIGN VARIABLES

        while position != visited_positions[0]:
            # WHILE THE POSITION IS NOT THE START POSITION

            for each_position in visited_positions:
                # FOR EACH POSITION IN THE VISITED POSITIONS LIST

                if each_position[1] == position[-1]:
                    # IF THE POSITION IS WHERE THE CELL CAME FROM

                    shortest_path.append(each_position[1])
                    # ADD THIS POSITION TO SHORTEST PATH

                    position = each_position
                    # UPDATE POSITION VARIABLE

        return shortest_path

    def direction_calculator(self, visited_positions, direction, position, maze):

        ##### direction_calculator #######
        # Parameters : visited_positions:List, direction:Tuple, position:Tuple, maze:object
        # Return Type : direction:Tuple
        # Purpose :- Calculates the direction the ghost must move in order to get to the player
        ##########################

        if len(visited_positions) == 1:
            # IF THERE IS ONLY ONE POSITION IN VISITED POSITIONS

            if self.__colour == "blue" and self.get_is_frightened() is False and self.get_is_alive():
                # IF THE BLUE GHOST IS NOT FRIGHTENED AND IS ALIVE

                self.update_end_pos(self.closest_distance_calculator(position, self.pacman.maze_class.special_dots_list))
                # UPDATE THE END POS VARIABLE

            else:
                return self.random_movement(direction, maze)
                # OTHERWISE RETURN A RANDOM DIRECTION

        else:
            path = self.movement_function(visited_positions)
            # CALCULATE THE PATH THE GHOST SHOULD TAKE

            if len(path) >= 2:
                # IF THERE ARE MORE THAN TWO POSITIONS THERE

                if (path[-1][0] + (cell_width//2), path[-1][1] + (cell_height//2)) == self.rect.center:
                    # IF THE GHOST IS IN THE CENTER OF THE CELL

                    if path[-2][0] + (cell_width // 2) != self.rect.center[0]:
                        # IF THE GHOST HAS TO MOVE IN THE X AXIS

                        if path[-2][0] + (cell_width // 2) > self.rect.center[0]:
                            # IF THE POSITION IS TO THE RIGHT

                            return 1, 0
                            # MOVE RIGHT

                        elif path[-2][0] + (cell_width // 2) < self.rect.center[0]:
                            # IF THE POSITION IS TO THE LEFT

                            return -1, 0
                            # MOVE LEFT

                    elif path[-2][1] + (cell_width // 2) != self.rect.center[1]:
                        # IF THE GHOST HAS TO MOVE IN THE Y AXIS

                        if path[-2][1] + (cell_width // 2) > self.rect.center[1]:
                            # IF THE POSITION IS DOWN

                            return 0, 1
                            # MOVE DOWN

                        elif path[-2][1] + (cell_width // 2) < self.rect.center[1]:
                            # IF THE POSITION IS UP

                            return 0, -1
                            # MOVE UP
                else:
                    return direction
            else:
                return direction
        return direction

    def orange_ghost_movement(self, position, maze, pacman):

        ##### orange_ghost_movement #######
        # Parameters : position:Tuple, maze:object, pacman:object
        # Return Type : position:Tuple
        # Purpose :- Find the cell two ahead of the player if possible
        ##########################

        if pacman.get_orientation() == "right":
            # IF THE PLAYER IS FACING RIGHT

            if (position[0]+56, position[1]) in maze and (position[0]+56, position[1]) != (224, 280):
                # IF TWO POSITIONS AHEAD OF THEM IS IN THE MAZE

                return int(position[0]+56), int(position[1])
                # RETURN TWO POSITIONS AHEAD OF THEM

            else:
                # OTHERWISE RETURN THEIR EXACT POSITION
                return position
        if pacman.get_orientation() == "left":
            # IF THE PLAYER IS FACING LEFT

            if (position[0]-56, position[1]) in maze and (position[0]-56, position[1]) != (280, 280):
                # IF TWO POSITIONS AHEAD OF THEM IS IN THE MAZE

                return int(position[0]-56), int(position[1])
                # RETURN TWO POSITIONS AHEAD OF THEM

            else:
                return position
                # OTHERWISE RETURN THEIR EXACT POSITION
        if pacman.get_orientation() == "up":
            # IF THE PLAYER IS FACING UP

            if (position[0], position[1]-56) in maze and (position[0], position[1]-56) != (252, 280):
                # IF TWO POSITIONS AHEAD OF THEM IS IN THE MAZE

                return int(position[0]), int(position[1]-56)
                # RETURN TWO POSITIONS AHEAD OF THEM

            else:
                return position
                # OTHERWISE RETURN THEIR EXACT POSITION

        if pacman.get_orientation() == "down":
            if (position[0], position[1]+56) in maze and (position[0], position[1]+56) != (252, 280) and (position[0], position[1]+56) != (224, 280) and (position[0], position[1]+56) != (280, 280):
                # IF TWO POSITIONS AHEAD OF THEM IS IN THE MAZE

                return int(position[0]), int(position[1]+56)
                # RETURN TWO POSITIONS AHEAD OF THEM

            else:
                return position
                # OTHERWISE RETURN THEIR EXACT POSITION

    def random_movement(self, direction_input, maze):

        ##### random_movement #######
        # Parameters : direction_input:Tuple, maze:object
        # Return Type : direction:Tuple
        # Purpose :- Generates a random direction to move in
        ##########################

        if (self.rect.center[0] - (cell_width//2)) % 28 == 0 and (self.rect.center[1] - (cell_height//2)) % 28 == 0:
            # IF THE GHOST IS IN THE CENTRE

            if self.rect.center == (294, 294):
                # IF THE GHOST IS AT THE STARTING POSITION

                return -1, 0
                # GO LEFT

            else:
                direction = random.randint(1, 4)
                # GENERATE A RANDOM NUMBER

                while self.get_old_direction() == direction:
                    # WHILE THE DIRECTION IS THE SAME DIRECTION AS LAST TIME

                    direction = random.randint(1, 4)
                    # GENERATE A RANDOM NUMBER

                self.update_old_direction(direction)
                # UPDATE OLD DIRECTION

                if direction == 1 and (self.get_pixel_position()[0] + 28, self.get_pixel_position()[1]) in maze.maze_pixel_list:
                    # IF THE NUMBER IS ONE AND THE PLAYER DOESNT HAVE A WALL TO THEIR RIGHT

                    return 1, 0
                    # GO RIGHT

                if direction == 2 and (self.get_pixel_position()[0] - 28, self.get_pixel_position()[1]) in maze.maze_pixel_list:
                    # IF THE NUMBER IS TWO AND THE PLAYER DOESNT HAVE A WALL TO THEIR LEFT

                    return -1, 0
                    # GO LEFT

                if direction == 3 and (self.get_pixel_position()[0], self.get_pixel_position()[1] + 28) in maze.maze_pixel_list:
                    # IF THE NUMBER IS THREE AND THE PLAYER DOESNT HAVE A WALL BELOW

                    return 0, 1
                    # GO DOWN

                if direction == 4 and (self.get_pixel_position()[0], self.get_pixel_position()[1] - 28) in maze.maze_pixel_list:
                    # IF THE NUMBER IS FOUR AND THE PLAYER DOESNT HAVE A WALL ABOVE

                    return 0, -1
                    # GO UP

                else:
                    return 0, 0
                    # OTHERWISE DO NOT MOVE
        else:
            return direction_input
            # OTHERWISE KEEP MOVING IN THE SAME DIRECTION

    def closest_distance_calculator(self, position_variable, list):

        ##### closest_distance_calculator #######
        # Parameters : position_variable:Tuple, list:List
        # Return Type : position:Tuple
        # Purpose :- Finds the closest position from a list of positions
        ##########################

        distance = 10000
        position = []
        for each_position in list:
            # LOOP THROUGH ALL POSITIONS IN LIST

            my_distance = 0
            if position_variable[0] >= each_position[0]:
                # IF THE X POSITION IS TO THE RIGHT

                my_distance += ((position_variable[0]//28) - (each_position[0]//28))
            else:
                # X POSITION TO THE LEFT

                my_distance += ((each_position[0]//28) - (position_variable[0]//28))
            if position_variable[1] >= each_position[1]:
                # Y POSITION BELOW

                my_distance += ((position_variable[1] // 28) - (each_position[1] // 28))
            else:
                # Y POSITION ABOVE

                my_distance += ((each_position[1] // 28) - (position_variable[1] // 28))
            if my_distance <= distance:
                # IF THE POSITION IS CLOSER

                position = each_position
                distance = my_distance
                # UPDATE POSITION AND DISTANCE VARIABLES

        return position

    def adjacent_search(self, cell_to_check, end_location, walls):

        ##### adjacent_search #######
        # Parameters : cell_to_check:List, end_location:Tuple, walls:List
        # Return Type : priority_queue:List
        # Purpose :- Finds all the positions that are adjacent
        ##########################

        priority_queue = []
        if (cell_to_check[1][0] + 28, cell_to_check[1][1]) not in walls and cell_to_check[1][0] + 28 < screen_width and (cell_to_check[1][0] + 28, cell_to_check[1][1]) != cell_to_check[2] and (cell_to_check[1][0] + 28, cell_to_check[1][1]) not in self.visited:
            # IF THE CELL IS IN THE MAZE AND NOT A WALL AND HAS NOT BEEN SEARCHED BEFORE

            absolute_distance = abs(int((vector(end_location[0] // 28, end_location[1] // 28) - vector((cell_to_check[1][0] + 28) // 28, cell_to_check[1][1] // 28))[0])) + abs(int((vector(end_location[0] // 28, end_location[1] // 28) - vector((cell_to_check[1][0] + 28) // 28, cell_to_check[1][1] // 28))[1]))
            # CALCULATE THE  MANHATTAN DISTANCE

            if end_location[0] > (cell_to_check[1][0] + 28):
                # IF YOU ARE MOVING IN THE RIGHT DIRECTION

                absolute_distance -= 1
                # REMOVE ONE OFF DISTANCE

            priority_queue.append((absolute_distance, (int(cell_to_check[1][0] + 28), int(cell_to_check[1][1])), (int(cell_to_check[1][0]), int(cell_to_check[1][1]))))
            # ADD POSITION TO PRIORITY QUEUE

        if (cell_to_check[1][0] - 28, cell_to_check[1][1]) not in walls and cell_to_check[1][0] - 28 > 0 and (cell_to_check[1][0] - 28, cell_to_check[1][1]) != cell_to_check[2] and (cell_to_check[1][0] - 28, cell_to_check[1][1]) not in self.visited:
            # IF THE CELL IS IN THE MAZE AND NOT A WALL AND HAS NOT BEEN SEARCHED BEFORE

            absolute_distance = abs(int((vector(end_location[0] // 28, end_location[1] // 28) - vector((cell_to_check[1][0] - 28) // 28, cell_to_check[1][1] // 28))[0])) + abs(int((vector(end_location[0] // 28, end_location[1] // 28) - vector((cell_to_check[1][0] - 28) // 28, cell_to_check[1][1] // 28))[1]))
            # CALCULATE THE  MANHATTAN DISTANCE

            if end_location[0] < (cell_to_check[1][0] - 28):
                # IF YOU ARE MOVING IN THE RIGHT DIRECTION

                absolute_distance -= 1
                # REMOVE ONE OFF DISTANCE

            priority_queue.append((absolute_distance, (int(cell_to_check[1][0] - 28), int(cell_to_check[1][1])), (int(cell_to_check[1][0]), int(cell_to_check[1][1]))))
            # ADD POSITION TO PRIORITY QUEUE

        if (cell_to_check[1][0], cell_to_check[1][1] + 28) not in walls and cell_to_check[1][1] + 28 < screen_length and (cell_to_check[1][0], cell_to_check[1][1] + 28) != cell_to_check[2] and (cell_to_check[1][0], cell_to_check[1][1] + 28) not in self.visited:
            # IF THE CELL IS IN THE MAZE AND NOT A WALL AND HAS NOT BEEN SEARCHED BEFORE

            absolute_distance = abs(int((vector(end_location[0] // 28, end_location[1] // 28) - vector(cell_to_check[1][0] // 28, (cell_to_check[1][1] + 28) // 28))[0])) + abs(int((vector(end_location[0] // 28, end_location[1] // 28) - vector(cell_to_check[1][0] // 28, (cell_to_check[1][1] + 28) // 28))[1]))
            # CALCULATE THE  MANHATTAN DISTANCE

            if end_location[1] > (cell_to_check[1][1] + 28):
                # IF YOU ARE MOVING IN THE RIGHT DIRECTION

                absolute_distance -= 1
                # REMOVE ONE OFF DISTANCE

            priority_queue.append((absolute_distance, (int(cell_to_check[1][0]), int(cell_to_check[1][1] + 28)), (int(cell_to_check[1][0]), int(cell_to_check[1][1]))))
            # ADD POSITION TO PRIORITY QUEUE

        if (cell_to_check[1][0], cell_to_check[1][1] - 28) not in walls and cell_to_check[1][1] - 28 > 0 and (cell_to_check[1][0], cell_to_check[1][1] - 28) != cell_to_check[2] and (cell_to_check[1][0], cell_to_check[1][1] - 28) not in self.visited:
            # IF THE CELL IS IN THE MAZE AND NOT A WALL AND HAS NOT BEEN SEARCHED BEFORE

            absolute_distance = abs(int((vector(end_location[0] // 28, end_location[1] // 28) - vector(cell_to_check[1][0] // 28, (cell_to_check[1][1] - 28) // 28))[0])) + abs(int((vector(end_location[0] // 28, end_location[1] // 28) - vector(cell_to_check[1][0] // 28, (cell_to_check[1][1] - 28) // 28))[1]))
            # CALCULATE THE  MANHATTAN DISTANCE

            if end_location[1] < (cell_to_check[1][1] - 28):
                # IF YOU ARE MOVING IN THE RIGHT DIRECTION

                absolute_distance -= 1
                # REMOVE ONE OFF DISTANCE

            priority_queue.append((absolute_distance, (int(cell_to_check[1][0]), int(cell_to_check[1][1] - 28)), (int(cell_to_check[1][0]), int(cell_to_check[1][1]))))
            # ADD POSITION TO PRIORITY QUEUE

        return priority_queue

    # INHERITANCE
    def reset(self, starting_position):

        ##### reset #######
        # Parameters : starting_position: Tuple
        # Return Type : None
        # Purpose :- Reset starting position and starting variables
        ##########################

        self.rect.center = (starting_position[0] + cell_width // 2, starting_position[1] + cell_height // 2)
        self.update_direction((0, 0))
        self.update_old_direction(False)
        self.update_end_pos(None)
        self.update_start_pos(None)
        self.update_change_mode(None)
        self.update_ghost_clock(0)
        self.update_is_alive(True)
        self.update_is_frightened(False)
        # RESET ALL VARIABLES TO STARTING VALUES

    def is_running(self, position, walls):

        ##### is_running #######
        # Parameters : position:Tuple, walls:List
        # Return Type : None
        # Purpose :- Makes the ghost run to the ghost cage
        ##########################

        self.search((0, self.get_pixel_position(), self.get_pixel_position()), (252, 280), walls)
        # CALCULATE HOW TO GET TO GHOST CAGE

        tempA = self.direction_calculator(self.visited, self.get_direction(), position, walls)
        self.update_direction(tempA)
        # MOVE THERE

    def reset_game(self, starting_position):

        ##### reset_game #######
        # Parameters : starting_position:Tuple
        # Return Type : None
        # Purpose :- Resets all variables
        ##########################

        self.reset(starting_position)
        self.movement = []
        self.priority_queue = []
        self.visited = []
        # RESET ALL VARIABLES

    def singleplayer_update(self):

        ##### singleplayer_update #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Logic for singleplayer game
        ##########################

        self.image_animator()
        # MAKE GHOST LOOK ANIMATED

        if not self.pacman.get_is_paused() and self.pacman.get_has_started():
            # IF THE GAME IS NOT PAUSED AND THE PLAYER HAS STARTED

            self.ghost_essentials()
            # THE GHOST WILL BEGIN THE GAME

            if self.get_pixel_position() == self.pacman.get_pixel_position():
                # IF THE GHOST AND PLAYER COLLIDE

                if self.get_is_frightened():
                    # IF THE GHOST IS FRIGHTENED

                    self.update_is_alive(False)
                    # KILL GHOST

                else:
                    self.pacman.update_is_alive(False)
                    self.pacman.update_timer(0)
                    self.pacman.update_has_started(False)
                    # KILL PLAYER

            if self.get_pixel_position() == (252, 280) and not self.get_is_alive():
                # IF THE GHOST MAKES IT TO THE GHOST CAGE AND IS DEAD

                self.update_is_alive(True)
                self.update_is_frightened(False)
                self.pacman.update_score(self.pacman.get_score() + 15)
                # BRING IT BACK TO LIFE AND RESET FRIGHTENED AND IS ALIVE VARIABLES

    def multiplayer_update(self):

        ##### multiplayer_update #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Logic for multiplayer game
        ##########################

        self.image_animator()
        # MAKE THE PLAYER LOOK ANIMATED

        self.ghost_essentials()
        # GHOST WILL UPDATE POSITION AND TIME

        if self.get_pixel_position() == (252, 280) and not self.get_is_alive():
            # IF THE GHOST REACHES THE CAGE

            self.update_is_alive(True)
            self.update_is_frightened(False)
            # BRING IT BACK TO LIFE

    def ghost_essentials(self):

        ##### ghost_essentials #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Moves ghost, updates ghost clock and pixel position
        ##########################

        self.update_ghost_clock(self.get_ghost_clock() + 1)
        # INCREASE TIME BY ONE

        self.update_pixel_position((int((self.rect.center[0] // cell_width) * cell_width), int((self.rect.center[1] // cell_width) * cell_width)))
        # UPDATE THE PIXEL POSITION

        self.rect.center += vector(self.get_direction())
        # MOVE THE GHOST

    def force_pause(self):

        ##### force_pause #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Freezes the ghost in the middle of the cell
        ##########################

        self.rect.center = (self.get_pixel_position()[0] + (cell_width // 2), self.get_pixel_position()[1] + (cell_height // 2))
        # FREEZE THE GHOST IN PLACE

    def image_animator(self):

        ##### image_animator #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Makes the ghost image looks animated depending on its orientation and certain variables
        ##########################

        if not self.get_is_alive():
            # IF THE GHOST IS DEAD

            self.orientation_images(self.get_direction(), self.right_eye, self.left_eye, self.up_eye, self.down_eye, 0.15, 0, 0)
            # UPDATE TO EYES IMAGES

        else:
            if self.get_change_mode() and not self.get_is_frightened():
                # IF THE BLACK GHOST HAS CHANGED MODE AND IS NOT FRIGHTENED

                self.orientation_images(self.get_direction(), self.white_right, self.white_left, self.white_up, self.white_down, 0.15, 4, 4)
                # DISPLAY WHITE GHOST

            else:
                if not self.get_is_frightened():
                    # IF THE GHOST IS NOT FRIGHTENED

                    self.orientation_images(self.get_direction(), self.right_images, self.left_images, self.up_images, self.down_images, 0.15, 4, 4)
                    # DISPLAY GHOST IMAGES DEPENDING ON ORIENTATION

    def get_change_mode(self):

        ##### get_change_mode #######
        # Parameters : None
        # Return Type : __change_mode:Boolean
        # Purpose :- Get change_mode variable
        ##########################

        return self.__change_mode

    def update_change_mode(self, change_mode):

        ##### update_change_mode #######
        # Parameters : change_mode:Boolean
        # Return Type : None
        # Purpose :- Updates change_mode variable
        ##########################

        self.__change_mode = change_mode

    def get_is_frightened(self):

        ##### get_is_frightened #######
        # Parameters : None
        # Return Type : __is_frightened:Boolean
        # Purpose :- Gets is_frightened variable
        ##########################

        return self.__is_frightened

    def update_is_frightened(self, is_frightened):

        ##### update_is_frightened #######
        # Parameters : is_frightened:Boolean
        # Return Type : None
        # Purpose :- Updates is_frightened variable
        ##########################

        self.__is_frightened = is_frightened

    def get_is_alive(self):

        ##### get_is_alive #######
        # Parameters : None
        # Return Type : __is_alive:Boolean
        # Purpose :- Gets is_alive variable
        ##########################

        return self.__is_alive

    def update_is_alive(self, is_alive):

        ##### update_is_alive #######
        # Parameters : is_alive:Boolean
        # Return Type : None
        # Purpose :- Update is alive variable
        ##########################

        self.__is_alive = is_alive

    def get_ghost_clock(self):

        ##### get_ghost_clock #######
        # Parameters : None
        # Return Type : __ghost_clock:int
        # Purpose :- Get ghost_clock variable
        ##########################

        return self.__ghost_clock

    def update_ghost_clock(self, ghost_clock):

        ##### update_ghost_clock #######
        # Parameters : ghost_clock:int
        # Return Type : None
        # Purpose :- Update ghost clock variable
        ##########################

        self.__ghost_clock = ghost_clock

    def get_start_pos(self):

        ##### get_start_pos #######
        # Parameters : None
        # Return Type : __start_pos:Tuple
        # Purpose :- Gets __start_pos variable
        ##########################

        return self.__start_pos

    def update_start_pos(self, start_pos):

        ##### update_start_pos #######
        # Parameters : start_pos:Tuple
        # Return Type : None
        # Purpose :- Updates start_pos variable
        ##########################

        self.__start_pos = start_pos

    def get_end_pos(self):

        ##### get_end_pos #######
        # Parameters : None
        # Return Type : __end_pos:Tuple
        # Purpose :- Gets end_pos variable
        ##########################

        return self.__end_pos

    def update_end_pos(self, end_pos):

        ##### update_end_pos #######
        # Parameters : end_pos:Tuple
        # Return Type : None
        # Purpose :- Updates end pos variable
        ##########################

        self.__end_pos = end_pos

    def get_old_direction(self):

        ##### get_old_direction #######
        # Parameters : None
        # Return Type : __old_dirction:Tuple
        # Purpose :- Get old_direction variable
        ##########################

        return self.__old_direction

    def update_old_direction(self, old_direction):

        ##### update_old_direction #######
        # Parameters : old_direction:Tuple
        # Return Type : None
        # Purpose :- Update old_direction variable
        ##########################

        self.__old_direction = old_direction

    def get_direction(self):

        ##### get_direction #######
        # Parameters : None
        # Return Type : __direction:Tuple
        # Purpose :- Gets direction variable
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
        # Purpose :- Gets pixel position variable
        ##########################

        return self.__pixel_position

    def update_pixel_position(self, pixel_position):

        ##### update_pixel_position #######
        # Parameters : pixel_position:Tuple
        # Return Type : None
        # Purpose :- Updates pixel position variable
        ##########################

        self.__pixel_position = pixel_position
