import pygame
import math
from spawner import EnemySpawn
from player import Player


class Game:

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

        self.__font_size = l_screen_height//37
        self.__font_style = "cousine"
        self.__font_screen_offset = l_screen_width//160

        self.__score_text = None
        self.__lives_text = None

        self.__soundtrack = "421_Disco_Bach_Loop.mp3"

        # ====================  A Min Score for Dynamic Difficulty Increase ============================================

        self.__check_score_min_bound = 2
        self.__check_score_multiplier = 1.5

        pygame.init()

        self.__font = pygame.font.SysFont(self.__font_style, self.__font_size)

        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        pygame.display.set_caption(self.__screen_title)

        self.__player = Player(self.__screen_width // 2, self.__screen_height // 2,
                               self.__screen_width, self.__screen_height)

        self.__asshole_spawner = EnemySpawn(self.__player, self.__screen_width, self.__screen_height,
                                            self.__font_screen_offset)

        pygame.mixer.music.load(self.__soundtrack)
        pygame.mixer.music.play(-1)

    def run(self):

        while self.__game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__game_running = False

            self.input_and_logic()
            self.draw()
            self.update_score(self.__score_frame_increment)
            self.check_score_and_increase_difficulty()
            pygame.time.delay(math.trunc(self.__time_per_frame_in_milli_seconds))

        pygame.quit()
        quit()

    def input_and_logic(self):

        self.__player.input()
        if self.__player.move(self.__time_per_frame_in_seconds) == Player.ERR_CODE_DEATH:
            print("Score: " + self.get_score())
            self.__game_running = False

        self.__asshole_spawner.move(self.__time_per_frame_in_seconds)

    def draw(self):

        self.draw_background()
        self.draw_entities()
        self.draw_text()

        pygame.display.flip()

    def draw_background(self):
        self.__screen.fill(pygame.Color("white"))

    def draw_entities(self):
        self.__asshole_spawner.draw(self.__screen)
        self.__player.draw(self.__screen)

    def draw_text(self):
        self.__score_text = self.__font.render("Score: " + self.get_score(), True, (0, 0, 0))
        self.__lives_text = self.__font.render("Lives: " + str(self.__player.get_lives()), True, (0, 0, 0))

        self.__screen.blit(self.__score_text,
                           (self.__screen_width // 2 - self.__score_text.get_rect().width // 2,
                            self.__screen_height - self.__font_size))
        self.__screen.blit(self.__lives_text, (self.__font_screen_offset, self.__screen_height - self.__font_size))

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
            self.__check_score_min_bound *= self.__check_score_multiplier
