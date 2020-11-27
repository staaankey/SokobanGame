import os
import pygame as pg
from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (211, 211, 211)
YELLOW = (250, 240, 170)
FPS = 60
WIDTH = 800
HEIGHT = 600
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))


def getRandColor():
    """
    A function that returns a random number of a random color in RGB.
    """
    return randint(0, 255), randint(0, 255), randint(0, 255)


class GameObject(pg.sprite.Sprite):
    def __init__(self, img):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(img)
        self.x = 0
        self.y = 0
        self.speed = 0


class Player(GameObject):
    """
    The function that is responsible for initializing the player and issuing basic parameters to his properties.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 15
        self.height = 15
        self.speed = 15
        self.image = pg.image.load("../res/sokoban.png")

    def move(self, direction):
        """
        A function that is responsible for moving the player around the playing field in a certain direction.
        """
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "up" and self.y > 0:
            self.y -= self.speed
        if direction == "down" and self.y < HEIGHT - self.height:
            self.y += self.speed

    def draw(self):
        """
        A function that is responsible for drawing the player's object on the playing field.
        """
        SCREEN.blit(self.image, (self.x, self.y))


class Box(GameObject):
    """
    Constructor for the Box class that initializes a new box on the map.
    """

    def __init__(self, width=None, height=None):
        self.x = randint(255, 255)
        self.y = randint(270, 270)
        self.image = pg.image.load(os.path.abspath("../res/box.png"))
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.speed = 15
        self.color = getRandColor()

    def draw(self):
        """
        A function that draws a new box on the playing field.
        """
        SCREEN.blit(self.image, [self.x, self.y])

    def move(self, x, y):
        """
        A function that is responsible for displacing an object along the x and y axes.
        """
        self.x += x
        self.y += y


class Wall:
    def __init__(self, x, y):
        """
        A constructor that initializes the game board.
        """
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15
        self.image = pg.image.load(os.path.abspath("../res/wall.png"))
        self.rect = self.image.get_rect()


class Map(Wall):
    def __init__(self, x, y):
        """
        A constructor that initializes the game board.
        """
        self.x = x
        self.y = y
        self.walls = []
        self.level = ('''
                        #########\n
                        #       #\n
                        #       #\n
                        #         #############\n
                         ####                 #\n
                            #####         ####\n
                                ############\n
                     ''')

    def draw_background(self):
        """
        A function that draws the graces of the level and objects inside it
        """
        pg.draw.rect(SCREEN, YELLOW, (0, 0, 800, 600))

    def create_level(self):
        """
        A function that draws the boundaries of the game level.
        """
        for i in self.level:
            if i == "\n":
                self.y += 12
                self.x = 0

            if i == "#":
                self.walls.append(Wall(self.x, self.y))
                self.x += 12

            if i == " ":
                self.x += 12

    def draw_walls(self):
        """
        A function that draws walls on the screen.
        """
        for wall in self.walls:
            SCREEN.blit(wall.image, (wall.x, wall.y))


class Manager:
    """
    The Manager class that manages all the events and classes on the playing field.
    It also handles collisions of objects and is an event handler.
    Stores the main objects on the map.
    """

    def __init__(self, main_map):
        self.countOfTargets = 1
        self.targets = []
        self.player = Player()
        self.map = main_map
        self.map.create_level()

    def create_targets(self):
        """
        A function that creates new objects for the playing field.
        """
        for i in range(self.countOfTargets):
            self.targets.append(Box(30, 30))

    def show_targets(self):
        """
        A function that represents boxes on the playing field.
        """
        for target in self.targets:
            target.draw()

    def handler_events(self, event):
        """
        Simple event handler. Fires during certain actions on the map.

        """
        if event.type == pg.QUIT:
            return True
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.player.move("right")
        if keys[pg.K_LEFT]:
            self.player.move("left")
        if keys[pg.K_UP]:
            self.player.move("up")
        if keys[pg.K_DOWN]:
            self.player.move("down")

    def collision_catcher(self, player):
        """
        A function that controls the collision of the player's object and boxes on the playing field.
        """
        for target in self.targets:
            print("p", player.x, player.y)
            print("b", target.x, target.y)
            if target.x - player.width == player.x and player.y == target.y and target.x < WIDTH - target.width:
                target.move(+player.speed, 0)
            elif target.x + player.width == player.x and player.y == target.y and target.x > 0:
                target.move(-player.speed, 0)
            elif player.x == target.x and target.y + player.height == player.y and target.y > 0:
                target.move(0, -player.speed)
            elif target.x == player.x and target.y - player.height == player.y and target.y < HEIGHT - target.height:
                target.move(0, +player.speed)

    def collision_with_walls(self, walls, player):
        pass


class GameWindow:
    """
    The game window class, defines all the properties and methods of the main game window.

    """

    def __init__(self):
        """
        The constructor that initializes the game window sets its basic properties, objects and fields.

        """
        pg.init()
        self.width = 800
        self.height = 600
        self.title = "SOKOBAN"
        self.boxes = Box()
        self.map = Map(0, 0)
        self.manager = Manager(self.map)
        self.manager.create_targets()
        SCREEN.fill(WHITE)
        pg.display.set_caption(self.title)

    def mainLoop(self):
        """
        The main loop of the game, which triggers all actions on the map.

        """
        finished = False
        clock = pg.time.Clock()

        while not finished:
            for event in pg.event.get():
                if self.manager.handler_events(event):
                    finished = True

            self.manager.map.draw_background()
            self.manager.map.draw_walls()
            self.manager.player.draw()
            self.manager.show_targets()
            self.manager.collision_catcher(self.manager.player)
            pg.display.flip()
            pg.display.update()
            clock.tick(FPS)


def main():
    window = GameWindow()
    window.mainLoop()

    print('Game over!')


if __name__ == "__main__":
    main()
