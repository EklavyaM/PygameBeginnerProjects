import pygame
import math
from random import randint
from threading import Timer
from time import sleep


class AssholeSpawner:

    # ==================== The sleep time of the Spawning thread is decreased by increasing ==========================
    # ==================== the Difficulty value thereby making it spawn assholes faster ==============================

    # ==================== The THRESHOLD_DIFFICULTY value is the minimum sleep time required =====================
    # ==================== by the Spawning thread. Any less than 0.07 makes the game far too difficult =============

    DIFFICULTY_VALUE = 0.04
    THRESHOLD_DIFFICULTY = 0.04

    def __init__(self, l_player):

        # ==================== AssholeSpawner Constructor ==========================================================
        # ==================== Needs a player instance for collision detection =====================================

        self.__assholes = []
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

    def __spawn(self):

        # ==================== Spawn function called by thread_spawner =============================================
        # ==================== Uses random values for x-position, velocity and size of an asshole ==================
        # ==================== After Spawning takes a break for few seconds ========================================

        # ==================== Change values for different asshole behavior and visuals ============================

        while g_game_running:

            self.__temp_vel = randint(10, 700)
            self.__temp_size_x = self.__temp_size_y = randint(8, 20)
            self.__temp_type_index = randint(0, len(AssholeSpawner.Asshole.TYPES) - 1)

            self.__temp_pos_x = randint(0, g_screen_dimensions[0] - self.__temp_size_x)

            if AssholeSpawner.Asshole.TYPES[self.__temp_type_index] == AssholeSpawner.Asshole.DIR_DOWN:
                self.__temp_pos_y = -self.__temp_size_y

            elif AssholeSpawner.Asshole.TYPES[self.__temp_type_index] == AssholeSpawner.Asshole.DIR_UP:
                self.__temp_pos_y = g_screen_dimensions[1]

            self.__assholes.append(AssholeSpawner.Asshole(self.__temp_pos_x, self.__temp_pos_y,
                                                          self.__temp_vel,
                                                          self.__temp_size_x, self.__temp_size_y,
                                                          self.__temp_type_index))
            sleep(self.__sleep_time)

    def increase_difficulty(self):

        # ==================== Try not to change this ======================================================

        if self.__sleep_time - AssholeSpawner.DIFFICULTY_VALUE >= AssholeSpawner.THRESHOLD_DIFFICULTY:
            self.__sleep_time -= AssholeSpawner.DIFFICULTY_VALUE

    def move(self):

        # ==================== Movement Logic for All Assholes ======================================================

        for asshole in self.__assholes:

            if asshole.get_is_destroyed():
                self.__assholes.remove(asshole)
                continue

            asshole.move()
            asshole.boundary_check()

            # ==================== Check if Asshole Collided with Player ==========================================

            if asshole.check_player_collision(self.__player):
                global g_game_running

                if not asshole.get_has_collided():

                    asshole.set_has_collided(True)
                    self.__player.hit()

    def draw(self, scr):

        # ==================== Drawing all Assholes =================================================================

        for asshole in self.__assholes:
            asshole.draw(scr)

    # ==================== Inner Class Asshole for Spawner to create instances of ==================================

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
            self.__color = pygame.Color("red")

            self.__type = AssholeSpawner.Asshole.TYPES[l_type_index]

            self.__is_destroyed = False
            self.__has_collided = False
            self.__hit_box = pygame.Rect(self.__pos_x, self.__pos_y, self.__size_x, self.__size_y)

        def move(self):

            # ==================== Updating Asshole's Position  ==================================================
            # ==================== Along with its hit box =======================================================

            if not self.__has_collided:

                if self.__type == AssholeSpawner.Asshole.DIR_DOWN:
                    self.__pos_y = self.__hit_box.top = self.__pos_y + self.__velocity * g_time_per_frame_in_seconds

                elif self.__type == AssholeSpawner.Asshole.DIR_UP:
                    self.__pos_y = self.__hit_box.top = self.__pos_y - self.__velocity * g_time_per_frame_in_seconds

            else:
                self.__color.r -= 10

                if self.__color.r <= 10:
                    self.__is_destroyed = True
                    pass

        def draw(self, scr):

            # ==================== Drawing the Asshole ===========================================================

            pygame.draw.rect(scr, self.__color, self.__hit_box)

        def check_player_collision(self, l_player):

            # ==================== Returns True if Asshole is colliding with the Player ===========================

            if self.__hit_box.colliderect(l_player.hit_box):
                return True

            # ==================== Getters and setters for has_collided check ===========================

        def set_has_collided(self, has_collided):
            self.__has_collided = has_collided

        def get_has_collided(self):
            return self.__has_collided

            # ==================== Getters and setters for is_destroyed check ===========================

        def set_is_destroyed(self, is_destroyed):
            self.__is_destroyed = is_destroyed

        def get_is_destroyed(self):
            return self.__is_destroyed

        def boundary_check(self):

            # ==================== Check if Asshole crossed the Boundary to Assguard ================================

            if self.__type == AssholeSpawner.Asshole.DIR_DOWN:
                if self.__pos_y + self.__size_y >= g_screen_dimensions[1] - g_font_screen_offset:
                    self.__has_collided = True

            elif self.__type == AssholeSpawner.Asshole.DIR_UP:
                if self.__pos_y <= 0:
                    self.__has_collided = True


