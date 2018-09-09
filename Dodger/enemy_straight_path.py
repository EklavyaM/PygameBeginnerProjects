import pygame
import math


class EnemyStraightPath:

    # ==================== Straight Path up or down ===============================================================

    DIR_UP = 0
    DIR_DOWN = 1

    TYPES = (DIR_DOWN, DIR_UP)

    FADE = 400

    def __init__(self, l_pos_x, l_pos_y,
                 l_vel,
                 l_size,
                 l_color,
                 l_type_index):

        # ==================== EnemyStraightPath Constructor ==========================================================

        self.__pos_x = l_pos_x
        self.__pos_y = l_pos_y
        self.__velocity = l_vel
        self.__size = l_size
        self.__color = pygame.Color(l_color[0], l_color[1], l_color[2])

        self.__type = EnemyStraightPath.TYPES[l_type_index]

        self.__is_destroyed = False
        self.__has_collided = False

        self.__hit_box = pygame.Rect(self.__pos_x, self.__pos_y, self.__size, self.__size)

        self.__temp_color_increment = 0
        self.__temp_color_boundary = 256 - self.__temp_color_increment

    def move(self, dt):

        # ==================== Updating its Position  ==================================================
        # ==================== Along with its hit box =======================================================

        if not self.__has_collided:

            if self.__type == EnemyStraightPath.DIR_DOWN:
                self.update_pos(self.__pos_y + self.__velocity * dt)

            elif self.__type == EnemyStraightPath.DIR_UP:
                self.update_pos(self.__pos_y - self.__velocity * dt)

        else:
            self.play_death_animation(dt)

    def kill(self):
        self.__is_destroyed = True

    def play_death_animation(self, dt):

        # ==================== fade to white ===============================================================

        self.__temp_color_increment = math.trunc(EnemyStraightPath.FADE * dt)
        self.__temp_color_boundary = 256 - self.__temp_color_increment

        if self.__color.r < self.__temp_color_boundary:
            self.__color.r += self.__temp_color_increment
        if self.__color.g < self.__temp_color_boundary:
            self.__color.g += self.__temp_color_increment
        if self.__color.b < self.__temp_color_boundary:
            self.__color.b += self.__temp_color_increment

        # ==================== death =====================================

        if self.__color.r >= self.__temp_color_boundary \
                and self.__color.g >= self.__temp_color_boundary \
                and self.__color.b >= self.__temp_color_boundary:
            self.kill()

    def update_pos(self, l_pos_y):
        self.__pos_y = self.__hit_box.top = l_pos_y

    def draw(self, scr):

        # ==================== Drawing the Guy ===========================================================

        pygame.draw.rect(scr, self.__color, self.__hit_box)

    def check_player_collision(self, l_player):

        # ==================== Returns True if the guy is colliding with the Player ===========================

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

    def get_size(self):
        return self.__size
