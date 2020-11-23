import pygame as pg
from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60
WIDTH = 800
HEIGHT = 600
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))


def getRandColor():
    """A function that returns a random number of a random color in RGB."""
    return randint(0, 255), randint(0, 255), randint(0, 255)


class GameObject:
    x, y = 0, 0


class Player(GameObject):
    """The function that is responsible for initializing the player and issuing basic parameters to his properties."""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 15
        self.height = 15
        self.speed = 15

    def move(self, direction):
        """A function that is responsible for moving the player around the playing field in a certain direction."""
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "up" and self.y > 0:
            self.y -= self.speed
        if direction == "down" and self.y < HEIGHT - self.height:
            self.y += self.speed

    def draw(self, screen):
        """A function that is responsible for drawing the player's object on the playing field."""
        pg.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))


class Box(GameObject):
    """Constructor for the Box class that initializes a new box on the map."""
    def __init__(self, width=None, height=None):
        self.x = randint(255, 255)
        self.y = randint(270, 270)
        self.width = width
        self.height = height
        self.speed = 15
        self.color = getRandColor()

    def draw(self, screen):
        """A function that draws a new box on the playing field."""
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, x, y):
        """A function that is responsible for displacing an object along the x and y axes."""
        self.x += x
        self.y += y


class Map(GameObject):
    def __init__(self):
        self.x = randint(300, 400)
        self.y = randint(300, 400)

    def draw(self, screen):
        pg.draw.line(screen, BLACK, (50, 500), (440, 500))
        pg.draw.line(screen, BLACK, (50, 50), (50, 500))
        pg.draw.line(screen, BLACK, (50, 50), (500, 50))
        pg.draw.line(screen, BLACK, (500, 50), (500, 500))


class Manager:
    def __init__(self):
        self.countOfTargets = 1
        self.targets = []
        self.player = Player()

    def createTargets(self):
        for i in range(self.countOfTargets):
            self.targets.append(Box(15, 15))

    def showTargets(self, screen):
        for target in self.targets:
            target.draw(screen)

    def collison(self, player):
        for target in self.targets:
            print("p", player.x, player.y)
            print("b", target.x, target.y)
            if target.x - player.width == player.x and player.y == target.y and target.x < WIDTH - target.width:
                target.move(+player.speed, 0)
            if target.x + player.width == player.x and player.y == target.y and target.x > 0:
                target.move(-player.speed, 0)
            if player.x == target.x and target.y + player.height == player.y and target.y > 0:
                target.move(0, -player.speed)
            if target.x == player.x and target.y - player.height == player.y and target.y < HEIGHT - target.height:
                target.move(0, +player.speed)

    def handleEvents(self, event):
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

        return False


class GameWindow:
    def __init__(self):
        pg.init()
        self.width = 800
        self.height = 600
        self.title = "Sokoban"
        SCREEN.fill(WHITE)
        pg.display.set_caption(self.title)
        self.boxes = Box()
        self.manager = Manager()
        self.map = Map()
        self.manager.createTargets()

    def mainLoop(self):
        finished = False
        clock = pg.time.Clock()

        while not finished:
            for event in pg.event.get():
                if self.manager.handleEvents(event):
                    finished = True

            SCREEN.fill(WHITE)
            self.manager.player.draw(SCREEN)
            self.manager.showTargets(SCREEN)
            self.map.draw(SCREEN)
            self.manager.collison(self.manager.player)
            pg.display.flip()
            pg.display.update()
            clock.tick(FPS)


def main():
    window = GameWindow()
    window.mainLoop()

    print('Game over!')


if __name__ == "__main__":
    main()
