import pygame
from game_settings import *
vector = pygame.math.Vector2


class moving_object:

    # NEED TO CHANGE SELF.IMAGE and SELF.IMAGELOOP VARIABLES
    def update_sprite(self, images_to_update, speed, variable_x_size, variable_y_size):

        ##### update_sprite #######
        # Parameters : images_to_update:List, speed:float, variable_x_size:int, variable_y_size:int
        # Return Type : None
        # Purpose :- Loops through multiple images in order to gives animation illusion. Also makes the size of these images smaller in order to fit in the cells
        ##########################

        self.image_loop += speed
        if self.image_loop > len(images_to_update):
            self.image_loop = 0
        self.image = images_to_update[int(self.image_loop)]
        self.image = pygame.transform.scale(self.image, (cell_width - variable_x_size, cell_height - variable_y_size))
        self.image.set_colorkey(BLACK)

    def orientation_images(self, direction, right_images, left_images, up_images, down_images, speed, variable_x_size, variable_y_size):

        ##### orientation_images #######
        # Parameters : direction:Tuple, right_images:List, left_images:List, up_images:List, down_images:List, speed:float, variable_x_size:int, variable_y_size:int
        # Return Type : None
        # Purpose :-Depending on the orientation it displays a different image to the users screen then uses the update sprite function in order to make this image look animated
        ##########################

        if direction == (1, 0):
            self.update_sprite(right_images, speed, variable_x_size, variable_y_size)
        elif direction == (-1, 0):
            self.update_sprite(left_images, speed, variable_x_size, variable_y_size)
        elif direction == (0, -1):
            self.update_sprite(up_images, speed, variable_x_size, variable_y_size)
        elif direction == (0, 1):
            self.update_sprite(down_images, speed, variable_x_size, variable_y_size)
        else:
            self.update_sprite(right_images, speed, variable_x_size, variable_y_size)

    def wall_check(self, my_direction, wall_list, player_rect):

        ##### wall_check #######
        # Parameters : my_direction:Tuple, wall_list:List, player_rect:pygame.Rect
        # Return Type : None
        # Purpose :- Gets the players pixel position and when they hit a wall it stops the player
        ##########################

        # WE ALSO UPDATE PIXEL POSITION HERE BECAUSE THE ANIMATION LOOKS NICER

        pixel_position = vector((player_rect.each_line // cell_width) * cell_width, (player_rect.y // cell_width) * cell_width)
        if my_direction == (1, 0):
            if (pixel_position.each_line + 28, pixel_position.y) in wall_list:
                my_direction = (0, 0)
        if my_direction == (-1, 0):
            if (pixel_position.each_line - 28, pixel_position.y) in wall_list:
                my_direction = (0, 0)
        elif my_direction == (0, 1):
            if (pixel_position.each_line, pixel_position.y + 28) in wall_list:
                my_direction = (0, 0)
            if (pixel_position.each_line, pixel_position.y + 28) == (252, 252):
                my_direction = (0, 0)
        if my_direction == (0, -1):
            if (pixel_position.each_line, pixel_position.y - 28) in wall_list:
                my_direction = (0, 0)
        return my_direction, pixel_position

