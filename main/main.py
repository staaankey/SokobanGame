import os
import pygame as pg
import levels
from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (211, 211, 211)
BROWN = (210, 105, 30)
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


class GameObject:
    """

    """

    def __init__(self, img):
        """

        :param img: image of object
        """
        super.__init__()
        self.image = pg.image.load(img)
        self.x = 0
        self.y = 0
        self.speed = 0


class Player(GameObject):
    """
    The function that is responsible for initializing the player and issuing basic parameters to his properties.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pg.image.load(os.path.abspath("../res/sokoban.png"))
        self.width = 20
        self.height = 20
        self.speed = 20

    def move(self, direction):
        """
        A function that is responsible for moving the player around the playing field in a certain direction.
        :param direction: direction of moving
        :return:None
        """
        if direction == "right" and self.x < WIDTH - self.width:  # TODO: Fix me
            self.x += self.speed
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "up" and self.y > 0 + self.height:
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

        :param x: coordinate x
        :param y: coordinate y
        """
        self.x = x
        self.y = y
        self.image = pg.image.load(os.path.abspath("../res/box.png"))
        self.width = 20
        self.height = 20
        self.speed = 20
        self.color = getRandColor()

    def draw(self):
        """
        A function that draws a new box on the playing field.
        """
        pg.draw.rect(SCREEN, RED, (self.x, self.y, self.width, self.height))

    def move(self, x, y):
        """
        A function that is responsible for displacing an object along the x and y axes.
        :param x: position
        :param y: position
        :return:
        """
        self.x += x
        self.y += y


class Wall(GameObject):
    def __init__(self, x, y):
        """
        A constructor that initializes the game board.
        :param x: wall's x coordinate
        :param y: wall's y coordinate
        """
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.image = pg.image.load(os.path.abspath("../res/wall.png"))


