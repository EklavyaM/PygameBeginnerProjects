import pygame
import math


class PowerOneUp:

    # ==================== Straight Path up or down ===============================================================

    DIR_UP = 0
    DIR_DOWN = 1

    TYPES = (DIR_DOWN, DIR_UP)

    FADE_RATE = 200
    FADE_OFFSET = 5

    def __init__(self, l_pos_x, l_pos_y,
                 l_vel,
                 l_size,
                 l_color_in, l_color_out, l_color_fade,
                 l_stroke_width,
                 l_type_index):

        # ==================== EnemyStraightPath Constructor ==========================================================

        self.__pos_x = l_pos_x
        self.__pos_y = l_pos_y
        self.__velocity = l_vel
        self.__size = l_size

        self.__stroke_width = l_stroke_width

        self.__inner_color = pygame.Color(l_color_in[0], l_color_in[1], l_color_in[2])
        self.__outer_color = pygame.Color(l_color_out[0], l_color_out[1], l_color_out[2])
        self.__fade_color = pygame.Color(l_color_fade[0], l_color_fade[1], l_color_fade[2])

        self.__type = PowerOneUp.TYPES[l_type_index]

        self.__is_destroyed = False
        self.__has_collided = False

        self.__hit_box = pygame.Rect(self.__pos_x, self.__pos_y, self.__size, self.__size)
        self.__inner_box = pygame.Rect(self.__pos_x + self.__stroke_width, self.__pos_y + self.__stroke_width,
                                       self.__size - 2 * self.__stroke_width,
                                       self.__size - 2 * self.__stroke_width)

        self.__temp_color_increment = 0
        self.__temp_color_boundary = (255, 255, 255)

    def move(self, dt):

        # ==================== Updating its Position  ==================================================
        # ==================== Along with its hit box =======================================================

        if not self.__has_collided:

            if self.__type == PowerOneUp.DIR_DOWN:
                self.update_pos(self.__pos_y + self.__velocity * dt)

            elif self.__type == PowerOneUp.DIR_UP:
                self.update_pos(self.__pos_y - self.__velocity * dt)

        else:
            self.play_death_animation(dt)

    def kill(self):
        self.__is_destroyed = True

    def play_death_animation(self, dt):

        # ==================== fade to white ===============================================================

        self.__temp_color_increment = math.trunc(PowerOneUp.FADE_RATE * dt)

        if self.__fade_color.r - self.__inner_color.r > PowerOneUp.FADE_OFFSET:
            self.__inner_color.r += self.__temp_color_increment
        elif self.__fade_color.r - self.__inner_color.r < - PowerOneUp.FADE_OFFSET:
            self.__inner_color.r -= self.__temp_color_increment

        if self.__fade_color.g - self.__inner_color.g > PowerOneUp.FADE_OFFSET:
            self.__inner_color.g += self.__temp_color_increment
        elif self.__fade_color.g - self.__inner_color.g < - PowerOneUp.FADE_OFFSET:
            self.__inner_color.g -= self.__temp_color_increment

        if self.__fade_color.b - self.__inner_color.b > PowerOneUp.FADE_OFFSET:
            self.__inner_color.b += self.__temp_color_increment
        elif self.__fade_color.b - self.__inner_color.b < - PowerOneUp.FADE_OFFSET:
            self.__inner_color.b -= self.__temp_color_increment

        if self.__fade_color.r - self.__outer_color.r > PowerOneUp.FADE_OFFSET:
            self.__outer_color.r += self.__temp_color_increment
        elif self.__fade_color.r - self.__outer_color.r < - PowerOneUp.FADE_OFFSET:
            self.__outer_color.r -= self.__temp_color_increment

        if self.__fade_color.g - self.__outer_color.g > PowerOneUp.FADE_OFFSET:
            self.__outer_color.g += self.__temp_color_increment
        elif self.__fade_color.g - self.__outer_color.g < - PowerOneUp.FADE_OFFSET:
            self.__outer_color.g -= self.__temp_color_increment

        if self.__fade_color.b - self.__outer_color.b > PowerOneUp.FADE_OFFSET:
            self.__outer_color.b += self.__temp_color_increment
        elif self.__fade_color.b - self.__outer_color.b < - PowerOneUp.FADE_OFFSET:
            self.__outer_color.b -= self.__temp_color_increment

        if math.fabs(self.__fade_color.r - self.__inner_color.r) <= PowerOneUp.FADE_OFFSET and \
                math.fabs(self.__fade_color.g - self.__inner_color.g) <= PowerOneUp.FADE_OFFSET and \
                math.fabs(self.__fade_color.b - self.__inner_color.b) <= PowerOneUp.FADE_OFFSET and \
                math.fabs(self.__fade_color.r - self.__outer_color.r) <= PowerOneUp.FADE_OFFSET and \
                math.fabs(self.__fade_color.g - self.__outer_color.g) <= PowerOneUp.FADE_OFFSET and \
                math.fabs(self.__fade_color.b - self.__outer_color.b) <= PowerOneUp.FADE_OFFSET:
            self.kill()

    def update_pos(self, l_pos_y):
        self.__pos_y = self.__hit_box.top = l_pos_y
        self.__inner_box.top = self.__pos_y + self.__stroke_width

    def draw(self, scr):

        # ==================== Drawing the Guy ===========================================================

        pygame.draw.rect(scr, self.__outer_color, self.__hit_box)
        pygame.draw.rect(scr, self.__inner_color, self.__inner_box)

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
