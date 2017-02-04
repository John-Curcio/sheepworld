# Libraries
import numpy as np
import random
# Custom modules
import animalClass as ac

class Sheep(ac.Animal):

    def __init__(self):
        ac.Animal.__init__(self, 5)
        self.age = 1 # yes, not zero. 
        self.strategy = Strategy()

#This object contains a sheep's entire genetic material.
class Strategy(object):

    def __init__(self, **kwargs):
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

    def move(sheepSet, wolf=None): #TODO: currently full of flaws and incomplete
        vec = np.array([0.0, 0.0])
        sheepSet = sheepSet.difference({self})
        for sheep in sheepSet:
            distVec = [min(x, 2*np.pi - x) for x in sheep.pos - self.pos] #TODO: incorrect. need value with minimum absolute value
            dist = sum([x**2 for x in distVec])**0.5 
            #this is the distance in angles, which is proportional to the length
            #of the shortest path from two points on a sphere
            n = len(self.sheepDistWeights)
            weight = None
            for i in range(n):
                if dist >= 2*np.pi * i / n:
                    weight = self.sheepDistWeights[i]
                    break
            vec += np.array([weight * x for x in (sheep.pos - self.pos)])
        vec = np.linalg.norm(vec)

        wolfVec = np.array([0.0, 0.0])
        if wolf != None:
            n = len(self.wolfDistWeights)
            for i in range(n):
                if dist >= 2*np.pi * i / n:
                    wolfVec += self.wolfDistWeights[i] * (self.pos - wolf.pos)
            vec = self.sheepWeight * vec + self.wolfWeight * wolfVec
            vec = np.linalg.norm(vec)
        self.pos += self.speed * vec


def breed(parents): 
    #parents is a set of sheep
    #there may be an arbitrary number of parents
    sheep3 = Sheep()
    nParents = len(parents)
    for i in range(len(sheep3.sheepDistWeights)):
        #for each gene of the new strategy, randomly choose a subset of parents,
        #and set this gene to be the average of the i'th genes of the subset of
        #parents
        k = random.randrange(1, nParents)
        parentSubset = random.sample(parents, k)
        sheep3.sheepDistWeights[i] = 0.0
        sheep3.wolfDistWeights[i] = 0.0
        for parent in parentSubset:
            sheep3.sheepDistWeights[i] += parent.sheepDistWeights[i]
            sheep3.wolfDistWeights[i] += parent.wolfDistWeights[i]
        sheep3.sheepDistWeights[i] /= k
        sheep3.wolfDistWeights[i] /= k
        #mutations also occur, but their severity is determined by the 
        #mutationRate, not necessarily their frequency.
        sheep3.sheepDistWeights[i] += random.gauss(0.0, sheep3.strategy.mutationRate)
        sheep3.wolfDistWeights[i] += random.gauss(0.0, sheep3.strategy.mutationRate)
    sheep3.sheepWeight += random.gauss(0.0, sheep3.strategy.mutationRate)
    sheep3.sheepWeight = min(sheep3.sheepWeight, 1)
    sheep3.sheepWeight = max(sheep3.sheepWeight, 0)
    sheep3.wolfWeight = 1 - sheep3.sheepWeight
    return sheep3



