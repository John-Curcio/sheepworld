# Libraries
import numpy as np
import random
# Custom modules
import animalClass as ac

class Sheep(ac.Animal):

    def __init__(self, **kwargs):
        speed = 0.01
        color = (0, 0, 0)
        numGenes = 20
        if "speed" in kwargs: speed = kwargs["speed"]
        if "color" in kwargs: color = kwargs["color"]
        if "numGenes" in kwargs: numGenes = kwargs["numGenes"]
        ac.Animal.__init__(self, speed=speed, color=color)
        self.age = 1 # yes, not zero. 
        self.strategy = Strategy(self, numGenes=numGenes)

    """ a sheep's intended direction is a linear combination of the minimum 
    relative position vectors between the sheep and other sheep and the minimum
    relative position vector between the sheep and the wolf. The weights are in
    the sheep's genetic material.

    if a sheep is undecided - i.e. its intended direction has magnitude zero -
    then it stays still
    """
    def planMove(self, sheepSet, wolf=None):
        sheepVec = np.array([0.0, 0.0])
        sheepSet = sheepSet.difference({self})
        for sheep in sheepSet:
            sheepVec = sheepVec + self.strategy.getWeightedDistVec(self.strategy.sheepDistWeights, sheep)
        mag = np.linalg.norm(sheepVec)
        if mag != 0:
            sheepVec = sheepVec / mag
        
        wolfVec = np.array([0.0, 0.0])
        if wolf != None:
            tempVec = self.strategy.getWeightedDistVec(self.strategy.wolfDistWeights, wolf)
            if np.linalg.norm(tempVec) > 0:
                wolfVec = tempVec
        self.plannedDir = self.strategy.sheepWeight * sheepVec + self.strategy.wolfWeight * wolfVec
        mag = np.linalg.norm(self.plannedDir)
        if mag != 0:
            self.plannedDir = self.plannedDir / mag

    def move(self):
        self.pos += self.speed * self.plannedDir
        self.pos = self.pos % 1


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
        self.mutationRate = 0.5
        if "mutationRate" in kwargs:
            self.mutationRate = kwargs["mutationRate"]
        if "color" in kwargs:
            self.color = kwargs["color"]
        numGenes = 7
        if "numGenes" in kwargs:
            numGenes = kwargs["numGenes"]
        self.sheepDistWeights = np.array([random.randrange(-1, 1) for _ in range((numGenes - 2)//2)])
        mag = np.linalg.norm(self.sheepDistWeights)
        if mag > 0:
            self.sheepDistWeights = self.sheepDistWeights / mag
        self.wolfDistWeights = np.array([random.randrange(-1, 1) for _ in range((numGenes - 2)//2)])
        mag = np.linalg.norm(self.wolfDistWeights)
        if mag > 0:
            self.wolfDistWeights = self.wolfDistWeights / mag
        self.sheepWeight = random.random()
        self.wolfWeight = 1 - self.sheepWeight

    def asList(self):
        return ([self.sheepWeight] + 
                [self.wolfWeight] + 
                list(self.sheepDistWeights) + 
                list(self.wolfDistWeights))

    """
    Calculate the total variance in the strategies, and have the mutation rate 
    be the inverse square root of that. 
    Var(X) = E[X**2] - E[X]**2
    Wish there were a more mathematically-justified way to do this, but hey,
    it's a learning experience.
    """
    def getMutationRate(self, parents):
        nParents = len(parents)
        variance = 0.0

        totalVariance = 0.0
        parentStrategies = [parent.strategy.asList() for parent in parents]

        geneSumSquares = 0.0
        for geneIndex in range(len(parentStrategies[0])):
            parentGenes = [strategy[geneIndex] for strategy in parentStrategies]
            geneSumSquares = sum([gene**2 for gene in parentGenes])
            totalVariance += np.mean(geneSumSquares) - np.mean(parentGenes)
            #variance is additive
        return (totalVariance**-0.5 / len(parentStrategies[0]))

    """
    This sheep wants to have a baby, so it needs mate(s).
    There may be any number of mates >=2. Also possible for this sheep to choose
    another sheep more than once.
    Older sheep probably did something good to live so long, so they're more 
    attractive, i.e. more likely to be chosen as mates.
    """
    def chooseMates(self, sheepSet, numMates): 
        sheepList = list( sheepSet.difference({self.owner}) )
        sheepSqAges = [sheep.age**2 for sheep in sheepList]
        totalSqAge = sum(sheepSqAges)
        if totalSqAge == 0:
            sheepSqAges = [1 / len(sheepList)] * len(sheepList)
            totalSqAge = 1
        mateProbs = [sqAge / totalSqAge for sqAge in sheepSqAges]
        mates = [None] * numMates
        for mate in range(numMates):
            p = np.random.random()
            cumulative = 0
            i = 0
            mateFound = False
            while (i < len(mateProbs) and not mateFound):
                cumulative += mateProbs[i]
                if cumulative >= p:
                    mates[mate] = sheepList[i]
                    mateFound = True
                i += 1
            if not mateFound:
                return None
        if len(mates) != numMates:
            return None
        return mates

    def getWeightedDistVec(self, weights, animal):
        shortestDistVec = self.owner.getShortestDistVec(animal)
        shortestDist = np.linalg.norm(shortestDistVec)
        maxDist = 1/np.sqrt(2)
        n = len(weights)
        for i in range(n):
            if (maxDist * (i+1) / n) >= shortestDist:
                return (weights[i] * shortestDistVec / np.linalg.norm(shortestDistVec))
        # useful print statements for debugging
        print("Couldn't find the right weight. Here's the distance: " + str(shortestDist))
        print("...and here's the shortestDistVector: " + str(shortestDistVec))
        print("...and here's animal.pos: " + str(animal.pos))
        print("...and here's self.owner.pos" + str(self.owner.pos))
        assert(False)


# TODO: needs crossover
def breed(parents): 
    #parents is a set of sheep. there may be an arbitrary number of parents
    sheep3 = Sheep(numGenes=len(parents[0].strategy.asList()))
    strategy3 = sheep3.strategy
    nParents = len(parents)    
    mutationRate = strategy3.getMutationRate(parents)
    for i in range(len(strategy3.sheepDistWeights)):
        #for each gene of the new strategy, randomly choose a subset of parents,
        #and set this gene to be the average of the i'th genes of the subset of
        #parents
        k = random.randrange(1, nParents)
        parentSubset = random.sample(parents, k)
        strategy3.sheepDistWeights[i] = 0.0
        strategy3.wolfDistWeights[i] = 0.0
        for parent in parentSubset:
            strategy3.sheepDistWeights[i] += parent.strategy.sheepDistWeights[i]
            strategy3.wolfDistWeights[i] += parent.strategy.wolfDistWeights[i]
        strategy3.sheepDistWeights[i] /= k
        strategy3.wolfDistWeights[i] /= k
        #mutations also occur, but their severity is determined by the 
        #mutationRate, not necessarily their frequency.
        strategy3.sheepDistWeights[i] += random.gauss(0.0, mutationRate)
        strategy3.wolfDistWeights[i] += random.gauss(0.0, mutationRate)
    #sheepWeight varies according to a logistic model
    t = np.log(strategy3.sheepWeight / (1 - strategy3.sheepWeight))
    t += random.gauss(0.0, mutationRate)
    strategy3.sheepWeight += sigmoid(t)
    strategy3.wolfWeight = 1 - strategy3.sheepWeight
    return sheep3

def getMinAngle(u, v):
    cos = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    return np.arccos(cos)

def getVariance(A):
    n = len(A)
    mean = 0
    meanSq = 0
    for a in A:
        meanSq += a**2
        mean += a
    meanSq /= n
    mean /= n
    return meanSq - mean**2

def sigmoid(t):
    return 1/(1 + np.exp(-1*t))

