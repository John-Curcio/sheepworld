# Libraries
import numpy as np
import random
# Custom modules
import animalClass as ac

class Wolf(ac.Animal):

    def __init__(self, **kwargs):
        ac.Animal.__init__(self)
        if "speed" in kwargs: self.speed = kwargs["speed"]
        if "color" in kwargs: self.color = kwargs["color"]
        
    """
    When a wolf hunts, it takes a step in the direction of the closest sheep. If
    it catches that sheep - that is, it comes within a certain distance - the 
    sheep dies, and the wolf's position is randomized again*.

    *The interpretation of this is that the wolf is satisfied, but another wolf
    appears randomly, and the new one's hungry. But the deletion of the old
    wolf, and the initialization of the new wolf, is just unnecessary, and is
    not the first thing you'd think from reading this code.
    """
    def hunt(self, sheepSet):
        minDistVec = None
        minDist = None
        closestSheep = None
        for sheep in sheepSet:
            distVec = self.getShortestDistVec(sheep)
            dist = np.linalg.norm(distVec)
            if minDist == None or dist < minDist:
                minDist = dist
                minDistVec = distVec
                closestSheep = sheep
        if minDist > 0:
            self.plannedDir = minDistVec / minDist
            self.move()
        if np.linalg.norm(self.pos - closestSheep.pos) <= 0.05:
            sheepSet.remove(closestSheep)
            self.pos = np.array([random.random() for _ in range(2)])
    