class Player:

    # ==================== Player Class Variables =================================================================

    SIZE_X = 16
    SIZE_Y = 16

    REG_ACC = 200
    REG_COLOR = "white"

    STUN_ACC = 50
    STUN_COLOR = "blue"
    STUN_TIME = 3.5

    MAX_VELOCITY = 500
    MIN_VELOCITY = 0.5
    FRICTION = 0.3

    DIR_UP = 0
    DIR_DOWN = 1
    DIR_LEFT = 2
    DIR_RIGHT = 3

    def __init__(self, l_pos_x, l_pos_y):

        # ==================== Player Constructor =================================================================

        self.pos_x = l_pos_x
        self.pos_y = l_pos_y
        self.vel_x = 0
        self.vel_y = 0
        self.acc = Player.REG_ACC

        self.hit_box = pygame.Rect(self.pos_x, self.pos_y, Player.SIZE_X, Player.SIZE_Y)
        self.color = pygame.Color(Player.REG_COLOR)
        self.lives = 3
        self.current_dir = None

        self.keys = None
        self.dx, self.dy = 0, 0

        self.stun_timer = None

    def move(self):

        # ==================== Polling for Input =================================================================

        self.keys = pygame.key.get_pressed()

        if self.dx != 1 and (self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]):
            self.dy = 0
            self.dx = -1
        if self.dx !=-1 and (self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]):
            self.dy = 0
            self.dx = 1
        if self.dy != 1 and (self.keys[pygame.K_UP] or self.keys[pygame.K_w]):
            self.dy = -1
            self.dx = 0
        if self.dy != -1 and (self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]):
            self.dy = 1
            self.dx = 0

        # ==================== Accelerating Player till reaching Max Velocity =========================================

        updated_vel_x = self.vel_x + self.dx * self.acc
        updated_vel_y = self.vel_y + self.dy * self.acc

        if math.fabs(updated_vel_x) < Player.MAX_VELOCITY:
            self.vel_x = updated_vel_x
        else:
            self.vel_x = math.copysign(Player.MAX_VELOCITY, updated_vel_x)

        if math.fabs(updated_vel_y) < Player.MAX_VELOCITY:
            self.vel_y = updated_vel_y
        else:
            self.vel_y = math.copysign(Player.MAX_VELOCITY, updated_vel_y)

        # ==================== Applying Friction and =================================================================
        # ==================== Stopping all motion when velocity is less than a certain value ========================
        # ==================== which is Player.MIN_VELOCITY in this case =============================================

        if math.fabs(self.vel_x) > Player.MIN_VELOCITY or math.fabs(self.vel_y) > Player.MIN_VELOCITY:
            self.vel_x += -self.vel_x * Player.FRICTION
            self.vel_y += -self.vel_y * Player.FRICTION
        else:
            self.vel_x, self.vel_y = 0, 0

        # ==================== Checking for Boundary =================================================================

        l_temp_pos_x = self.pos_x + self.vel_x * g_time_per_frame_in_seconds
        l_temp_pos_y = self.pos_y + self.vel_y * g_time_per_frame_in_seconds

        if l_temp_pos_x > g_screen_dimensions[0] - Player.SIZE_X:
            l_temp_pos_x = g_screen_dimensions[0] - Player.SIZE_X
        elif l_temp_pos_x < 0:
            l_temp_pos_x = 0

        if l_temp_pos_y > g_screen_dimensions[1] - Player.SIZE_Y:
            l_temp_pos_y = g_screen_dimensions[1] - Player.SIZE_Y
        elif l_temp_pos_y < 0:
            l_temp_pos_y = 0

        # ==================== Updating Positions of both the Player and its Hit Box Rect ===========================

        self.pos_x = self.hit_box.left = l_temp_pos_x
        self.pos_y = self.hit_box.top = l_temp_pos_y

    def draw(self, scr):

        # ==================== Drawing the Player =================================================================

        pygame.draw.rect(scr, self.color, self.hit_box)

    def hit(self):

        # ==================== When Player is Hit =================================================================

        self.lives -= 1

        if self.lives <= 0:
            self.kill()
        else:
            self.stun()

    def stun(self):

        # ==================== When Player is Stunned start a stun timer ============================================

        self.acc = Player.STUN_ACC
        self.color = pygame.Color(Player.STUN_COLOR)

        if not self.stun_timer:
            self.stun_timer = Timer(Player.STUN_TIME, self.un_stun)
            self.stun_timer.start()

        else:
            if self.stun_timer.is_alive():
                self.stun_timer.cancel()

            self.stun_timer = Timer(Player.STUN_TIME, self.un_stun)
            self.stun_timer.start()

    def un_stun(self):

        # ==================== Called when stun timer ends ===========================================================

        self.acc = Player.REG_ACC
        self.color = pygame.Color(Player.REG_COLOR)
        print("unstunned")

    def kill(self):

        # ==================== When Player is Killed =================================================================

        global g_game_running

        if self.stun_timer:
            self.stun_timer.cancel()

        g_game_running = False
        print("Score " + get_score())


