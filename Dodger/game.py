import pygame
import math
from random import randint
from threading import Thread
from time import sleep


class AssholeSpawner:

    def __init__(self, l_player):

        # ==================== AssholeSpawner Constructor ==========================================================
        # ==================== Needs a player instance for collision detection =====================================

        self.assholes = []
        self.thread_spawner = Thread(target=self.__spawn)
        self.temp_pos_x = 0
        self.temp_vel = 0
        self.temp_size = 0

        self.player = l_player

        # ==================== Starting Spawning Thread ============================================================

        self.thread_spawner.start()

    def __spawn(self):

        # ==================== Spawn function called by thread_spawner =============================================
        # ==================== Uses random values for x-position, velocity and size of an asshole ==================
        # ==================== After Spawning takes a break for few seconds ========================================

        while g_game_running:
            self.temp_pos_x = randint(0, g_screen_dimensions[0])
            self.temp_vel = randint(1, 5)
            self.temp_size_x = self.temp_size_y = randint(8, 20)
            self.assholes.append(AssholeSpawner.Asshole(self.temp_pos_x, -self.temp_size_y, self.temp_vel,
                                                        self.temp_size_x, self.temp_size_y))
            sleep(0.7)

    def move(self):

        # ==================== Movement Logic for All Assholes ======================================================

        for asshole in self.assholes:
            asshole.move()

            # ==================== Check if Asshole Collided with Player ==========================================

            if asshole.check_player_collision(self.player):
                global g_game_running
                g_game_running = False

            # ==================== Check if Asshole crossed the Boundary to Assguard ================================

            if asshole.pos_y > g_screen_dimensions[1]:
                self.assholes.remove(asshole)

    def draw(self, scr):

        # ==================== Drawing all Assholes =================================================================

        for asshole in self.assholes:
            asshole.draw(scr)

    # ==================== Inner Class Asshole for Spawner to create instances of ==================================
    class Asshole:

        def __init__(self, l_pos_x, l_pos_y, l_vel, l_size_x, l_size_y):

            # ==================== Asshole Constructor ==========================================================

            self.pos_x = l_pos_x
            self.pos_y = l_pos_y
            self.velocity = l_vel
            self.size_x = l_size_x
            self.size_y = l_size_y
            self.color = pygame.Color("red")
            self.hit_box = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)

        def move(self):

            # ==================== Updating Asshole's Position  ==================================================
            # ==================== Along with its hit box =======================================================

            self.pos_y = self.hit_box.top = self.pos_y + self.velocity

        def draw(self, scr):

            # ==================== Drawing the Asshole ===========================================================

            pygame.draw.rect(scr, self.color, self.hit_box)

        def check_player_collision(self, l_player):

            # ==================== Returns True if Asshole is colliding with the Player ===========================

            if self.hit_box.colliderect(l_player.hit_box):
                return True


class Player:

    # ==================== Player Class Variables =================================================================

    SIZE_X = 16
    SIZE_Y = 16
    ACC = 5
    MAX_VELOCITY = 7
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

        l_temp_pos_x = self.pos_x + self.vel_x
        l_temp_pos_y = self.pos_y + self.vel_y

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


def render():

    # ====================  All the Rendering Process  =============================================================

    global g_screen, g_asshole_spawner

    g_screen.fill(pygame.Color("black"))
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

    global g_game_running, g_player, g_score, g_font, g_screen, g_asshole_spawner

    pygame.init()

    g_screen = pygame.display.set_mode(g_screen_dimensions)
    pygame.display.set_caption(g_screen_title)

    g_player = Player(g_screen_dimensions[0] // 2, g_screen_dimensions[1] // 2)
    g_asshole_spawner = AssholeSpawner(g_player)


def update_score(l_value):

    # ====================  Pass Value to Update Score  =============================================================

    global g_score
    g_score += l_value


def main():

    # ====================  Main Loop  =================================================================

    global g_game_running

    init()

    while g_game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g_game_running = False

        logic()
        render()
        update_score(0.1)
        pygame.time.delay(17)

    pygame.quit()
    quit()


if __name__ == "__main__":

    # ====================  Global Declaration  =================================================================

    g_screen_dimensions = (800, 600)
    g_screen_title = "Dodger"
    g_screen = None
    g_game_running = True
    g_player = None
    g_asshole_spawner = None
    g_score = 0
    g_font = None

    main()

