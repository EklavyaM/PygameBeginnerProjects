import pygame
import math
from threading import Timer


class Player:

    # ==================== Player Class Variables =================================================================

    STUN_TIME = 3.5
    MIN_VELOCITY = 0.5
    FRICTION = 0.4

    DIR_UP = 0
    DIR_DOWN = 1
    DIR_LEFT = 2
    DIR_RIGHT = 3

    ERR_CODE_DEATH = 0

    MAX_LIVES = 5

    def __init__(self, l_pos_x, l_pos_y,
                 l_reg_color_in, _l_reg_color_out, l_stun_color_in, l_stun_color_out,
                 l_screen_width, l_screen_height,
                 l_bottom_offset):

        # ==================== Player Constructor =================================================================

        self.__size = l_screen_width/100
        self.__reg_acc = l_screen_width/6.5
        self.__stun_acc = self.__reg_acc/4
        self.__max_velocity = l_screen_width/3.6

        self.__REG_COLOR_IN = l_reg_color_in
        self.__REG_COLOR_OUT = _l_reg_color_out
        self.__STUN_COLOR_IN = l_stun_color_in
        self.__STUN_COLOR_OUT = l_stun_color_out

        self.__is_alive = True
        self.__screen_width = l_screen_width
        self.__screen_height = l_screen_height
        self.__bottom_offset = l_bottom_offset
        self.__pos_x = l_pos_x
        self.__pos_y = l_pos_y
        self.__vel_x = 0
        self.__vel_y = 0
        self.__acc = self.__reg_acc

        self.__inner_color = self.__REG_COLOR_IN
        self.__outer_color = self.__REG_COLOR_OUT

        self.__stroke_width = 2

        self.__hit_box = pygame.Rect(self.__pos_x, self.__pos_y, self.__size, self.__size)
        self.__inner_box = pygame.Rect(self.__pos_x + self.__stroke_width, self.__pos_y + self.__stroke_width,
                                       self.__size - 2 * self.__stroke_width, self.__size - 2 * self.__stroke_width)

        self.__lives = 3
        self.__current_dir = None

        self.__keys = None
        self.__dx, self.__dy = 0, 0

        self.stun_timer = None

        self.__one_up_count = 0

    def input(self):

        # ==================== Polling for Input =================================================================

        self.__keys = pygame.key.get_pressed()

        if self.__dx != 1 and (self.__keys[pygame.K_LEFT] or self.__keys[pygame.K_a]):
            self.__dy = 0
            self.__dx = -1
        if self.__dx != -1 and (self.__keys[pygame.K_RIGHT] or self.__keys[pygame.K_d]):
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

        if math.fabs(updated_vel_x) < self.__max_velocity:
            self.__vel_x = updated_vel_x
        else:
            self.__vel_x = math.copysign(self.__max_velocity, updated_vel_x)

        if math.fabs(updated_vel_y) < self.__max_velocity:
            self.__vel_y = updated_vel_y
        else:
            self.__vel_y = math.copysign(self.__max_velocity, updated_vel_y)

        # ==================== Applying Friction and =================================================================
        # ==================== Stopping all motion when velocity is less than a certain value ========================
        # ==================== which is Player.MIN_VELOCITY in this case =============================================

        if math.fabs(self.__vel_x) > Player.MIN_VELOCITY:
            self.__vel_x += -self.__vel_x * Player.FRICTION
        else:
            self.__vel_x = 0
        if math.fabs(self.__vel_y) > Player.MIN_VELOCITY:
            self.__vel_y += -self.__vel_y * Player.FRICTION
        else:
            self.__vel_y = 0

        # ==================== Checking for Boundary =================================================================

        l_temp_pos_x = self.__pos_x + self.__vel_x * dt
        l_temp_pos_y = self.__pos_y + self.__vel_y * dt

        if l_temp_pos_x > self.__screen_width - self.__size:
            l_temp_pos_x = self.__screen_width - self.__size
            if self.__dx > 0:
                self.__dx = -1
        elif l_temp_pos_x < 0:
            l_temp_pos_x = 0
            if self.__dx < 0:
                self.__dx = 1

        if l_temp_pos_y > self.__screen_height - self.__size:
            l_temp_pos_y = self.__screen_height - self.__size
            if self.__dy > 0:
                self.__dy = -1
        elif l_temp_pos_y < self.__bottom_offset:
            l_temp_pos_y = self.__bottom_offset
            if self.__dy < 0:
                self.__dy = 1

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

    def one_up(self):

        self.__one_up_count += 1

        if self.__one_up_count >= 3:
            if self.__lives < Player.MAX_LIVES:
                self.__lives += 1
            self.__one_up_count = 0

    def hit(self):

        # ==================== When Player is Hit =================================================================

        self.__lives -= 1

        if self.__lives <= 0:
            self.kill()
        else:
            self.stun()

    def stun(self):

        # ==================== When Player is Stunned start a stun timer ============================================

        self.__acc = self.__stun_acc
        self.__inner_color = self.__STUN_COLOR_IN
        self.__outer_color = self.__STUN_COLOR_OUT

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

        self.__acc = self.__reg_acc
        self.__inner_color = self.__REG_COLOR_IN
        self.__outer_color = self.__REG_COLOR_OUT

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

    def get_size(self):
        return self.__size
