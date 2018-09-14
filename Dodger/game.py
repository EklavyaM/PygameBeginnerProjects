import pygame
import math
import time
from enemy_spawner import EnemySpawner
from powerup_spawner import PowerupSpawner
from player import Player


class Game:

    # ==================== Color Scheme ==========================================================================

    # red

    CLR_BG = CLR_FDE = (170, 57, 57)
    CLR_UI_BG = CLR_PLR_STN_OUT = CLR_PLR_STN_IN = CLR_ENM = (101, 9, 9)
    CLR_UI_TXT_LIF = CLR_UI_TXT_SCR = (239, 137, 137)
    CLR_POW_LIF_OUT = (255, 255, 255)
    CLR_POW_LIF_IN = (204, 93, 93)
    CLR_PLR_REG_OUT = (239, 137, 137)
    CLR_PLR_REG_IN = (239, 137, 137)

    # blue

    # CLR_BG = CLR_FDE = (42, 78, 110)
    # CLR_UI_BG = CLR_PLR_STN_OUT = CLR_PLR_STN_IN = CLR_ENM = (4, 31, 55)
    # CLR_UI_TXT_LIF = CLR_UI_TXT_SCR = (114, 141, 165)
    # CLR_POW_LIF_OUT = (255, 255, 255)
    # CLR_POW_LIF_IN = (114, 141, 165)
    # CLR_PLR_REG_OUT = (114, 141, 165)
    # CLR_PLR_REG_IN = (114, 141, 165)

    def __init__(self, l_screen_width, l_screen_height, l_screen_title, l_frame_rate):
        self.__screen_width = l_screen_width
        self.__screen_height = l_screen_height
        self.__screen_title = l_screen_title

        self.__frame_rate = l_frame_rate
        self.__time_per_frame_in_seconds = 1.0/l_frame_rate
        self.__time_per_frame_in_milli_seconds = self.__time_per_frame_in_seconds * 1000

        self.__game_running = True

        self.__score = 0
        self.__score_frame_increment = 1

        self.__font_size = l_screen_height//40
        self.__font_style = "cousine"
        self.__font_screen_offset = self.__font_size + 2

        self.__score_text = None
        self.__lives_text = None

        self.__soundtrack = "Eye of the Storm.mp3"

        # ====================  A Min Score for Dynamic Difficulty Increase ============================================

        self.__check_score_min_bound = 2
        self.__check_score_multiplier = 1.5

        pygame.init()

        self.__font = pygame.font.SysFont(self.__font_style, self.__font_size)

        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        pygame.display.set_caption(self.__screen_title)

        self.__player = Player(self.__screen_width // 2, self.__screen_height // 2,
                               Game.CLR_PLR_REG_IN, Game.CLR_PLR_REG_OUT, Game.CLR_PLR_STN_IN, Game.CLR_PLR_STN_OUT,
                               self.__screen_width, self.__screen_height,
                               self.__font_screen_offset)
        self.__player_direction_change_sounds = [pygame.mixer.Sound("Sounds/sfx_walk1.wav"),
                                                 pygame.mixer.Sound("Sounds/sfx_walk3.wav")]
        self.__player_direction_change_sounds_last_index = -1

        for sound in self.__player_direction_change_sounds:
            sound.set_volume(0.5)

        self.__asshole_spawner = EnemySpawner(self.__player,
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

    def run(self):

        while self.__game_running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.__game_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.__player.move_left():
                        self.play_player_direction_change_sound(0)
                    elif event.key == pygame.K_RIGHT and self.__player.move_right():
                        self.play_player_direction_change_sound(0)
                    if event.key == pygame.K_UP and self.__player.move_up():
                        self.play_player_direction_change_sound(1)
                    elif event.key == pygame.K_DOWN and self.__player.move_down():
                        self.play_player_direction_change_sound(1)

            self.logic()
            self.draw()
            self.update_score(self.__score_frame_increment)
            self.check_score_and_increase_difficulty()
            pygame.time.delay(math.trunc(self.__time_per_frame_in_milli_seconds))

        pygame.quit()
        quit()

    def logic(self):

        self.__asshole_spawner.move(self.__time_per_frame_in_seconds)
        self.__powerup_spawner.move(self.__time_per_frame_in_seconds)

        self.__player_code = self.__player.move(self.__time_per_frame_in_seconds)

        if self.__player_code == Player.ERR_CODE_DEATH:
            print("Score: " + self.get_score())
            self.__game_running = False
        elif self.__player_code == Player.INFO_CODE_HIT_ONCE:
            self.__time_without_hit = time.time() - self.__time_without_hit
            print("Time Survived: " + str(round(self.__time_without_hit)) + " seconds")
            self.__time_without_hit = time.time()

    def draw(self):

        self.draw_background()
        self.draw_entities()
        self.draw_ui()

        pygame.display.flip()

    def draw_background(self):
        self.__screen.fill(Game.CLR_BG)

    def draw_entities(self):
        self.__asshole_spawner.draw(self.__screen)
        self.__powerup_spawner.draw(self.__screen)
        self.__player.draw(self.__screen)

    def draw_ui(self):
        pygame.draw.rect(self.__screen, Game.CLR_UI_BG,
                         (0, 0, self.__screen_width, self.__font_screen_offset))
        self.__score_text = self.__font.render(self.get_score(), True, Game.CLR_UI_TXT_SCR)

        self.__screen.blit(self.__score_text,
                           (self.__screen_width // 2 - self.__score_text.get_rect().width // 2, 0))

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

        if self.__check_score_min_bound < self.__score < self.__check_score_multiplier * self.__check_score_min_bound:
            self.__score_frame_increment += 0.02

        elif self.__score > self.__check_score_multiplier * self.__check_score_min_bound:
            self.__asshole_spawner.increase_difficulty()
            self.__powerup_spawner.increase_difficulty()
            self.__check_score_min_bound *= self.__check_score_multiplier

    def play_player_direction_change_sound(self, l_index):
        if self.__player_direction_change_sounds_last_index == -1:
            self.__player_direction_change_sounds[l_index].play()
            self.__player_direction_change_sounds_last_index = l_index
        else:
            if l_index != self.__player_direction_change_sounds_last_index:
                self.__player_direction_change_sounds[self.__player_direction_change_sounds_last_index].stop()
                self.__player_direction_change_sounds[l_index].play()
                self.__player_direction_change_sounds_last_index = l_index
