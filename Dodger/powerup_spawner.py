class PowerupSpawner:

    SPAWN_TIME = 3
    INITIAL_WAIT = 3

    SIZE_X = 16
    SIZE_Y = 16

    POS_Y = -SIZE_Y

    VELOCITY = 3

    def __init__(self, l_player, l_screen_width, l_screen_height, l_bottom_offset):

        self.__power_ups = []
        self.__screen_width = l_screen_width
        self.__screen_height = l_screen_height
        self.__bottom_offset = l_bottom_offset

        self.__player = l_player
