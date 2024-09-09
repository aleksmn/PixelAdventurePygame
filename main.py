import os
import random
import math
import pygame as pg
from os import listdir
from os.path import isfile

pg.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60
PLAYER_VELOCITY = 5
GRAVITY = 1

def get_background(name):
    image = pg.image.load("assets/Background/" + name)
    x, y, width, height = image.get_rect()

    tiles = []

    for i in range(SCREEN_WIDTH // width + 1):
        for j in range(SCREEN_HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image



class Player(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
        
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def handle_move(self):

        self.x_vel = 0
        
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.move_left(PLAYER_VELOCITY)

        if keys[pg.K_RIGHT]:
            self.move_right(PLAYER_VELOCITY)


    def update(self):
        self.handle_move()
        self.move(self.x_vel, self.y_vel)

        self.y_vel += GRAVITY + (self.fall_count / FPS * GRAVITY)
        self.fall_count += 1




    def draw(self, screen):
        pg.draw.rect(screen, "red", self.rect)





class Game:

    def __init__(self):        
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Pixel Adventure")        
        self.clock = pg.time.Clock()

        self.background, self.bg_image = get_background("Green.png")

        self.player = Player(100, 100, 50, 50)

        self.run()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()


    def update(self):
        self.player.update()


    def draw(self):
        for tile in self.background:
            self.screen.blit(self.bg_image, tile)

        self.player.draw(self.screen)


    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            pg.display.flip()


# Точка входа в программу
if __name__ == "__main__":
    # Запускаем игру
    Game()