import pygame
import math
from random import randint
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
    INFO_CODE_HIT_ONCE = 1

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

        self.__rebound_sound = pygame.mixer.Sound("Sounds/sfx_rebound.wav")
        self.__rebound_sound.set_volume(0.5)

        self.__coin_collect_sound_single = pygame.mixer.Sound("Sounds/sfx_coin_single.wav")
        self.__coin_collect_sound_single.set_volume(0.6)

        self.__coin_collect_sound_double = pygame.mixer.Sound("Sounds/sfx_coin_double.wav")
        self.__coin_collect_sound_double.set_volume(0.6)

        self.__one_up_sound = pygame.mixer.Sound("Sounds/sfx_coin_cluster.wav")
        self.__one_up_sound.set_volume(0.7)

        self.__damage_sounds = [pygame.mixer.Sound("Sounds/sfx_sounds_damage1.wav"),
                                pygame.mixer.Sound("Sounds/sfx_sounds_damage2.wav")]
        self.__damage_sounds[0].set_volume(0.7)
        self.__damage_sounds[1].set_volume(0.7)

        self.__REG_COLOR_IN = l_reg_color_in
        self.__REG_COLOR_OUT = _l_reg_color_out
        self.__STUN_COLOR_IN = l_stun_color_in
        self.__STUN_COLOR_OUT = l_stun_color_out

        self.__screen_width = l_screen_width
        self.__screen_height = l_screen_height
        self.__bottom_offset = l_bottom_offset
        self.__original_pos_x = l_pos_x
        self.__original_pos_y = l_pos_y
        self.__pos_x = l_pos_x
        self.__pos_y = l_pos_y
        self.__vel_x = 0
        self.__vel_y = 0
        self.__acc = self.__reg_acc

        self.__inner_color = self.__REG_COLOR_IN
        self.__outer_color = self.__REG_COLOR_OUT

        self.__stroke_width = l_screen_width/800

        self.__hit_box = pygame.Rect(self.__pos_x, self.__pos_y, self.__size, self.__size)
        self.__inner_box = pygame.Rect(self.__pos_x + self.__stroke_width, self.__pos_y + self.__stroke_width,
                                       self.__size - 2 * self.__stroke_width, self.__size - 2 * self.__stroke_width)

        self.__lives = 3
        self.__current_dir = None

        self.__keys = None
        self.__dx, self.__dy = 0, 0

        self.__stun_timer = None
        self.__time_stunned = 0
        self.__time_stunned_remaining = 0

        self.__one_up_count = 0

        self.__has_been_hit_once = False
        self.__is_stunned = False
        self.__is_alive = True

    def move_left(self):
        if self.__dx != 1:
            self.__dx = -1
            self.__dy = 0
            return True
        return False

    def move_right(self):
        if self.__dx != -1:
            self.__dx = 1
            self.__dy = 0
            return True
        return False

    def move_up(self):
        if self.__dy != 1:
            self.__dy = -1
            self.__dx = 0
            return True
        return False

    def move_down(self):
        if self.__dy != -1:
            self.__dy = 1
            self.__dx = 0
            return True
        return False

    def move(self, dt):

        # ==================== Accelerating Player till reaching Max Velocity =========================================

        if not self.__is_alive:
            return Player.ERR_CODE_DEATH

        if self.__has_been_hit_once:
            self.__has_been_hit_once = False
            return Player.INFO_CODE_HIT_ONCE

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
                self.play_rebound_sound()

        elif l_temp_pos_x < 0:
            l_temp_pos_x = 0
            if self.__dx < 0:
                self.__dx = 1
                self.play_rebound_sound()

        if l_temp_pos_y > self.__screen_height - self.__size:
            l_temp_pos_y = self.__screen_height - self.__size
            if self.__dy > 0:
                self.__dy = -1
                self.play_rebound_sound()

        elif l_temp_pos_y < self.__bottom_offset:
            l_temp_pos_y = self.__bottom_offset
            if self.__dy < 0:
                self.__dy = 1
                self.play_rebound_sound()

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

        if self.__one_up_count == 3:
            if self.__lives < Player.MAX_LIVES:
                self.__lives += 1

            self.play_one_up_sound()
            self.__one_up_count = 0
        elif self.__one_up_count == 2:
            self.play_coin_collect_sound_double()
        elif self.__one_up_count == 1:
            self.play_coin_collect_sound_single()

    def hit(self):

        # ==================== When Player is Hit =================================================================
        self.__has_been_hit_once = True

        self.__lives -= 1
        self.play_damage_sound()
        if self.__lives <= 0:
            self.kill()
        else:
            self.stun()

    def stun(self):

        # ==================== When Player is Stunned start a stun timer ============================================

        self.__is_stunned = True

        self.__acc = self.__stun_acc
        self.__inner_color = self.__STUN_COLOR_IN
        self.__outer_color = self.__STUN_COLOR_OUT

        if not self.__stun_timer:
            self.__stun_timer = Timer(Player.STUN_TIME, self.un_stun)
            self.__stun_timer.start()

        else:
            if self.__stun_timer.is_alive():
                self.__stun_timer.cancel()

            self.__stun_timer = Timer(Player.STUN_TIME, self.un_stun)
            self.__stun_timer.start()

    def un_stun(self):

        # ==================== Called when stun timer ends ===========================================================
        self.__is_stunned = False

        self.__acc = self.__reg_acc
        self.__inner_color = self.__REG_COLOR_IN
        self.__outer_color = self.__REG_COLOR_OUT

    def kill(self):

        # ==================== When Player is Killed =================================================================

        self.__is_alive = False

        if self.__stun_timer:
            self.__stun_timer.cancel()

    def reset(self):

        if self.__is_stunned:
            self.un_stun()

        self.__is_alive = True
        self.__lives = 3
        self.__current_dir = None

        self.__keys = None
        self.__dx, self.__dy = 0, 0

        self.__stun_timer = None
        self.__time_stunned = 0
        self.__time_stunned_remaining = 0

        self.__one_up_count = 0
        self.__has_been_hit_once = False

        self.__pos_x = self.__original_pos_x
        self.__pos_y = self.__original_pos_y
        self.__vel_x = 0
        self.__vel_y = 0

        # ==================== All Sounds =================================================================

    def play_rebound_sound(self):
        pygame.mixer.Sound.play(self.__rebound_sound)

    def play_coin_collect_sound_single(self):
        pygame.mixer.Sound.play(self.__coin_collect_sound_single)

    def play_coin_collect_sound_double(self):
        pygame.mixer.Sound.play(self.__coin_collect_sound_double)

    def play_one_up_sound(self):
        pygame.mixer.Sound.play(self.__one_up_sound)

    def play_damage_sound(self):
        pygame.mixer.Sound.play(self.__damage_sounds[randint(0, len(self.__damage_sounds)-1)])

    # ==================== Getters and Setters =================================================================

    def get_lives(self):
        return self.__lives

    def get_hitbox(self):
        return self.__hit_box

    def get_is_alive(self):
        return self.__is_alive

    def get_size(self):
        return self.__size
