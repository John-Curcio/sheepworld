# Libraries
import numpy as np
import random
# Custom modules
import animalClass as ac

class Sheep(ac.Animal):

    def __init__(self):
        ac.Animal.__init__(self)
        self.strategy = Strategy()

#This object contains a sheep's entire genetic material.
class Strategy(object):

    def __init__(self, **kwargs):
        sheep.age = 1
        self.mutationRate = 0.05
        if "mutationRate" in kwargs:
            self.mutationRate = kwargs["mutationRate"]
        numGenes = 5
        if "numGenes" in kwargs:
            numGenes = kwargs["numGenes"]
        # sheepDistWeights refers to the weight a sheep assigns to another sheep, 
        # given the distance separating them. Similarly for wolfDistWeights.
        self.sheepDistWeights = np.array([random.random()] * numGenes)
        self.sheepDistWeights = np.linalg.norm(self.sheepDistWeights)
        self.wolfDistWeights = np.array([random.random()] * numGenes)
        self.wolfDistWeights = np.linalg.norm(self.wolfDistWeights)
        # sheepWeight refers to how heavily a sheep should weigh the sum of 
        # weighted sheep relative position vecotrs, compared to the relative 
        # position vector of a wolf.
        self.sheepWeight = random.random()
        self.wolfWeight = 1 - self.sheepWeight

    def chooseMates(sheepSet, numMates): #there may be any number of mates >= 2
        #older sheep are sexier, and are more likely to be chosen as mates.
        sheepList = list( sheepSet.difference({self}) )
        sheepSqAges = [sheep.age**2 for sheep in sheepList]
        totalSqAge = sum(sheepSqAges)
        mateProbs = [sqAge / totalSqAge for sqAge in sheepSqAges]

        mates = set()
        for unusedVariable in range(numMates):
            p = np.random.random()
            cumulative = 0
            for i in range(len(mateProbs)):
                cumulative += mateProbs[i]
                if p >= cumulative:
                    mates.add(sheepList[i])
                    break
        return mates


def breed(*args): 
    parents = args #there may be an arbitrary number of parents
    sheep3 = Sheep()
    nParents = len(parents)
    for i in range(len(sheep3.strategy)):
        #for each gene of the new strategy, randomly choose a subset of parents,
        #and set this gene to be the average of the i'th genes of the subset of
        #parents
        k = random.randrange(1, nParents)
        parentSubset = random.sample(parents, k)
        sheep3.strategy[i] = 0.0
        for parent in parentSubset:
            sheep3.strategy[i] += parent.strategy[i]
        sheep3.strategy[i] /= k
        #mutations also occur, but their severity is determined by the 
        #mutationRate, not necessarily their frequency.
        sheep3.strategy[i] += random.gauss(0.0, sheep3.strategy.mutationRate)
    return sheep3



