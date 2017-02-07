"""
This script contains a lot of stuff that will be useful for debugging.

"""

# Libraries
import numpy as np
import random
# Custom modules
import sheepClass as sc
import pygame

class Player(sc.Sheep):

    def __init__(self, **kwargs):
        sc.Sheep.__init__(self)
        speed = 0.01
        color = (255, 0, 0)
        if "speed" in kwargs: 
            self.speed = kwargs["speed"]
        if "color" in kwargs: 
            self.color = kwargs["color"]
        if "pos" in kwargs:
            self.pos = kwargs["pos"]
        self.pos = np.array([random.random() for _ in range(2)])
        self.arrowsToDirs = {pygame.K_DOWN:[0,1], 
                    pygame.K_UP:[0,-1], 
                    pygame.K_LEFT:[-1,0], 
                    pygame.K_RIGHT:[1,0]}

    def planMove(self, sheepSet, wolf):
        self.plannedDir = np.array([0.0, 0.0])
        keysPressed = pygame.key.get_pressed()
        for arrow in self.arrowsToDirs.keys():
            if keysPressed[arrow]:
                self.plannedDir += self.arrowsToDirs[arrow]
        mag = np.linalg.norm(self.plannedDir)
        if mag > 0.0:
            self.plannedDir /= mag
         

