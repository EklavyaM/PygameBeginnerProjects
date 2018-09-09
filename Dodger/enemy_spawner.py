from time import sleep
from random import randint
from threading import Timer
from enemy_straight_path import EnemyStraightPath


class EnemySpawner:

    # ==================== The sleep time of the Spawning thread is decreased by increasing ==========================
    # ==================== the Difficulty value thereby making it spawn assholes faster ==============================

    # ==================== The THRESHOLD_DIFFICULTY value is the minimum sleep time required =====================
    # ==================== by the Spawning thread. Any less than 0.07 makes the game far too difficult =============

    DIFFICULTY_VALUE = 0.03
    THRESHOLD_DIFFICULTY = 0.07

    INITIAL_WAIT = 3

    def __init__(self, l_player, l_screen_width, l_screen_height, l_bottom_offset):

        # ==================== EnemySpawner Constructor ==========================================================
        # ==================== Needs a player instance for collision detection =====================================

        self.__enemies = []
        self.__screen_width = l_screen_width
        self.__screen_height = l_screen_height
        self.__bottom_offset = l_bottom_offset

        self.__thread_spawn = Timer(EnemySpawner.INITIAL_WAIT, self.__spawn)
        self.__thread_spawn.setDaemon(True)
        self.__sleep_time = 0.8

        self.__temp_pos_x = 0
        self.__temp_pos_y = 0
        self.__temp_vel = 0
        self.__temp_size = 0
        self.__temp_type_index = 0

        self.__player = l_player

        # ==================== Starting Spawning Thread ============================================================

        self.__thread_spawn.start()

    @staticmethod
    def check_player_collision(l_enemy, l_player):

        # ==================== Checks for collision between player and enemy instance =============================

        if l_enemy.check_player_collision(l_player):
            if not l_enemy.get_has_collided():
                l_enemy.set_has_collided(True)
                l_player.hit()

    def __spawn(self):

        # ==================== Spawn function called by thread_spawn =============================================
        # ==================== Uses random values for x-position, velocity and size of an enemy ==================
        # ==================== After Spawning takes a break for few seconds ========================================

        # ==================== Change values for different enemy behavior and visuals ============================

        while self.__player.get_is_alive():

            self.__temp_vel = randint(self.__screen_width // 160, self.__screen_width//3)
            self.__temp_size = randint(self.__screen_width//200, self.__screen_width//100)
            self.__temp_pos_x = randint(0, self.__screen_width - self.__temp_size)
            self.__temp_type_index = randint(0, len(EnemyStraightPath.TYPES) - 1)

            if EnemyStraightPath.TYPES[self.__temp_type_index] == EnemyStraightPath.DIR_DOWN:
                self.__temp_pos_y = -self.__temp_size

            elif EnemyStraightPath.TYPES[self.__temp_type_index] == EnemyStraightPath.DIR_UP:
                self.__temp_pos_y = self.__screen_height

            self.__enemies.append(EnemyStraightPath(self.__temp_pos_x, self.__temp_pos_y,
                                                    self.__temp_vel,
                                                    self.__temp_size,
                                                    self.__temp_type_index))
            sleep(self.__sleep_time)

    def increase_difficulty(self):

        # ==================== Try not to change this ======================================================

        if self.__sleep_time - EnemySpawner.DIFFICULTY_VALUE >= EnemySpawner.THRESHOLD_DIFFICULTY:
            self.__sleep_time -= EnemySpawner.DIFFICULTY_VALUE

    def move(self, dt):

        # ==================== Movement Logic for All Enemies ======================================================

        for enemy in self.__enemies:

            if enemy.get_is_destroyed():
                self.__enemies.remove(enemy)
                continue

            enemy.move(dt)
            self.check_boundary(enemy)
            EnemySpawner.check_player_collision(enemy, self.__player)

    def draw(self, scr):

        # ==================== Drawing all Enemies =================================================================

        for enemy in self.__enemies:
            enemy.draw(scr)

    def check_boundary(self, l_enemy):

        # ==================== Check if EnemyStraightPath crossed the Boundary  ================================

        if l_enemy.get_type() == EnemyStraightPath.DIR_DOWN:
            if l_enemy.get_pos_y() + l_enemy.get_size() >= self.__screen_height:
                l_enemy.set_has_collided(True)

        elif l_enemy.get_type() == EnemyStraightPath.DIR_UP:
            if l_enemy.get_pos_y() <= self.__bottom_offset:
                l_enemy.set_has_collided(True)

