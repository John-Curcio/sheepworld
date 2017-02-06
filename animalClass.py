#Libraries
import random
import numpy as np
import pygame

class Animal(object):

    def __init__(self, speed=5.0, color=(0, 0, 0)):
        self.pos = np.array([random.uniform(0.0, 2*np.pi), random.uniform(0.0, 2*np.pi)])
        self.r = 10
        # ^ rho and theta, respectively
        self.speed = speed
        self.Surface = pygame.Surface((2 * self.r, 2 * self.r))
        self.Surface.convert_alpha()
        self.Surface.set_colorkey((0, 0, 0)) #black is transparent.
        self.color = color

    def draw(self, screen, size):
        mappedPos = (min(size)/(2*np.pi) ) * self.pos
        screen.blit(self.Surface, (round(mappedPos[0] - self.r), round(mappedPos[1] - self.r)))
        pygame.draw.circle(screen, self.color, (int(round(mappedPos[0])), int(round(mappedPos[1]))), self.r)