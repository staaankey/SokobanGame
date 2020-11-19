import pygame as pg
import os


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60
SPEED = [2, 2]




class GameObject:
    x, y = 0, 0
    pass


class Player(GameObject):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 25
        self.height = 25
    pass


class Box(GameObject):
    pass


class Wall(GameObject):
    pass


class GameField:
    pass

class GameWindow:
    def __init__(self):
        pg.init()
        self.width = 800
        self.height = 600
        self.title = "Sokoban"
        self.screen = pg.display.set_mode((self.width, self.height))
        self.screen.fill(WHITE)
        pg.display.set_caption(self.title)
        self.mainPlayer = Player()

    def mainLoop(self):
        finished = False
        clock = pg.time.Clock()

        while not finished:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True

            keys = pg.key.get_pressed()
            if keys[pg.K_RIGHT] and (self.mainPlayer.x < self.width - self.mainPlayer.width):
                self.mainPlayer.x += 10
            if keys[pg.K_LEFT] and (self.mainPlayer.x > 0):
                self.mainPlayer.x -= 10
            if keys[pg.K_UP] and (self.mainPlayer.y > 0):
                self.mainPlayer.y -= 10
            if keys[pg.K_DOWN] and (self.mainPlayer.y < self.height - self.mainPlayer.height):
                self.mainPlayer.y += 10


            self.screen.fill(WHITE)
            pg.draw.rect(self.screen, RED, (self.mainPlayer.x, self.mainPlayer.y, self.mainPlayer.width, self.mainPlayer.height))
            pg.display.flip()
            pg.display.update()
            clock.tick(FPS)




def main():
    window = GameWindow()
    window.mainLoop()
    print('Game over!')




if __name__ == "__main__":
    main()


