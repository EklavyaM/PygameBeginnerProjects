import pygame
import math
from random import randint
from threading import Thread
from time import sleep


class AssholeSpawner:

    def __init__(self, l_player):
        self.assholes = []
        self.thread_spawner = Thread(target=self.__spawn)
        self.temp_pos_x = 0
        self.temp_vel = 0
        self.temp_size = 0

        self.player = l_player

        self.thread_spawner.start()

    def __spawn(self):
        while game_running:
            self.temp_pos_x = randint(0, screen_dimensions[0])
            self.temp_vel = randint(1, 5)
            self.temp_size_x = self.temp_size_y = randint(8, 20)
            self.assholes.append(AssholeSpawner.Asshole(self.temp_pos_x, -self.temp_size_y, self.temp_vel,
                                                        self.temp_size_x, self.temp_size_y))
            sleep(1)

    def move(self):
        for asshole in self.assholes:
            asshole.move()
            asshole.check_player_collision(self.player)
            if asshole.pos_y > screen_dimensions[1]:
                self.assholes.remove(asshole)

    def draw(self, scr):
        for asshole in self.assholes:
            asshole.draw(scr)

    class Asshole:

        def __init__(self, l_pos_x, l_pos_y, l_vel, l_size_x, l_size_y):
            self.pos_x = l_pos_x
            self.pos_y = l_pos_y
            self.velocity = l_vel
            self.size_x = l_size_x
            self.size_y = l_size_y
            self.color = pygame.Color("red")
            self.hit_box = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)

        def move(self):
            self.pos_y = self.hit_box.top = self.pos_y + self.velocity

        def draw(self, scr):
            pygame.draw.rect(scr, self.color, self.hit_box)

        def check_player_collision(self, l_player):
            if self.hit_box.colliderect(l_player.hit_box):
                print("collided")


class Player:

    SIZE_X = 16
    SIZE_Y = 16
    ACC = 5
    MAX_VELOCITY = 7
    MIN_VELOCITY = 0.5
    FRICTION = 0.3

    def __init__(self, l_pos_x, l_pos_y):

        self.pos_x = l_pos_x
        self.pos_y = l_pos_y
        self.vel_x = 0
        self.vel_y = 0
        self.hit_box = pygame.Rect(self.pos_x, self.pos_y, Player.SIZE_X, Player.SIZE_Y)
        self.color = pygame.Color("white")

    def move(self):

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

        # max velocity check
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

        # apply friction
        if math.fabs(self.vel_x) > Player.MIN_VELOCITY or math.fabs(self.vel_y) > Player.MIN_VELOCITY:
            self.vel_x += -self.vel_x * Player.FRICTION
            self.vel_y += -self.vel_y * Player.FRICTION
        else:
            self.vel_x, self.vel_y = 0, 0

        l_temp_pos_x = self.pos_x + self.vel_x
        l_temp_pos_y = self.pos_y + self.vel_y

        if l_temp_pos_x > screen_dimensions[0] - Player.SIZE_X:
            l_temp_pos_x = screen_dimensions[0] - Player.SIZE_X
        elif l_temp_pos_x < 0:
            l_temp_pos_x = 0

        if l_temp_pos_y > screen_dimensions[1] - Player.SIZE_Y:
            l_temp_pos_y = screen_dimensions[1] - Player.SIZE_Y
        elif l_temp_pos_y < 0:
            l_temp_pos_y = 0

        self.pos_x = self.hit_box.left = l_temp_pos_x
        self.pos_y = self.hit_box.top = l_temp_pos_y

    def draw(self, scr):
        pygame.draw.rect(scr, self.color, self.hit_box)


def main():

    global game_running, player

    pygame.init()

    screen = pygame.display.set_mode(screen_dimensions)
    pygame.display.set_caption(screen_title)

    player = Player(screen_dimensions[0]//2, screen_dimensions[1]//2)
    asshole_spawner = AssholeSpawner(player)

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        # input and logic

        player.move()
        asshole_spawner.move()

        # rendering

        screen.fill(pygame.Color("black"))

        asshole_spawner.draw(screen)
        player.draw(screen)

        pygame.display.flip()

        # tick
        pygame.time.delay(17)

    pygame.quit()
    quit()


if __name__ == "__main__":

    screen_dimensions = (800, 600)
    screen_title = "Dodger"
    game_running = True
    player = None

    main()

