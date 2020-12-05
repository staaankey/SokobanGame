import os
import pygame as pg
from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (211, 211, 211)
YELLOW = (250, 240, 170)
FPS = 120
WIDTH = 800
HEIGHT = 600
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))


def getRandColor():
    """
    A function that returns a random number of a random color in RGB.
    """
    return randint(0, 255), randint(0, 255), randint(0, 255)


class GameObject(pg.sprite.Sprite):
    """

    """

    def __init__(self, img):
        """
        :param img:
        """
        super().__init__(self)
        self.image = pg.image.load(img)
        self.x = 0
        self.y = 0
        self.speed = 0


class Player(GameObject):
    """
    The function that is responsible for initializing the player and issuing basic parameters to his properties.
    """

    def __init__(self, x, y):
        self.sprite = pg.sprite.Sprite()
        self.x = x
        self.y = y
        self.image = pg.Surface((75, 75))
        self.rect = self.image.get_rect()
        self.width = 10
        self.height = 10
        self.speed = 10

    def move(self, direction):
        """
        A function that is responsible for moving the player around the playing field in a certain direction.
        :param direction:
        :return:
        """
        if direction == "right" and self.x < WIDTH - self.width:  # TODO: Fix me
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
        pg.draw.rect(SCREEN, RED, (self.x, self.y, self.width, self.height))


class Box(GameObject):
    """
    Constructor for the Box class that initializes a new box on the map.
    """

    def __init__(self, x, y):
        """

        :param x:
        :param y:
        """
        self.x = x
        self.y = y
        #self.image = pg.image.load(os.path.abspath("../res/box.png"))
        #self.rect = self.image.get_rect()
        self.width = 10
        self.height = 10
        self.speed = 10
        self.color = getRandColor()

    def draw(self):
        """
        A function that draws a new box on the playing field.
        """
        pg.draw.rect(SCREEN, RED, (self.x, self.y, self.width, self.height))

    def move(self, x, y):
        """
        A function that is responsible for displacing an object along the x and y axes.
        :param x:
        :param y:
        :return:
        """
        self.x += x
        self.y += y


class Wall(GameObject):
    def __init__(self, x, y):
        """
        A constructor that initializes the game board.
        :param x:
        :param y:
        """
        self.x = x
        self.y = y
        self.width = 100
        self.image = pg.image.load(os.path.abspath("../res/wall.png"))
        self.rect = self.image.get_rect()

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)


class Spot(GameObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pg.image.load(os.path.abspath("../res/baggage.png"))
        self.rect = self.image.get_rect()

    def draw(self):
        SCREEN.blit((self.image, [self.x, self.y]))


class Map(Wall):
    def __init__(self, x, y):
        """
        A constructor that initializes the game board.
        :param x:
        :param y:
        """
        self.x = x
        self.y = y
        self.walls = []
        self.boxes = []
        self.spots = []
        self.player = None
        self.level = ("""
                            # # # # # # # # #\n
                            #               #\n
                            #   #     #     #\n
                            #       $       #\n
                            #      @        #\n
                            #               #\n
                            #             o #\n
                            #             o #\n
                            # # # # # # # # #\n
                    """)

    def draw_background(self):
        """
        A function that draws the graces of the level and objects inside it
        """
        pg.draw.rect(SCREEN, YELLOW, (0, 0, 800, 600))

    def create_level(self):
        """
        A function that draws the boundaries of the game level.
        """
        for char in self.level:
            if char == "\n":
                self.y += 10
                self.x = 0

            elif char == "#":
                self.walls.append(Wall(self.x, self.y))
                self.x += 10

            elif char == "@":
                self.player = Player(self.x, self.y)
                self.x += 10

            elif char == " ":
                self.x += 10

            elif char == "$":
                self.boxes.append(Box(self.x, self.y))
                self.x += 10

            elif char == "o":
                self.spots.append(Spot(self.x, self.y))
                self.x += 10

    def draw_map(self):
        """
        A function that draws walls on the screen.
        """
        for wall in self.walls:
            SCREEN.blit(wall.image, (wall.x, wall.y))

        for box in self.boxes:
            pg.draw.rect(SCREEN, GREY, (box.x, box.y, box.width, box.height))

        for spot in self.spots:
            SCREEN.blit(spot.image, (spot.x, spot.y))


class Manager:
    """
    The Manager class that manages all the events and classes on the playing field.
    It also handles collisions of objects and is an event handler.
    Stores the main objects on the map.
    """

    def __init__(self, main_map, walls, spots, boxes):
        self.map = main_map
        self.map.create_level()
        self.player = self.map.player
        self.walls = walls
        self.spots = spots
        self.boxes = boxes

    def handler_events(self, event):
        """
        Simple event handler. Fires during certain actions on the map.
        :param event:
        :return:
        """
        if event.type == pg.QUIT:
            return True
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] and Manager.collision_with_walls(self.walls, self.player, "right"):
            self.player.move("right")
        if keys[pg.K_LEFT] and Manager.collision_with_walls(self.walls, self.player, "left"):
            self.player.move("left")
        if keys[pg.K_UP] and Manager.collision_with_walls(self.walls, self.player, "up"):
            self.player.move("up")
        if keys[pg.K_DOWN] and Manager.collision_with_walls(self.walls, self.player, "down"):
            self.player.move("down")

    @staticmethod
    def collision_with_walls(walls, player, key):
        """
        A function that controls the collision of the player, blocks and walls.
        :param walls:
        :param player:
        :param key:
        :return:
        """
        return True


    @staticmethod
    def collision_catcher(player, targets):
        """
        A function that controls the collision of the player's object and boxes on the playing field.
        :param player:
        :param targets:
        :return:
        """
        for target in targets:
            if target.x + target.width == player.x + player.width and player.y == target.y and target.x < WIDTH - target.width:
                target.move(+player.speed, 0)
            elif target.x + target.width == player.x + player.width and player.y == target.y and target.x > 0:
                target.move(-player.speed, 0)
            elif player.x == target.x and target.y + target.height == player.y and target.y > 0:
                target.move(0, -player.speed)
            elif target.x == player.x and target.y - target.height == player.y and target.y < HEIGHT - target.height:
                target.move(0, +player.speed)

    @staticmethod
    def collision_with_spots(boxes, spots):
        count = 0
        for box in boxes:
            for spot in spots:
                if box.x == spot.x and box.y == spot.y:
                    count += 1
                    if count == len(spots):
                        exit()
                    else:
                        continue


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
        self.title = "Sokoban"
        self.map = Map(0, 0)
        self.manager = Manager(self.map, self.map.walls, self.map.spots, self.map.boxes)
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
            self.manager.map.draw_map()
            self.manager.player.draw()
            self.manager.collision_catcher(self.manager.player, self.map.boxes)
            self.manager.collision_with_spots(self.map.boxes, self.manager.spots)
            pg.display.flip()
            pg.display.update()
            clock.tick(FPS)


def main():
    window = GameWindow()
    window.mainLoop()

    print('Game over!')


if __name__ == "__main__":
    main()
