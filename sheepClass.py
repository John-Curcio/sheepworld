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
    def __init__(self, **kwargs):
        self.mutationRate = 0.05
        if "mutationRate" in kwargs:
            self.mutationRate = kwargs["mutationRate"]
        if "color" in kwargs:
            self.color = kwargs["color"]
        numGenes = 7
        if "numGenes" in kwargs:
            numGenes = kwargs["numGenes"]
        self.sheepDistWeights = np.array([random.random() for _ in range((numGenes - 2)//2)])
        self.sheepDistWeights = np.linalg.norm(self.sheepDistWeights)
        self.wolfDistWeights = np.array([random.random() for _ in range((numGenes - 2)//2)])
        self.wolfDistWeights = np.linalg.norm(self.wolfDistWeights)
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

    def getWeightedDistVec(self, weights, animal):
        shortestDistVec = [valWithMinAbs(x, 2*np.pi - x) for x in animal.pos - self.pos]
        shortestDistVec = np.array(shortestDistVec)
        shortestDist = sum([x**2 for x in shortestDistVec])**0.5 
        # ^ this is the shortest angular distance, which is proportional to the 
        #length of the shortest path from two points on a sphere
        for i in range(1, len(weights)+1):
            if (2*np.pi * i / n) >= shortestDist:
                return weights[i] * shortestDistVec
        #Shouldn't ever make it this far
        print("Couldn't find the right weight. Here's the distance: " + str(shortestDist))
        assert(False)

    def move(self, sheepSet, wolf=None):
        sheepVec = np.array([0.0, 0.0])
        sheepSet = sheepSet.difference({self})
        for sheep in sheepSet:
            sheepVec += getWeightedDistVec(self.sheepDistWeights, sheep)
        sheepVec = np.linalg.norm(sheepVec)
        
        wolfVec = np.array([0.0, 0.0])
        if wolf != None:
            wolfVec = getWeightedDistVec(self.wolfDistWeights, wolf)

        dirVec = self.sheepWeight * sheepVec + self.wolfWeight * wolfVec
        dirVec = np.linalg.norm(vec)


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
