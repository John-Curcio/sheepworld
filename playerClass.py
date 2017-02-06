"""
This script contains a lot of stuff that will be useful for debugging.

"""

# Libraries
import numpy as np
import random
# Custom modules
import animalClass as ac
import pygame

class Player(ac.Animal):

    def __init__(self, pos=None):
        ac.Animal.__init__(self, speed=0.05, color=(255, 255, 20))
        if pos == None:
            pos = np.array([random.random() for _ in range(2)])
        self.pos = pos
        self.arrowsToDirs = {pygame.K_DOWN:[0,1], 
                    pygame.K_UP:[0,-1], 
                    pygame.K_LEFT:[-1,0], 
                    pygame.K_RIGHT:[1,0]}

    def move(self):
        dirVec = np.array([0.0, 0.0])
        keysPressed = pygame.key.get_pressed()
        for arrow in self.arrowsToDirs.keys():
            if keysPressed[arrow]:
                dirVec += self.arrowsToDirs[arrow]
        mag = np.linalg.norm(dirVec)
        if mag > 0.0:
            dirVec /= mag
        for i in range(len(dirVec)):
            self.pos[i] += self.speed * dirVec[i]
        self.pos %= (2*np.pi)

