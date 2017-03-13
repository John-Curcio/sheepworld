#Libraries
import random
import numpy as np
import pygame

class Animal(object):

    def __init__(self, **kwargs):
        speed = 0
        color = (0, 0, 0)
        if "speed" in kwargs: speed = kwargs["speed"]
        if "color" in kwargs: color = kwargs["color"]
        self.speed = speed
        self.color = color
        self.pos = None
        self.randomizePos()
        self.plannedDir = np.array([0.0, 0.0])
        self.r = 10
        # ^ rho and theta, respectively
        self.Surface = pygame.Surface((2 * self.r, 2 * self.r))
        self.Surface.convert_alpha()
        self.Surface.set_colorkey((0, 0, 0)) #black is transparent.

    def move(self):
        self.pos = (self.pos + self.speed * self.plannedDir) % 1

    def randomizePos(self):
        self.pos = np.array([random.random(), random.random()])
    #B is another animal
    def getShortestDistVec(self, B):
        vecWithMinMag = None
        minMag = None
        for x in {0.0, 1.0, -1.0}:
            for y in {0.0, 1.0, -1.0}:
                vec = B.pos - self.pos + np.array([x, y])
                mag = np.linalg.norm(vec)
                if minMag == None or mag < minMag:
                    minMag = mag
                    vecWithMinMag = vec
        return vecWithMinMag

    def draw(self, screen, size):
        mappedPos = np.array((size[0]*self.pos[0], size[1]*self.pos[1]))
        screen.blit(self.Surface, (round(mappedPos[0] - self.r), round(mappedPos[1] - self.r)))
        pygame.draw.circle(screen, self.color, (int(round(mappedPos[0])), int(round(mappedPos[1]))), self.r)
        # V probably great for debugging. Shows the step that this animal just took.
        pygame.draw.line(screen, self.color, mappedPos, mappedPos - 2*self.r*self.plannedDir, 2)


def valWithMinAbs(*args):
    val = None
    for x in args:
        if val == None or abs(x) < abs(val):
            val = x
    return val