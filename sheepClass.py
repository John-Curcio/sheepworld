# Libraries
import numpy as np
import random
# Custom modules
import animalClass as ac

class Sheep(ac.Animal):

    def __init__(self, **kwargs):
        speed = 0.01
        color = (0, 0, 0)
        if "speed" in kwargs: speed = kwargs["speed"]
        if "color" in kwargs: color = kwargs["color"]
        ac.Animal.__init__(self, speed=speed, color=color)
        self.age = 1 # yes, not zero. 
        self.strategy = Strategy(self, numGenes=20)
        self.plannedDir = np.array([1.0, 0.0]) 

    def planMove(self, sheepSet, wolf=None):
        sheepVec = np.array([0.0, 0.0])
        sheepSet = sheepSet.difference({self})
        for sheep in sheepSet:
            sheepVec += self.strategy.getWeightedDistVec(self.strategy.sheepDistWeights, sheep)
        sheepVec /= np.linalg.norm(sheepVec)
        
        wolfVec = np.array([0.0, 0.0])
        if wolf != None:
            wolfVec = self.strategy.getWeightedDistVec(self.strategy.wolfDistWeights, wolf)

        self.plannedDir = self.strategy.sheepWeight * sheepVec + self.strategy.wolfWeight * wolfVec
        self.plannedDir /= np.linalg.norm(self.plannedDir)

    def move(self):
        self.pos += self.speed * self.plannedDir
        self.pos = self.pos % (2*np.pi)


class Strategy(object):
    """
    This object contains a sheep's entire genetic material.

    numGenes refers to how many distances a sheep recognizes. For example, if 
    numGenes = 1, then the sheep treats all animals as equidistant. 

    sheepDistWeights refers to the weight a sheep assigns to another sheep, 
    given the distance separating them. Similarly for wolfDistWeights.
    
    sheepWeight refers to how heavily a sheep should weigh the sum of 
    weighted sheep relative position vecotrs, compared to the relative 
    position vector of a wolf.
    """
    def __init__(self, owner, **kwargs):
        self.owner = owner #owner refers to the sheep that owns this strategy
        self.mutationRate = 0.05
        if "mutationRate" in kwargs:
            self.mutationRate = kwargs["mutationRate"]
        if "color" in kwargs:
            self.color = kwargs["color"]
        numGenes = 7
        if "numGenes" in kwargs:
            numGenes = kwargs["numGenes"]
        self.sheepDistWeights = np.array([random.random() for _ in range((numGenes - 2)//2)])
        mag = np.linalg.norm(self.sheepDistWeights)
        if mag > 0:
            self.sheepDistWeights /= mag
        self.wolfDistWeights = np.array([random.random() for _ in range((numGenes - 2)//2)])
        mag = np.linalg.norm(self.wolfDistWeights)
        if mag > 0:
            self.wolfDistWeights /= mag
        self.sheepWeight = random.random()
        self.wolfWeight = 1 - self.sheepWeight

    def asList(self):
        return [self.sheepWeight] + [self.wolfWeight] + [self.sheepDistWeights] + [self.wolfDistWeights]

    """
    Calculate the total variance in the strategies, and have the mutation rate 
    be the inverse square root of that. 
    Wish there were a more mathematically-justified way to do this, but hey,
    it's a learning experience.
    """
    def getMutationRate(self, parents):
        nParents = len(parents)
        sqMean = 0.0
        meanSq = 0.0
        for parent in parents:
            foo = np.array(parent.strategy.asList())
            sqMean += sum(foo)
            meanSqVec += sum(foo**2)
        sqMean *= sqMean
        n = nParents*len(parents)
        variance = (meanSqVec - sqMean) / n
        return max(variance**-0.5, 0.0001)

    """
    This sheep wants to have a baby, so it needs mate(s).
    There may be any number of mates >=2.
    Older sheep probably did something good to live so long, so they're sexier,
    i.e. more likely to be chosen as mates.
    """
    def chooseMates(sheepSet, numMates): 
        sheepList = list( sheepSet.difference({self.owner}) )
        sheepSqAges = [sheep.age**2 for sheep in sheepList]
        totalSqAge = sum(sheepSqAges)
        mateProbs = [sqAge / totalSqAge for sqAge in sheepSqAges]
        mates = set()
        for _ in range(numMates):
            p = np.random.random()
            cumulative = 0
            for i in range(len(mateProbs)):
                cumulative += mateProbs[i]
                if p >= cumulative:
                    mates.add(sheepList[i])
                    break
        return mates

    def getWeightedDistVec(self, weights, animal):
        shortestDistVec = np.array([0.0, 0.0])
        for i in range(len(animal.pos)):
            a = animal.pos[i] - self.owner.pos[i]
            b = 2*np.pi - animal.pos[i] - self.owner.pos[i]
            shortestDistVec[i] = valWithMinAbs(a, b)
        shortestDist = sum([x**2 for x in shortestDistVec])**0.5 
        # ^ this is the shortest angular distance, which is proportional to the 
        #length of the shortest path from two points on a sphere
        maxDist = np.sqrt(2) * np.pi
        n = len(weights)
        for i in range(n):
            if (maxDist * (i+1) / n) >= shortestDist:
                return (weights[i] * shortestDistVec / np.linalg.norm(shortestDistVec))
        print("Couldn't find the right weight. Here's the distance: " + str(shortestDist))
        print("...and here's the shortestDistVector: " + str(shortestDistVec))
        print("...and here's animal.pos - self.owner.pos: " + str(animal.pos - self.owner.pos))
        assert(False)


def breed(parents): 
    #parents is a set of sheep. there may be an arbitrary number of parents
    sheep3 = Sheep()
    nParents = len(parents)    
    mutationRate = getMutationRate(parents)
    for i in range(len(sheep3.strategy.sheepDistWeights)):
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
    #sheepWeight varies according to a logistic model
    t = np.log(sheep3.sheepWeight / (1 - sheep3.sheepWeight))
    t += random.gauss(0.0, sheep3.strategy.mutationRate)
    sheep3.sheepWeight += sigmoid(t)
    sheep3.wolfWeight = 1 - sheep3.sheepWeight
    return sheep3

def getMinAngle(u, v):
    cos = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    return np.arccos(cos)


def getShortestDistVec(a, b): #want to get from point A to point B, as always.
    result = np.array([0.0]*len(b))
    for i in range(len(result)):
        result[i] = valWithMinAbs((b - a)[i], (2*np.pi - a - b)[i])
    return result

def getVariance(A):
    n = len(A)
    mean = 0
    meanSq = 0
    for a in A:
        meanSq += a
        mean += a
    meanSq /= n
    mean /= n
    return meanSq - mean**2

def sigmoid(t):
    return 1/(1 + np.exp(-1*t))

def valWithMinAbs(*args):
    val = None
    for x in args:
        if val == None or abs(x) < abs(val):
            val = x
    return val
