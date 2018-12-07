import pygame
import math
import time
from enemy_spawner import EnemySpawner
from powerup_spawner import PowerupSpawner
from player import Player


class Game:

    # ==================== Color Scheme ==========================================================================

    # red

    # CLR_BG = CLR_FDE = (170, 57, 57)
    # CLR_UI_BG = CLR_PLR_STN_OUT = CLR_PLR_STN_IN = CLR_ENM = (101, 9, 9)
    # CLR_UI_TXT_LIF = CLR_UI_TXT_SCR = (239, 137, 137)
    # CLR_POW_LIF_OUT = (255, 255, 255)
    # CLR_POW_LIF_IN = (204, 93, 93)
    # CLR_PLR_REG_OUT = (239, 137, 137)
    # CLR_PLR_REG_IN = (239, 137, 137)

    # blue

    # CLR_BG = CLR_FDE = (42, 78, 110)
    # CLR_UI_BG = CLR_PLR_STN_OUT = CLR_PLR_STN_IN = CLR_ENM = (4, 31, 55)
    # CLR_UI_TXT_LIF = CLR_UI_TXT_SCR = (114, 141, 165)
    # CLR_POW_LIF_OUT = (255, 255, 255)
    # CLR_POW_LIF_IN = CLR_PLR_REG_OUT = CLR_PLR_REG_IN = (114, 141, 165)

    # brown

    CLR_BG = CLR_FDE = (90, 63, 49)
    CLR_UI_BG = CLR_PLR_STN_OUT = CLR_PLR_STN_IN = CLR_ENM = (50, 37, 30)
    CLR_UI_TXT_LIF = CLR_UI_TXT_SCR = (142, 91, 66)
    CLR_POW_LIF_OUT = (223, 151, 117)
    CLR_POW_LIF_IN = CLR_PLR_REG_OUT = CLR_PLR_REG_IN = (201, 111, 66)

    def __init__(self, l_screen_title, l_frame_rate):

        self.__screen_title = l_screen_title

        self.__frame_rate = l_frame_rate
        self.__time_per_frame_in_seconds = 1.0/l_frame_rate
        self.__time_per_frame_in_milli_seconds = self.__time_per_frame_in_seconds * 1000

        self.__game_running = True
        self.__playing = True

        self.__score = 0
        self.__score_frame_increment = 1

        self.__score_text = None
        self.__lives_text = None
        self.__win_message = None
        self.__win_restart_message = None
        self.__win_exit_message = None
        self.__dev_message = None

        self.__soundtrack = "Eye of the Storm.ogg"

        # ====================  A Min Score for Dynamic Difficulty Increase ============================================

        self.__check_score_min_bound = 2
        self.__check_score_multiplier = 1.4

        pygame.init()

        self.__info_object = pygame.display.Info()

        self.__screen_width = self.__info_object.current_w
        self.__screen_height = self.__info_object.current_h

        self.__font_size = self.__screen_height // 38
        self.__small_font_size = self.__screen_height // 52
        self.__font_name = "Amiko-Regular.ttf"
        self.__font_screen_offset = self.__screen_height//28

        self.__font = pygame.font.Font(self.__font_name, self.__font_size)
        self.__small_font = pygame.font.Font(self.__font_name, self.__small_font_size)

        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption(self.__screen_title)
        pygame.mouse.set_visible(False)

        # ====================  INIT ===================================================================================

        self.__player = Player(self.__screen_width // 2, self.__screen_height // 2,
                               Game.CLR_PLR_REG_IN, Game.CLR_PLR_REG_OUT, Game.CLR_PLR_STN_IN, Game.CLR_PLR_STN_OUT,
                               self.__screen_width, self.__screen_height,
                               self.__font_screen_offset)
        self.__player_direction_change_sounds = [pygame.mixer.Sound("Sounds/sfx_walk1.wav"),
                                                 pygame.mixer.Sound("Sounds/sfx_walk3.wav")]
        self.__player_direction_change_sounds_last_index = -1

        for sound in self.__player_direction_change_sounds:
            sound.set_volume(0.5)

        self.__enemy_spawner = EnemySpawner(self.__player,
                                            self.CLR_ENM, self.CLR_FDE,
                                            self.__screen_width, self.__screen_height,
                                            self.__font_screen_offset)

        self.__powerup_spawner = PowerupSpawner(self.__player,
                                                self.CLR_POW_LIF_IN, self.CLR_POW_LIF_OUT, self.CLR_FDE,
                                                self.__screen_width, self.__screen_height,
                                                self.__font_screen_offset)

        self.__time_without_hit = time.time()
        self.__player_code = -1

        pygame.mixer.music.load(self.__soundtrack)
        pygame.mixer.music.play(-1)

    def play(self):

        while self.__game_running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.__game_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__game_running = False

                    if self.__playing:
                        if event.key == pygame.K_LEFT and self.__player.move_left():
                            self.play_player_direction_change_sound(0)
                        elif event.key == pygame.K_RIGHT and self.__player.move_right():
                            self.play_player_direction_change_sound(0)
                        if event.key == pygame.K_UP and self.__player.move_up():
                            self.play_player_direction_change_sound(1)
                        elif event.key == pygame.K_DOWN and self.__player.move_down():
                            self.play_player_direction_change_sound(1)

                    elif event.key == pygame.K_RETURN:
                        self.reset()

            self.logic()
            self.draw()
            self.update_score(self.__score_frame_increment)
            self.check_score_and_increase_difficulty()
            pygame.time.delay(math.trunc(self.__time_per_frame_in_milli_seconds))

        pygame.quit()

    def logic(self):

        self.__enemy_spawner.move(self.__time_per_frame_in_seconds)
        self.__powerup_spawner.move(self.__time_per_frame_in_seconds)

        self.__player_code = self.__player.move(self.__time_per_frame_in_seconds)

        if self.__player_code == Player.ERR_CODE_DEATH:
            # print("Score: " + self.get_score())
            self.stop()
        elif self.__player_code == Player.INFO_CODE_HIT_ONCE:
            self.__time_without_hit = time.time() - self.__time_without_hit
            # print("Time Survived: " + str(round(self.__time_without_hit)) + " seconds")
            self.__time_without_hit = time.time()

    def draw(self):

        self.draw_background()
        self.draw_entities()
        self.draw_ui()

        pygame.display.flip()

    def draw_background(self):
        self.__screen.fill(Game.CLR_BG)

    def draw_entities(self):
        self.__enemy_spawner.draw(self.__screen)
        self.__powerup_spawner.draw(self.__screen)
        self.__player.draw(self.__screen)

    def draw_ui(self):
        pygame.draw.rect(self.__screen, Game.CLR_UI_BG,
                         (0, 0, self.__screen_width, self.__font_screen_offset))
        self.__score_text = self.__font.render(self.get_score(), True, Game.CLR_UI_TXT_SCR)
        self.__dev_message = self.__font.render("Klad Spear", True, Game.CLR_UI_TXT_SCR)

        if not self.__playing:
            self.__win_message = self.__font.render("GAME OVER!", True, Game.CLR_UI_BG)
            self.__win_restart_message = self.__small_font.render("Press Enter to restart...", True, Game.CLR_UI_BG)
            self.__win_exit_message = self.__small_font.render("or Escape to exit", True, Game.CLR_UI_BG)

            self.__screen.blit(self.__win_message,
                               ((self.__screen_width - self.__win_message.get_rect().width) // 2,
                                (self.__screen_height - self.__win_message.get_rect().height) // 2
                                - self.__font_screen_offset))
            self.__screen.blit(self.__win_restart_message,
                               ((self.__screen_width - self.__win_restart_message.get_rect().width) // 2,
                                (self.__screen_height - self.__win_restart_message.get_rect().height) // 2))
            self.__screen.blit(self.__win_exit_message,
                               ((self.__screen_width - self.__win_exit_message.get_rect().width) // 2,
                                (self.__screen_height - self.__win_exit_message.get_rect().height) // 2
                                + 0.7 * self.__font_screen_offset))

        self.__screen.blit(self.__score_text,
                           (self.__screen_width // 2 - self.__score_text.get_rect().width // 2,
                            (self.__font_screen_offset - self.__font_size)//2))

        self.__screen.blit(self.__dev_message,
                           (self.__screen_width - 1.05 * self.__dev_message.get_rect().width,
                            self.__screen_height - self.__dev_message.get_rect().height))

        for i in range(self.__player.get_lives()):
            pygame.draw.rect(self.__screen, Game.CLR_PLR_REG_IN,
                             (8 + i * (self.__player.get_size() + self.__font_screen_offset//3),
                              (self.__font_screen_offset - self.__player.get_size())//2 + 1,
                              self.__player.get_size() - 2, self.__player.get_size() - 2))

    def get_score(self):
        return str(math.trunc(self.__score))

    def update_score(self, l_value):
        self.__score += l_value * self.__time_per_frame_in_seconds

    def check_score_and_increase_difficulty(self):

        # ====================  Checks if the Score lies between a range and increases the difficulty =================
        # ====================  along with the Score Increment Value when it crosses the upper bound ==================
        # ====================  then updates the upper bound to 1.5 times the lower bound =============================
        # ====================  and the lower bound to the old value of upper bound ===================================
        # ====================  Thereby creating a dynamic range of levels of difficulty which is =====================
        # ====================  [g_check_score_min_bound, 1.5 * g_check_score_min_bound] ==============================

        if not self.__playing:
            return

        if self.__check_score_min_bound < self.__score < self.__check_score_multiplier * self.__check_score_min_bound:
            self.__score_frame_increment += 0.02

        elif self.__score > self.__check_score_multiplier * self.__check_score_min_bound:
            self.__enemy_spawner.increase_difficulty()
            self.__powerup_spawner.increase_difficulty()
            self.__check_score_min_bound *= self.__check_score_multiplier

    def stop(self):
        self.__playing = False
        self.__score_frame_increment = 0
        self.__player_direction_change_sounds_last_index = -1
        self.__time_without_hit = time.time()
        self.__check_score_min_bound = 2

    def reset(self):
        self.__playing = True
        self.__powerup_spawner.stop()
        self.__enemy_spawner.stop()

        self.__score = 0
        self.__score_frame_increment = 1
        self.__player_direction_change_sounds_last_index = -1
        self.__time_without_hit = time.time()
        self.__check_score_min_bound = 2

        self.__player.reset()
        self.__enemy_spawner.reset()
        self.__powerup_spawner.reset()

    def play_player_direction_change_sound(self, l_index):
        if self.__player_direction_change_sounds_last_index == -1:
            self.__player_direction_change_sounds[l_index].play()
            self.__player_direction_change_sounds_last_index = l_index
        else:
            if l_index != self.__player_direction_change_sounds_last_index:
                self.__player_direction_change_sounds[self.__player_direction_change_sounds_last_index].stop()
                self.__player_direction_change_sounds[l_index].play()
                self.__player_direction_change_sounds_last_index = l_index
