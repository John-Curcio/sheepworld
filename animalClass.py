#Libraries
import numpy as np

class Animal(object):

    def __init__(self, speed=5.0):
        self.coords = [0.0, 0.0] #rho and theta, respectively
        self.speed = speed