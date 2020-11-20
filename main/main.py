import pygame as pg
from random import randint


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60
WIDHT = 800
HEIGHT = 600
SCREEN = pg.display.set_mode((WIDHT, HEIGHT))


def getRandColor():
    return (randint(0, 255), randint(0, 255), randint(0, 255))



class GameObject:
    x, y = 0, 0


class Player(GameObject):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 25
        self.height = 25
        self.speed = 5

    def move(self, direction):
        if direction == "right" and self.x < WIDHT - self.width:
            self.x += self.speed
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "up" and self.y > 0:
            self.y -= self.speed
        if direction == "down" and self.y < HEIGHT - self.height:
            self.y += self.speed

    def draw(self, screen):
        pg.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

class Box(GameObject):
    def __init__(self, coord=None, color=None, rad=None):
        self.coord = coord
        self.rad = rad
        self.color = color

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)



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
        self.countOfTargets = 5
        self.targets = []

    def createTargets(self):
        for i in range(self.countOfTargets):
            self.targets.append(Box((randint(250, 400), randint(200, 350)), getRandColor(), 10))

    def showTargets(self, screen):
        for i in self.targets:
            i.draw(screen)



class GameWindow:
    def __init__(self):
        pg.init()
        self.width = 800
        self.height = 600
        self.title = "Sokoban"
        SCREEN.fill(WHITE)
        pg.display.set_caption(self.title)
        self.player = Player()
        self.map = Map()
        self.boxes = Box()
        self.manager = Manager()
        self.manager.createTargets()



    def mainLoop(self):

        finished = False
        clock = pg.time.Clock()

        while not finished:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True

            keys = pg.key.get_pressed()
            if keys[pg.K_RIGHT]:
                self.player.move("right")
            if keys[pg.K_LEFT]:
                self.player.move("left")
            if keys[pg.K_UP]:
                self.player.move("up")
            if keys[pg.K_DOWN]:
                self.player.move("down")


            SCREEN.fill(WHITE)

            self.player.draw(SCREEN)
            #self.map.draw(screen)
            #self.boxes.draw(screen)
            self.manager.showTargets(SCREEN)



            pg.display.flip()
            pg.display.update()
            clock.tick(FPS)




def main():

    window = GameWindow()
    window.mainLoop()

    print('Game over!')




if __name__ == "__main__":
    main()


