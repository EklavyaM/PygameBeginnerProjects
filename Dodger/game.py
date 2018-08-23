import pygame
import math
from random import randint
from threading import Thread
from time import sleep


class AssholeSpawner:

    def __init__(self, l_player):

        # ==================== AssholeSpawner Constructor ==========================================================
        # ==================== Needs a player instance for collision detection =====================================

        self.__assholes = []
        self.__thread_spawner = Thread(target=self.__spawn)
        self.__sleep_time = 0.07
        self.__temp_pos_x = 0
        self.__temp_vel = 0
        self.__temp_size_x = 0
        self.__temp_size_y = 0

        self.__player = l_player

        # ==================== Starting Spawning Thread ============================================================

        self.__thread_spawner.start()

    def __spawn(self):

        # ==================== Spawn function called by thread_spawner =============================================
        # ==================== Uses random values for x-position, velocity and size of an asshole ==================
        # ==================== After Spawning takes a break for few seconds ========================================

        # ==================== Change values for different asshole behavior and visuals ============================

        while g_game_running:
            self.__temp_pos_x = randint(0, g_game_area_dimensions[0])
            self.__temp_vel = randint(100, 500)
            self.__temp_size_x = self.__temp_size_y = randint(8, 20)
            self.__assholes.append(AssholeSpawner.Asshole(self.__temp_pos_x, -self.__temp_size_y, self.__temp_vel,
                                                          self.__temp_size_x, self.__temp_size_y))
            sleep(self.__sleep_time)

    def move(self):

        # ==================== Movement Logic for All Assholes ======================================================

        for asshole in self.__assholes:

            if asshole.get_is_destroyed():
                self.__assholes.remove(asshole)
                continue

            asshole.move()
            asshole.boundary_check()

            # ==================== Check if Asshole Collided with Player ==========================================

            # if asshole.check_player_collision(self.player):
            #     global g_game_running
            #     g_game_running = False
            #
            #     print("Score: " + get_score())

    def draw(self, scr):

        # ==================== Drawing all Assholes =================================================================

        for asshole in self.__assholes:
            asshole.draw(scr)

    # ==================== Inner Class Asshole for Spawner to create instances of ==================================
    class Asshole:

        def __init__(self, l_pos_x, l_pos_y, l_vel, l_size_x, l_size_y):

            # ==================== Asshole Constructor ==========================================================

            self.__pos_x = l_pos_x
            self.__pos_y = l_pos_y
            self.__velocity = l_vel
            self.__size_x = l_size_x
            self.__size_y = l_size_y
            self.__color = pygame.Color("red")
            self.__is_destroyed = False
            self.__has_collided = False
            self.__hit_box = pygame.Rect(self.__pos_x, self.__pos_y, self.__size_x, self.__size_y)

        def move(self):

            # ==================== Updating Asshole's Position  ==================================================
            # ==================== Along with its hit box =======================================================

            if not self.__has_collided:
                self.__pos_y = self.__hit_box.top = self.__pos_y + self.__velocity * g_time_per_frame_in_seconds
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

            # ==================== Check if Asshole crossed the Boundary to Assguard ================================

        def boundary_check(self):
            if self.__pos_y + self.__size_y > g_game_area_dimensions[1]:
                self.__has_collided = True


class Player:

    # ==================== Player Class Variables =================================================================

    SIZE_X = 16
    SIZE_Y = 16
    ACC = 200
    MAX_VELOCITY = 500
    MIN_VELOCITY = 0.5
    FRICTION = 0.3

    def __init__(self, l_pos_x, l_pos_y):

        # ==================== Player Constructor =================================================================

        self.pos_x = l_pos_x
        self.pos_y = l_pos_y
        self.vel_x = 0
        self.vel_y = 0
        self.hit_box = pygame.Rect(self.pos_x, self.pos_y, Player.SIZE_X, Player.SIZE_Y)
        self.color = pygame.Color("white")

    def move(self):

        # ==================== Polling for Input =================================================================

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # ==================== Accelerating Player till reaching Max Velocity =========================================

        updated_vel_x = self.vel_x + dx * Player.ACC
        updated_vel_y = self.vel_y + dy * Player.ACC

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

        if l_temp_pos_x > g_game_area_dimensions[0] - Player.SIZE_X:
            l_temp_pos_x = g_game_area_dimensions[0] - Player.SIZE_X
        elif l_temp_pos_x < 0:
            l_temp_pos_x = 0

        if l_temp_pos_y > g_game_area_dimensions[1] - Player.SIZE_Y:
            l_temp_pos_y = g_game_area_dimensions[1] - Player.SIZE_Y
        elif l_temp_pos_y < 0:
            l_temp_pos_y = 0

        # ==================== Updating Positions of both the Player and its Hit Box Rect ===========================

        self.pos_x = self.hit_box.left = l_temp_pos_x
        self.pos_y = self.hit_box.top = l_temp_pos_y

    def draw(self, scr):

        # ==================== Drawing the Player =================================================================

        pygame.draw.rect(scr, self.color, self.hit_box)


def render():

    # ====================  All the Rendering Process  =============================================================

    global g_screen_dimensions, g_screen, g_asshole_spawner, g_font, g_font_size, g_score, g_score_text

    g_screen.fill(pygame.Color("black"))

    g_score_text = g_font.render("Score: " + get_score(), True, (255, 255, 255))
    g_screen.blit(g_score_text,
                  (g_screen_dimensions[0]//2 - g_score_text.get_rect().width//2, g_screen_dimensions[1] - g_font_size))

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

    g_player = Player(g_game_area_dimensions[0] // 2, g_game_area_dimensions[1] // 2)
    g_asshole_spawner = AssholeSpawner(g_player)


def get_score():

    # ====================  Returns a string with rounded score =====================================================

    return str(math.ceil(g_score))


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
        pygame.time.delay(math.trunc(g_time_per_frame_in_milli_seconds))

    pygame.quit()
    quit()


if __name__ == "__main__":

    # ====================  Global Declaration  =================================================================

    g_screen_dimensions = (1366, 768)
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

    g_game_area_dimensions = (g_screen_dimensions[0], g_screen_dimensions[1] - g_font_size)

    main()