class Spot(GameObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.image = pg.image.load(os.path.abspath("../res/area.png"))
        self.rect = self.image.get_rect()
        self.isActive = True

    def draw(self):
        SCREEN.blit((self.image, [self.x, self.y]))

    def change_picture(self, spot, box):
        if spot.x == box.x and spot.y == box.y:
            spot.image = pg.image.load(os.path.abspath("../res/box.png"))
        else:
            spot.image = pg.image.load(os.path.abspath("../res/area.png"))


class Map:
    def __init__(self, x, y, i):
        """
        A constructor that initializes the game board.
        :param x: x coordinate of the map
        :param y: y coordinate of the map
        """
        self.x = x
        self.y = y
        self.walls = []
        self.boxes = []
        self.spots = []
        self.player = None
        self.level = levels.list_of_levels[i]

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

            elif char == "X":
                self.walls.append(Wall(self.x, self.y))
                self.x += 20

            elif char == "@":
                self.player = Player(self.x, self.y)
                self.x += 20

            elif char == " ":
                self.x += 20

            elif char == "*":
                self.boxes.append(Box(self.x, self.y))
                self.x += 20

            elif char == ".":
                self.spots.append(Spot(self.x, self.y))
                self.x += 20

            elif char == ",":
                self.x += 0
                self.y += 0

    def draw_map(self):
        """
        A function that draws walls, boxes, and spots on the screen.
        """
        for wall in self.walls:
            SCREEN.blit(wall.image, (wall.x, wall.y))

        for box in self.boxes:
            SCREEN.blit(box.image, (box.x, box.y))

        for spot in self.spots:
            SCREEN.blit(spot.image, (spot.x, spot.y))


class Manager:
    """
    The Manager class that manages all the events and classes on the playing field.
    It also handles collisions of objects and is an event handler.
    Stores the main objects on the map.
    """

    def __init__(self):
        self.index = 0
        self.map = Map(0, 0, self.index)
        self.map.create_level()
        self.player = self.map.player
        self.walls = self.map.walls
        self.spots = self.map.spots
        self.boxes = self.map.boxes

    def init_map(self):  # TODO: Fix me
        """
        Initialization of map.
        :return: None
        """
        self.index += 1
        self.map = Map(0, 0, self.index)
        self.map.create_level()
        self.player = self.map.player
        self.walls = self.map.walls
        self.spots = self.map.spots
        self.boxes = self.map.boxes

    def handler_events(self, event):
        """
        Simple event handler. Fires during certain actions on the map.
        :param event: events
        :return: bool
        """
        if event.type == pg.QUIT:
            return True
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.collision_catcher(self.player, self.boxes, "right")
            self.collision_with_walls(self.walls, self.player, "right", self.boxes)
            self.counter(self.boxes, self.spots)

            self.player.move("right")
        if keys[pg.K_LEFT]:
            self.collision_catcher(self.player, self.boxes, "left")
            self.collision_with_walls(self.walls, self.player, "left", self.boxes)
            self.counter(self.boxes, self.spots)

            self.player.move("left")
        if keys[pg.K_UP]:
            self.collision_catcher(self.player, self.boxes, "up")
            self.collision_with_walls(self.walls, self.player, "up", self.boxes)
            self.counter(self.boxes, self.spots)

            self.player.move("up")
        if keys[pg.K_DOWN]:
            self.collision_catcher(self.player, self.boxes, "down")
            self.collision_with_walls(self.walls, self.player, "down", self.boxes)
            self.counter(self.boxes, self.spots)

            self.player.move("down")

    def collision_with_walls(self, walls, player, direction, boxes):
        """
        A function that controls the collision of the player, blocks and walls.
        :param boxes: list of boxes
        :param direction: direction of moving
        :param walls: list of walls
        :param player: oject of player
        :return: None
        """
        for box in boxes:
            for wall in walls:
                if wall.x - wall.width == player.x and player.y == wall.y and direction == "right": #moving box right
                    self.player.move("left")

                elif wall.x == box.x and box.y == wall.y and direction == "right":
                    self.player.move("left")
                    box.move(-player.speed, 0)

                elif wall.x + wall.width == player.x and player.y == wall.y and direction == "left":
                    self.player.move("right")

                elif wall.x == box.x and box.y == wall.y and direction == "left":
                    self.player.move("right")
                    box.move(player.speed, 0)

                elif player.x == wall.x and wall.y + wall.height == player.y and wall.y > 0 and direction == "up":
                    self.player.move("down")

                elif box.x == wall.x and wall.y == box.y and direction == "up":
                    self.player.move("down")
                    box.move(0, +player.speed)

                elif wall.x == player.x and wall.y - wall.height == player.y and direction == "down":
                    self.player.move("up")

                elif wall.x == box.x and wall.y == box.y and direction == "down":
                    self.player.move("up")
                    box.move(0, -player.speed)

    def collision_catcher(self, player, boxes, direction):
        """
        A function that controls the collision of the player's object and boxes on the playing field.
        :param direction: direction of moving
        :param player: object of main player
        :param boxes: list of boxes
        :return: None
        """

        for box in boxes:
            if box.x - box.width == player.x and player.y == box.y and direction == "right":
                box.move(+player.speed, 0)
            elif box.x + box.width == player.x and player.y == box.y and direction == "left":
                box.move(-player.speed, 0)
            elif player.x == box.x and box.y + box.height == player.y and direction == "up":
                box.move(0, -player.speed)
            elif box.x == player.x and box.y - box.height == player.y and direction == "down":
                box.move(0, +player.speed)

        for i in range(len(self.boxes)):
            for j in range(i + 1, len(self.boxes)):
                if self.boxes[i].x == self.boxes[j].x and self.boxes[i].y == self.boxes[j].y and direction == "left":
                    self.boxes[j].move(+self.player.speed, 0)
                    self.player.move("right")
                elif self.boxes[i].x == self.boxes[j].x and self.boxes[i].y == self.boxes[j].y and direction == "right":
                    self.boxes[j].move(-self.player.speed, 0)
                    self.player.move("left")
                elif self.boxes[i].x == self.boxes[j].x and self.boxes[i].y == self.boxes[j].y and direction == "up":
                    self.boxes[j].move(0, +self.player.speed)
                    self.player.move("down")
                elif self.boxes[i].x == self.boxes[j].x and self.boxes[i].y == self.boxes[j].y and direction == "down":
                    self.boxes[j].move(0, -self.player.speed)
                    self.player.move("up")

    def counter(self, boxes, spots):
        """
        The counter counts the boxes in their places.
        :param boxes: list of boxes.
        :param spots: list of spots.
        :return: None
        """
        count = 0
        for spot in spots:
            for box in boxes:
                if spot.x == box.x and spot.y == box.y:
                    count += 1
                    spot.image = box.image
                    if count == len(spots):
                        self.init_map()
                    break
                else:
                    spot.image = pg.image.load(os.path.abspath("../res/area.png"))


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
        self.manager = Manager()
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
            SCREEN.blit(self.manager.player.image, (self.manager.map.player.x, self.manager.map.player.y))
            pg.display.flip()
            pg.display.update()
            clock.tick(FPS)


def main():
    window = GameWindow()
    window.mainLoop()

    print('Game over!')


if __name__ == "__main__":
    main()
