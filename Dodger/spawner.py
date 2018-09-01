import pygame
from time import sleep
from random import randint
from threading import Timer


class AssholeSpawner:

    # ==================== The sleep time of the Spawning thread is decreased by increasing ==========================
    # ==================== the Difficulty value thereby making it spawn assholes faster ==============================

    # ==================== The THRESHOLD_DIFFICULTY value is the minimum sleep time required =====================
    # ==================== by the Spawning thread. Any less than 0.07 makes the game far too difficult =============

    DIFFICULTY_VALUE = 0.04
    THRESHOLD_DIFFICULTY = 0.04

    def __init__(self, l_player, l_screen_width, l_screen_height, l_bottom_offset):

        # ==================== AssholeSpawner Constructor ==========================================================
        # ==================== Needs a player instance for collision detection =====================================

        self.__assholes = []
        self.__screen_width = l_screen_width
        self.__screen_height = l_screen_height
        self.__bottom_offset = l_bottom_offset

        self.__thread_spawner = Timer(3, self.__spawn)
        self.__sleep_time = 0.8

        self.__temp_pos_x = 0
        self.__temp_pos_y = 0
        self.__temp_vel = 0
        self.__temp_size_x = 0
        self.__temp_size_y = 0
        self.__temp_type_index = 0

        self.__player = l_player

        # ==================== Starting Spawning Thread ============================================================

        self.__thread_spawner.start()

    @staticmethod
    def check_player_collision(l_asshole, l_player):

        # ==================== Checks for collision between player and asshole instance =============================

        if l_asshole.check_player_collision(l_player):
            if not l_asshole.get_has_collided():
                l_asshole.set_has_collided(True)
                l_player.hit()

    def __spawn(self):

        # ==================== Spawn function called by thread_spawner =============================================
        # ==================== Uses random values for x-position, velocity and size of an asshole ==================
        # ==================== After Spawning takes a break for few seconds ========================================

        # ==================== Change values for different asshole behavior and visuals ============================

        while self.__player.get_is_alive():

            self.__temp_vel = randint(10, 700)
            self.__temp_size_x = self.__temp_size_y = randint(10, 20)
            self.__temp_pos_x = randint(0, self.__screen_width - self.__temp_size_x)
            self.__temp_type_index = randint(0, len(AssholeSpawner.Asshole.TYPES) - 1)

            if AssholeSpawner.Asshole.TYPES[self.__temp_type_index] == AssholeSpawner.Asshole.DIR_DOWN:
                self.__temp_pos_y = -self.__temp_size_y

            elif AssholeSpawner.Asshole.TYPES[self.__temp_type_index] == AssholeSpawner.Asshole.DIR_UP:
                self.__temp_pos_y = self.__screen_height

            self.__assholes.append(AssholeSpawner.Asshole(self.__temp_pos_x, self.__temp_pos_y,
                                                          self.__temp_vel,
                                                          self.__temp_size_x, self.__temp_size_y,
                                                          self.__temp_type_index))
            sleep(self.__sleep_time)

    def increase_difficulty(self):

        # ==================== Try not to change this ======================================================

        if self.__sleep_time - AssholeSpawner.DIFFICULTY_VALUE >= AssholeSpawner.THRESHOLD_DIFFICULTY:
            self.__sleep_time -= AssholeSpawner.DIFFICULTY_VALUE

    def move(self, dt):

        # ==================== Movement Logic for All Assholes ======================================================

        for asshole in self.__assholes:

            if asshole.get_is_destroyed():
                self.__assholes.remove(asshole)
                continue

            asshole.move(dt)
            self.check_boundary(asshole)
            AssholeSpawner.check_player_collision(asshole, self.__player)

    def draw(self, scr):

        # ==================== Drawing all Assholes =================================================================

        for asshole in self.__assholes:
            asshole.draw(scr)

    def check_boundary(self, l_asshole):

        # ==================== Check if Asshole crossed the Boundary to Assguard ================================

        if l_asshole.get_type() == AssholeSpawner.Asshole.DIR_DOWN:
            if l_asshole.get_pos_y() + l_asshole.get_size_y() >= self.__screen_height - self.__bottom_offset:
                l_asshole.set_has_collided(True)

        elif l_asshole.get_type() == AssholeSpawner.Asshole.DIR_UP:
            if l_asshole.get_pos_y() <= 0:
                l_asshole.set_has_collided(True)

    # ==============================================================================================================
    # ==============================================================================================================
    # ==============================================================================================================
    # ==================== Inner Class Asshole for Spawner to create instances of ==================================
    # ==============================================================================================================
    # ==============================================================================================================
    # ==============================================================================================================

    class Asshole:

        # ==================== Different Types of Assholes ========================================================

        DIR_UP = 0
        DIR_DOWN = 1

        TYPES = (DIR_DOWN, DIR_UP)

        def __init__(self, l_pos_x, l_pos_y, l_vel, l_size_x, l_size_y, l_type_index):

            # ==================== Asshole Constructor ==========================================================

            self.__pos_x = l_pos_x
            self.__pos_y = l_pos_y
            self.__velocity = l_vel
            self.__size_x = l_size_x
            self.__size_y = l_size_y

            self.__outer_color = pygame.Color("black")
            self.__stroke_width = 1

            self.__inner_color = pygame.Color("red")

            self.__type = AssholeSpawner.Asshole.TYPES[l_type_index]

            self.__is_destroyed = False
            self.__has_collided = False

            self.__hit_box = pygame.Rect(self.__pos_x, self.__pos_y, self.__size_x, self.__size_y)
            self.__inner_box = pygame.Rect(self.__pos_x + self.__stroke_width, self.__pos_y + self.__stroke_width,
                                           self.__size_x - 2 * self.__stroke_width,
                                           self.__size_y - 2 * self.__stroke_width)

        def move(self, dt):

            # ==================== Updating Asshole's Position  ==================================================
            # ==================== Along with its hit box =======================================================

            if not self.__has_collided:

                if self.__type == AssholeSpawner.Asshole.DIR_DOWN:
                    self.update_pos(self.__pos_y + self.__velocity * dt)

                elif self.__type == AssholeSpawner.Asshole.DIR_UP:
                    self.update_pos(self.__pos_y - self.__velocity * dt)

            else:

                # ==================== animating outer color from black to white ===================================

                self.__outer_color.r += 10
                self.__outer_color.g += 10
                self.__outer_color.b += 10

                # ==================== animating inner color from red to white =====================================

                self.__inner_color.g += 10
                self.__inner_color.b += 10

                if self.__inner_color.g >= 245 or self.__inner_color.b >= 245:
                    self.__is_destroyed = True
                    pass

        def update_pos(self, l_pos_y):
            self.__pos_y = self.__hit_box.top = l_pos_y
            self.__inner_box.top = self.__pos_y + self.__stroke_width

        def draw(self, scr):

            # ==================== Drawing the Asshole ===========================================================

            pygame.draw.rect(scr, self.__outer_color, self.__hit_box)
            pygame.draw.rect(scr, self.__inner_color, self.__inner_box)

        def check_player_collision(self, l_player):

            # ==================== Returns True if Asshole is colliding with the Player ===========================

            if self.__hit_box.colliderect(l_player.get_hitbox()):
                return True

        # ==================== Getters and setters ===============================================================

        def set_has_collided(self, has_collided):
            self.__has_collided = has_collided

        def get_has_collided(self):
            return self.__has_collided

        def set_is_destroyed(self, is_destroyed):
            self.__is_destroyed = is_destroyed

        def get_is_destroyed(self):
            return self.__is_destroyed

        def get_pos_y(self):
            return self.__pos_y

        def get_type(self):
            return self.__type

        def get_size_y(self):
            return self.__size_y
