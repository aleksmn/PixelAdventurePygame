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
GRAVITY = 1

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


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pg.image.load(path).convert_alpha()
    surface = pg.Surface((size, size), pg.SRCALPHA, 32)
    rect = pg.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pg.transform.scale2x(surface)



class Player(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.animation_delay = 3

        self.all_sprites = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)


    def jump(self):
        self.y_vel = -GRAVITY * 20
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
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

    def handle_move(self, objects):

        self.x_vel = 0
        
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.move_left(PLAYER_VELOCITY)

        if keys[pg.K_RIGHT]:
            self.move_right(PLAYER_VELOCITY)

        self.handle_vertical_collision(objects)


    def handle_animation(self):

        sprite_sheet = "idle"

        if self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"

        elif self.y_vel > GRAVITY * 3:
            sprite_sheet = "fall"

        if self.x_vel != 0:
            sprite_sheet = "run"

        # print(sprite_sheet)

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.all_sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.animation_delay) % len(sprites)        
        self.sprite = sprites[sprite_index]
        self.animation_count += 1


    def handle_vertical_collision(self, objects):
        collided_objects = []
        for obj in objects:
            if pg.sprite.collide_mask(self, obj):
                if self.y_vel > 0:
                    self.rect.bottom = obj.rect.top
                    self.landed()
                elif self.y_vel < 0:
                    self.rect.top = obj.rect.bottom
                    self.hit_head()

                collided_objects.append(obj)
   
        return collided_objects


    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0


    def hit_head(self):
        self.count = 0
        self.y_vel *= -1


    def update(self, objects):

        self.move(self.x_vel, self.y_vel)

        self.y_vel += GRAVITY + (self.fall_count / FPS * GRAVITY)
        self.fall_count += 1

        self.handle_animation()
        self.update_mask()
        self.handle_move(objects)
        

    def update_mask(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(self.sprite)

    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))


class Object(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name


    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))



class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pg.mask.from_surface(self.image)



class Game:

    def __init__(self):        
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Pixel Adventure")        
        self.clock = pg.time.Clock()

        self.background, self.bg_image = get_background("Green.png")

        self.player = Player(100, 100, 50, 50)

        block_size = 96

        # self.blocks = [Block(0, SCREEN_HEIGHT - block_size, block_size)]
        self.floor = [Block(i * block_size, SCREEN_HEIGHT - block_size, block_size) 
                      for i in range(-SCREEN_WIDTH // block_size, SCREEN_WIDTH * 2 // block_size)]

        self.run()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and self.player.jump_count < 2:
                    self.player.jump()


    def update(self):
        self.player.update(objects=self.floor)


    def draw(self):
        for tile in self.background:
            self.screen.blit(self.bg_image, tile)

        for obj in self.floor:
            obj.draw(self.screen)

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