def render():

    # ====================  All the Rendering Process  =============================================================

    global g_screen_dimensions, g_screen, g_asshole_spawner, g_font, g_font_size, g_score, g_score_text

    g_screen.fill(pygame.Color("black"))

    g_score_text = g_font.render("Score: " + get_score(), True, (255, 255, 255))
    g_lives_text = g_font.render("Lives: " + str(g_player.lives), True, (255, 255, 255))

    g_screen.blit(g_score_text,
                  (g_screen_dimensions[0]//2 - g_score_text.get_rect().width//2, g_screen_dimensions[1] - g_font_size))

    g_screen.blit(g_lives_text, (g_font_screen_offset, g_screen_dimensions[1] - g_font_size))

    g_asshole_spawner.draw(g_screen)
    g_player.draw(g_screen)

    pygame.display.flip()


def logic():

    # ====================  Input Included in Player.move()  =======================================================

    global g_player, g_asshole_spawner

    g_player.move()
    g_asshole_spawner.move()


def init():

    # ====================  Global Initialization  =================================================================

    global g_game_running, g_player, g_score, g_font, g_screen, g_asshole_spawner, g_font, g_font_size, g_font_style

    pygame.init()

    g_font = pygame.font.SysFont(g_font_style, g_font_size)

    g_screen = pygame.display.set_mode(g_screen_dimensions)
    pygame.display.set_caption(g_screen_title)

    g_player = Player(g_screen_dimensions[0] // 2, g_screen_dimensions[1] // 2)
    g_asshole_spawner = AssholeSpawner(g_player)


def get_score():

    # ====================  Returns a string with rounded score =====================================================

    return str(math.trunc(g_score))


def check_score_and_increase_difficulty():

    # ====================  Checks if the Score lies between a range and increases the difficulty ===================
    # ====================  along with the Score Increment Value when it crosses the upper bound ====================
    # ====================  then updates the upper bound to 1.5 times the lower bound ===============================
    # ====================  and the lower bound to the old value of upper bound =====================================
    # ====================  Thereby creating a dynamic range of levels of difficulty which is =======================

    # ====================  [g_check_score_min_bound, 1.5 * g_check_score_min_bound] ================================

    global g_score_frame_increment, g_check_score_min_bound, g_asshole_spawner

    if g_check_score_min_bound < g_score < g_check_score_multiplier * g_check_score_min_bound:
        g_score_frame_increment += 0.02

    elif g_score > g_check_score_multiplier * g_check_score_min_bound:
        g_asshole_spawner.increase_difficulty()
        g_check_score_min_bound *= g_check_score_multiplier


def update_score(l_value):

    # ====================  Pass Value to Update Score  =============================================================

    global g_score
    g_score += l_value * g_time_per_frame_in_seconds


def main():

    # ====================  Main Loop  =================================================================

    global g_game_running, g_time_per_frame_in_milli_seconds, g_score_frame_increment

    init()

    while g_game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g_game_running = False

        logic()
        render()
        update_score(g_score_frame_increment)
        check_score_and_increase_difficulty()
        pygame.time.delay(math.trunc(g_time_per_frame_in_milli_seconds))

    pygame.quit()
    quit()


if __name__ == "__main__":

    # ====================  Global Declaration  =================================================================

    g_screen_dimensions = (1600, 900)
    g_screen_title = "Dodger"
    g_screen = None

    g_frame_rate = 60
    g_time_per_frame_in_seconds = 1.0/g_frame_rate
    g_time_per_frame_in_milli_seconds = g_time_per_frame_in_seconds * 1000

    g_game_running = True

    g_player = None
    g_asshole_spawner = None

    g_score = 0
    g_score_frame_increment = 1

    g_font = None
    g_font_size = 32
    g_font_style = "comicsansms"
    g_score_text = None
    g_font_screen_offset = 10

    # ====================  A Min Score for Dynamic Difficulty Increase ============================================

    g_check_score_min_bound = 2
    g_check_score_multiplier = 1.5

    main()

