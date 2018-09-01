import pygame
import math
from spawner import AssholeSpawner
from player import Player


def render():

    # ====================  All the Rendering Process  =============================================================

    global g_screen_dimensions, g_screen, g_asshole_spawner, g_font, g_font_size, g_score, g_score_text

    g_screen.fill(pygame.Color("black"))

    g_score_text = g_font.render("Score: " + get_score(), True, (255, 255, 255))
    g_lives_text = g_font.render("Lives: " + str(g_player.get_lives()), True, (255, 255, 255))

    g_screen.blit(g_score_text,
                  (g_screen_dimensions[0]//2 - g_score_text.get_rect().width//2, g_screen_dimensions[1] - g_font_size))

    g_screen.blit(g_lives_text, (g_font_screen_offset, g_screen_dimensions[1] - g_font_size))

    g_asshole_spawner.draw(g_screen)
    g_player.draw(g_screen)

    pygame.display.flip()


def logic():

    # ====================  Input Included in Player.move()  =======================================================

    global g_player, g_asshole_spawner, g_game_running

    g_player.input()
    if g_player.move(g_time_per_frame_in_seconds) == Player.ERR_CODE_DEATH:
        print("Score: " + get_score())
        g_game_running = False

    g_asshole_spawner.move(g_time_per_frame_in_seconds)


def init():

    # ====================  Global Initialization  =================================================================

    global g_player, g_screen, g_asshole_spawner, g_font

    pygame.init()

    g_font = pygame.font.SysFont(g_font_style, g_font_size)

    g_screen = pygame.display.set_mode(g_screen_dimensions)
    pygame.display.set_caption(g_screen_title)

    g_player = Player(g_screen_dimensions[0] // 2, g_screen_dimensions[1] // 2,
                      g_screen_dimensions[0], g_screen_dimensions[1])

    g_asshole_spawner = AssholeSpawner(g_player, g_screen_dimensions[0], g_screen_dimensions[1], g_font_screen_offset)


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

