#Libraries
import numpy as np

class Animal(object):

    def __init__(self, speed=5.0):
        self.pos = [random.uniform(0.0, 2*np.pi), random.uniform(0.0, 2*np.pi)] 
        # ^ rho and theta, respectively
        self.speed = speed