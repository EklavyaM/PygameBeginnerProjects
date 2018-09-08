import pygame
import math


class StraightPath:

    # ==================== Different Types of Assholes ========================================================

    DIR_UP = 0
    DIR_DOWN = 1

    TYPES = (DIR_DOWN, DIR_UP)

    def __init__(self, l_pos_x, l_pos_y, l_vel, l_size_x, l_size_y, l_type_index):

        # ==================== StraightPath Constructor ==========================================================

        self.__pos_x = l_pos_x
        self.__pos_y = l_pos_y
        self.__velocity = l_vel
        self.__size_x = l_size_x
        self.__size_y = l_size_y

        self.__outer_color = pygame.Color("black")
        self.__stroke_width = 1

        self.__inner_color = pygame.Color("black")

        self.__type = StraightPath.TYPES[l_type_index]

        self.__is_destroyed = False
        self.__has_collided = False

        self.__hit_box = pygame.Rect(self.__pos_x, self.__pos_y, self.__size_x, self.__size_y)
        self.__inner_box = pygame.Rect(self.__pos_x + self.__stroke_width, self.__pos_y + self.__stroke_width,
                                       self.__size_x - 2 * self.__stroke_width,
                                       self.__size_y - 2 * self.__stroke_width)

        self.__temp_color_increment = 10
        self.__temp_color_boundary = 256 - self.__temp_color_increment

    def move(self, dt):

        # ==================== Updating StraightPath's Position  ==================================================
        # ==================== Along with its hit box =======================================================

        if not self.__has_collided:

            if self.__type == StraightPath.DIR_DOWN:
                self.update_pos(self.__pos_y + self.__velocity * dt)

            elif self.__type == StraightPath.DIR_UP:
                self.update_pos(self.__pos_y - self.__velocity * dt)

        else:
            self.play_death_animation(dt)

    def kill(self):
        self.__is_destroyed = True

    def play_death_animation(self, dt):

        # ==================== fade to white ===============================================================

        self.__temp_color_increment = math.trunc(800 * dt)
        self.__temp_color_boundary = 256 - self.__temp_color_increment

        if self.__inner_color.r < self.__temp_color_boundary:
            self.__inner_color.r += self.__temp_color_increment
        if self.__inner_color.g < self.__temp_color_boundary:
            self.__inner_color.g += self.__temp_color_increment
        if self.__inner_color.b < self.__temp_color_boundary:
            self.__inner_color.b += self.__temp_color_increment

        if self.__outer_color.r < self.__temp_color_boundary:
            self.__outer_color.r += self.__temp_color_increment
        if self.__outer_color.g < self.__temp_color_boundary:
            self.__outer_color.g += self.__temp_color_increment
        if self.__outer_color.b < self.__temp_color_boundary:
            self.__outer_color.b += self.__temp_color_increment

        # ==================== death =====================================

        if self.__inner_color.r >= self.__temp_color_boundary \
                and self.__inner_color.g >= self.__temp_color_boundary \
                and self.__inner_color.b >= self.__temp_color_boundary:
            self.kill()

    def update_pos(self, l_pos_y):
        self.__pos_y = self.__hit_box.top = l_pos_y
        self.__inner_box.top = self.__pos_y + self.__stroke_width

    def draw(self, scr):

        # ==================== Drawing the StraightPath ===========================================================

        pygame.draw.rect(scr, self.__outer_color, self.__hit_box)
        pygame.draw.rect(scr, self.__inner_color, self.__inner_box)

    def check_player_collision(self, l_player):

        # ==================== Returns True if StraightPath is colliding with the Player ===========================

        if self.__hit_box.colliderect(l_player.get_hitbox()):
            return True

    # ==================== Getters and setters ===============================================================

    def set_has_collided(self, l_has_collided):
        self.__has_collided = l_has_collided

    def get_has_collided(self):
        return self.__has_collided

    def set_is_destroyed(self, l_is_destroyed):
        self.__is_destroyed = l_is_destroyed

    def get_is_destroyed(self):
        return self.__is_destroyed

    def get_pos_y(self):
        return self.__pos_y

    def get_type(self):
        return self.__type

    def get_size_y(self):
        return self.__size_y
