import pygame
import math
from threading import Timer


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

    ERR_CODE_DEATH = 0

    def __init__(self, l_pos_x, l_pos_y, l_screen_width, l_screen_height):

        # ==================== Player Constructor =================================================================

        self.__is_alive = True
        self.screen_width = l_screen_width
        self.screen_height = l_screen_height
        self.__pos_x = l_pos_x
        self.__pos_y = l_pos_y
        self.__vel_x = 0
        self.__vel_y = 0
        self.__acc = Player.REG_ACC

        self.__inner_color = pygame.Color(Player.REG_COLOR)
        self.__outer_color = pygame.Color("black")
        self.__stroke_width = 2

        self.__hit_box = pygame.Rect(self.__pos_x, self.__pos_y, Player.SIZE_X, Player.SIZE_Y)
        self.__inner_box = pygame.Rect(self.__pos_x + self.__stroke_width, self.__pos_y + self.__stroke_width,
                                       Player.SIZE_X - 2 * self.__stroke_width, Player.SIZE_Y - 2 * self.__stroke_width)

        self.__lives = 3
        self.__current_dir = None

        self.__keys = None
        self.__dx, self.__dy = 0, 0

        self.stun_timer = None

    def input(self):

        # ==================== Polling for Input =================================================================

        self.__keys = pygame.key.get_pressed()

        if self.__dx != 1 and (self.__keys[pygame.K_LEFT] or self.__keys[pygame.K_a]):
            self.__dy = 0
            self.__dx = -1
        if self.__dx !=-1 and (self.__keys[pygame.K_RIGHT] or self.__keys[pygame.K_d]):
            self.__dy = 0
            self.__dx = 1
        if self.__dy != 1 and (self.__keys[pygame.K_UP] or self.__keys[pygame.K_w]):
            self.__dy = -1
            self.__dx = 0
        if self.__dy != -1 and (self.__keys[pygame.K_DOWN] or self.__keys[pygame.K_s]):
            self.__dy = 1
            self.__dx = 0

    def move(self, dt):

        # ==================== Accelerating Player till reaching Max Velocity =========================================

        if not self.__is_alive:
            return Player.ERR_CODE_DEATH

        updated_vel_x = self.__vel_x + self.__dx * self.__acc
        updated_vel_y = self.__vel_y + self.__dy * self.__acc

        if math.fabs(updated_vel_x) < Player.MAX_VELOCITY:
            self.__vel_x = updated_vel_x
        else:
            self.__vel_x = math.copysign(Player.MAX_VELOCITY, updated_vel_x)

        if math.fabs(updated_vel_y) < Player.MAX_VELOCITY:
            self.__vel_y = updated_vel_y
        else:
            self.__vel_y = math.copysign(Player.MAX_VELOCITY, updated_vel_y)

        # ==================== Applying Friction and =================================================================
        # ==================== Stopping all motion when velocity is less than a certain value ========================
        # ==================== which is Player.MIN_VELOCITY in this case =============================================

        if math.fabs(self.__vel_x) > Player.MIN_VELOCITY or math.fabs(self.__vel_y) > Player.MIN_VELOCITY:
            self.__vel_x += -self.__vel_x * Player.FRICTION
            self.__vel_y += -self.__vel_y * Player.FRICTION
        else:
            self.__vel_x, self.__vel_y = 0, 0

        # ==================== Checking for Boundary =================================================================

        l_temp_pos_x = self.__pos_x + self.__vel_x * dt
        l_temp_pos_y = self.__pos_y + self.__vel_y * dt

        if l_temp_pos_x > self.screen_width:
            l_temp_pos_x = 0
        elif l_temp_pos_x < -Player.SIZE_X:
            l_temp_pos_x = self.screen_width - Player.SIZE_X

        if l_temp_pos_y > self.screen_height:
            l_temp_pos_y = 0
        elif l_temp_pos_y < -Player.SIZE_Y:
            l_temp_pos_y = self.screen_height - Player.SIZE_Y

        self.update_pos(l_temp_pos_x, l_temp_pos_y)

    def update_pos(self, l_pos_x, l_pos_y):

        # ==================== Updating Positions of both the Player and its Hit Box Rect ===========================

        self.__pos_x = self.__hit_box.left = l_pos_x
        self.__pos_y = self.__hit_box.top = l_pos_y
        self.__inner_box.left = self.__pos_x + self.__stroke_width
        self.__inner_box.top = self.__pos_y + self.__stroke_width

    def draw(self, scr):

        # ==================== Drawing the Player =================================================================
        pygame.draw.rect(scr, self.__outer_color, self.__hit_box)
        pygame.draw.rect(scr, self.__inner_color, self.__inner_box)

    def hit(self):

        # ==================== When Player is Hit =================================================================

        self.__lives -= 1

        if self.__lives <= 0:
            self.kill()
        else:
            self.stun()

    def stun(self):

        # ==================== When Player is Stunned start a stun timer ============================================

        self.__acc = Player.STUN_ACC
        self.__inner_color = pygame.Color(Player.STUN_COLOR)

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

        self.__acc = Player.REG_ACC
        self.__inner_color = pygame.Color(Player.REG_COLOR)

    def kill(self):

        # ==================== When Player is Killed =================================================================

        self.__is_alive = False

        if self.stun_timer:
            self.stun_timer.cancel()

    def get_lives(self):
        return self.__lives

    def get_hitbox(self):
        return self.__hit_box

    def get_is_alive(self):
        return self.__is_alive
