from time import sleep
from random import randint
from threading import Timer
from power_one_up import PowerOneUp


class PowerupSpawner:

    DIFFICULTY_VALUE = 0.03
    THRESHOLD_DIFFICULTY = 3

    INITIAL_WAIT = 10

    def __init__(self, l_player,
                 l_life_in, l_life_out,
                 l_screen_width, l_screen_height,
                 l_bottom_offset):

        # ==================== Powerup Constructor ==========================================================
        # ==================== Needs a player instance for collision detection =====================================

        self.__power_ups = []
        self.__screen_width = l_screen_width
        self.__screen_height = l_screen_height
        self.__bottom_offset = l_bottom_offset

        self.__thread_spawn = Timer(PowerupSpawner.INITIAL_WAIT, self.__spawn)
        self.__thread_spawn.setDaemon(True)
        self.__sleep_time = 10

        self.__temp_pos_x = 0
        self.__temp_pos_y = 0
        self.__temp_size = 0
        self.__temp_vel = 0
        self.__temp_color_in = l_life_in
        self.__temp_color_out = l_life_out
        self.__temp_type_index = 0

        self.__player = l_player

        # ==================== Starting Spawning Thread ============================================================

        self.__thread_spawn.start()

    @staticmethod
    def check_player_collision(l_powerup, l_player):

        # ==================== Checks for collision between player and enemy instance =============================

        if l_powerup.check_player_collision(l_player):
            if not l_powerup.get_has_collided():
                l_powerup.set_has_collided(True)
                l_player.one_up()

    def __spawn(self):

        # ==================== Spawn function called by thread_spawn =============================================
        # ==================== Uses random values for x-position, velocity and size of an enemy ==================
        # ==================== After Spawning takes a break for few seconds ========================================

        # ==================== Change values for different enemy behavior and visuals ============================

        while self.__player.get_is_alive():

            self.__temp_vel = randint(self.__screen_width // 20, self.__screen_width//10)
            self.__temp_size = self.__player.get_size()
            self.__temp_pos_x = randint(0, self.__screen_width - self.__temp_size)
            self.__temp_type_index = randint(0, len(PowerOneUp.TYPES) - 1)

            if PowerOneUp.TYPES[self.__temp_type_index] == PowerOneUp.DIR_DOWN:
                self.__temp_pos_y = -self.__temp_size

            elif PowerOneUp.TYPES[self.__temp_type_index] == PowerOneUp.DIR_UP:
                self.__temp_pos_y = self.__screen_height

            self.__power_ups.append(PowerOneUp(self.__temp_pos_x, self.__temp_pos_y,
                                               self.__temp_vel,
                                               self.__temp_size,
                                               self.__temp_color_in, self.__temp_color_out,
                                               self.__temp_type_index))
            sleep(self.__sleep_time)

    def increase_difficulty(self):

        # ==================== Try not to change this ======================================================

        if self.__sleep_time - PowerupSpawner.DIFFICULTY_VALUE >= PowerupSpawner.THRESHOLD_DIFFICULTY:
            self.__sleep_time -= PowerupSpawner.DIFFICULTY_VALUE

    def move(self, dt):

        # ==================== Movement Logic for All Enemies ======================================================

        for powerup in self.__power_ups:

            if powerup.get_is_destroyed():
                self.__power_ups.remove(powerup)
                continue

            powerup.move(dt)
            self.check_boundary(powerup)
            PowerupSpawner.check_player_collision(powerup, self.__player)

    def draw(self, scr):

        # ==================== Drawing all Enemies =================================================================

        for powerup in self.__power_ups:
            powerup.draw(scr)

    def check_boundary(self, l_powerup):

        # ==================== Check if EnemyStraightPath crossed the Boundary  ================================

        if l_powerup.get_type() == PowerOneUp.DIR_DOWN:
            if l_powerup.get_pos_y() + l_powerup.get_size() >= self.__screen_height:
                l_powerup.set_has_collided(True)

        elif l_powerup.get_type() == PowerOneUp.DIR_UP:
            if l_powerup.get_pos_y() <= self.__bottom_offset:
                l_powerup.set_has_collided(True)
