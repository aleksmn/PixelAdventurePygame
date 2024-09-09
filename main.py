import os
import random
import math
import pygame as pg
from os import listdir
from os.path import isfile, join

pg.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60
PLAYER_VELOCITY = 5
GRAVITY = 0

def flip(sprites):
    return [pg.transform.flip(image, True, False) for image in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pg.image.load(join(path, image)).convert_alpha()

        sprites = []
        
        for i in range(sprite_sheet.get_width() // width):
            surface = pg.Surface((width, height), pg.SRCALPHA, 32)
            rect = pg.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pg.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)

        else:
            all_sprites[image.replace(".png", "")] = sprites
    
    return all_sprites




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

        self.all_sprites = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)


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
        # pg.draw.rect(screen, "red", self.rect)
        self.sprite = self.all_sprites["idle_" + self.direction][0]
        screen.blit(self.sprite, (self.rect.x, self.rect.y))





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