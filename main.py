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



class Game:

    def __init__(self):        
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Pixel Adventure")
        
        self.clock = pg.time.Clock()
        

        self.run()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()


    def update(self):
        pass


    def draw(self):
        pass


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