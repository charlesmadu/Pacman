from game_settings import *
import random
# DIMENSIONS x = 19 y = 22


class Maze:
    def __init__(self):
        self.maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
                     [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                     [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
                     [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                     [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                     [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                     ]
        self.fruit_images = []
        self.fruit_positions = []
        self.reject_list = [(0, 8), (1, 8), (2, 8), (0, 12), (1, 12), (2, 12), (9, 12), (8, 10), (9, 10), (10, 10), (9, 8), (9, 9), (16, 8), (17, 8), (18, 8), (16, 12), (17, 12), (18, 12), (1, 10), (2, 10), (3, 10), (15, 10), (16, 10), (17, 10)]
        self.special_dots_list = [(28, 84), (476, 84), (28, 448), (476, 448)]
        self.outside_maze = [(28, 224), (56, 224), (448, 224), (476, 224), (28, 336), (56, 336), (448, 336), (476, 336)]
        self.walls, self.maze_pixel_list, self.dots_list = self.create_walls(self.maze, self.outside_maze)
        # RUN METHOD TO MAKE WALLS DOTS LIST AND A LIST OF ALL AVAILABLE POSITIONS IN THE MAZE

    def create_walls(self, maze, outside_maze):

        ##### create_walls #######
        # Parameters : maze:List, outside_maze:List
        # Return Type : wall_list:List, maze_pixel_list:List, dots_list:List
        # Purpose :- Assigns a grid position to each wall in the maze and returns the value as a 2D array as well as the positions of all the dots in the game
        ##########################

        wall_list = []
        maze_pixel_list = []
        dots_list = []
        # MAZE CREATION FUNCTION

        for y_position in range(0, len(maze)):
            for x_position in range(0, len(maze[y_position])):
                # FOR EACH CELL IN THE MAZE

                maze_pixel_list.append((x_position * cell_width, y_position * cell_height))
                # APPEND IT TO MAZE_PIXEL_LIST

                if maze[y_position][x_position] == 1:
                    # IF THE POSITION IS A 1

                    wall_list.append((x_position * cell_width, y_position * cell_height))
                    # IT IS A WALL ADD IT WALLS_LIST

                if maze[y_position][x_position] == 0 and (x_position, y_position) not in self.reject_list and (x_position*28, y_position*28) not in self.special_dots_list:
                    # IF IT IS ZERO AND IT IS NOT A REJECTION SPACE OR A SPECIAL DOT SPACE

                    dots_list.append((x_position * cell_width, y_position * cell_height))
                    # ADD IT TO DOTS LIST

        for each_pos in wall_list:
            # FOR EACH POSITION IN THE WALLS LIST

            if each_pos in maze_pixel_list:
                # IF THE POSITION IS IN THE MAZE PIXEL LIST

                maze_pixel_list.remove(each_pos)
                # REMOVE THAT POSITION

        for each_position in outside_maze:
            # FOR EACH POSITION THAT IS OUTSIDE THE MAZE

            if each_position in maze_pixel_list:
                # IF THE POSITION IS IN THE MAZE PIXEL LIST

                maze_pixel_list.remove(each_position)
                # REMOVE THIS POSITION FROM MAZE PIXEL LIST

        return wall_list, maze_pixel_list, dots_list
        # RETURN WALLS THE MAZE AND DOTS LIST

    def reset(self):

        ##### reset #######
        # Parameters : None
        # Return Type : None
        # Purpose :- Reset all maze variables
        ##########################

    # RESET FUNCTION

        self.fruit_images = []
        self.fruit_positions = []
        self.special_dots_list = [(28, 84), (476, 84), (28, 448), (476, 448)]
        # RESET ALL VARIABLE VALUES

        self.walls, self.maze_pixel_list, self.dots_list = self.create_walls(self.maze, self.outside_maze)
        # RESET DOTS LIST

    def random_fruit(self, dots_list, fruit_positions, fruit_pictures):

        ##### random_fruit #######
        # Parameters : dots_list:List, fruit_positions:List, fruit_pictures:List
        # Return Type : None
        # Purpose :- For singleplayer mode. Has a chance of randomly putting fruits into the maze
        ##########################

        amount_of_fruit = random.randint(0, 3)
        # GENERATE A RANDOM AMOUNT OF FRUIT IN THE MAZE

        for each_fruit in range(0, amount_of_fruit):
            # FOR EACH FRUIT THAT WILL BE IN THE MZE
            fruit_pos = random.randint(0, len(dots_list) - 1)
            # RANDOMLY GENERATE THEIR POSITION IN THE MAZE

            fruit_picture = random.randint(0, 7)
            # RANDOMLY CHOOSE A FRUIT PICTURE

            fruit_positions.append(dots_list[fruit_pos])
            # ADD THE POSITION TO FRUITS POSITION VARIABLE

            fruit_pictures.append(fruit_picture)
            # ADD THE FRUIT PICTURE ID TO PICTURES LIST

            dots_list.remove(dots_list[fruit_pos])
            # REMOVE THE POSITION FROM DOTS LIST


