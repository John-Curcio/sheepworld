#Libraries
import pygame
from pygame.locals import *
#Custom modules
import planetClass as pc
import sheepClass as sc
import wolfClass as wc
import playerClass as debug
################################################################################
###Global variables

##Graphics
pygame.init() 
#set up the window
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size) #set size of game window
background = pygame.Surface(screen.get_size()) #create empty surface
background.fill((0, 100, 230)) #fill surface with some color
background = background.convert()   
#^ not 100% necessary, just makes things faster, I'm told.
#surfaces with transparency need .convert_alpha() instead

#after creating the background, the surface isn't visible yet.
#need to blit (~paint) it in order to see it 
screen.blit(background, (0, 0)) #(0,0) is upper left corner

##Debugging
#The following is useful for debugging, but may be useful for other stuff later
debugMode = True
arrowsToDirs = {pygame.K_DOWN:[0,1], 
                pygame.K_UP:[0,-1], 
                pygame.K_LEFT:[-1,0], 
                pygame.K_RIGHT:[1,0]}

################################################################################

def main():
    FPS = 30 #desired frame rate in frames per second.
    clock = pygame.time.Clock() #create a pygame clock object
    playtime = 0.0 #milliseconds elapsed since start of game.
    planet = pc.Planet()
    maxHerdSize = 25
    numMates = 2
    minHerdSize = 10
    #paramDict is a dictionary of this simulation's parameters.
    paramDict = {   "maxHerdSize": maxHerdSize, 
                    "minHerdSize": minHerdSize, 
                    "numMates": numMates}
    sheepSet = set()
    # player = debug.Player(pos=(1/2, 1/2), speed=0.05, color=(255, 0, 0))
    # sheepSet.add(player)
    for i in range(maxHerdSize):
        sheepSet.add(sc.Sheep(numGenes=3))
    wolf = wc.Wolf(color=(255,255,255), speed=0.04)

    while True:
        milliseconds = clock.tick(FPS)
        playtime += milliseconds
        deltaTime = milliseconds / 1000.0
        #^ clock.tick() returns number of milliseconds passed since last frame
        #FPS is otional. passing it causes a delay so that you dont go faster than FPS in your game
        screen.blit(background, (0, 0)) 
        sheepSet = step(sheepSet, paramDict, wolf)
        pygame.display.flip()

"""
doHerdStuff takes care of everything the herd must do at every time step. This 
includes breeding, planning moves, executing moves, and drawing.
"""
def doHerdStuff(screen, sheepSet, paramDict, wolf=None):
    for s in sheepSet:
        s.planMove(sheepSet.difference({s}), wolf)
    for sheep in sheepSet:
        sheep.move()
        sheep.draw(screen, size)
    if len(sheepSet) <= paramDict["minHerdSize"]:
        for sheep in sheepSet:
            sheep.age += 1
        newSheepSet = set()
        for sheep in sheepSet:
            sheep.randomizePos()
            candidates = sheepSet.difference({sheep})
            mates = sheep.strategy.chooseMates(candidates, paramDict["numMates"])
            if mates == None:
                print("mate-finding failed")
                pygame.quit()
                return
            mates.append(sheep)
            newSheepSet.add(sc.breed(mates))
        print("another generation passed")
        sheepSet = sheepSet.union(newSheepSet)
    return sheepSet


def step(sheepSet, paramDict, wolf=None):
    if wolf != None:
        wolf.hunt(sheepSet)
        wolf.draw(screen, size)
    # print("before:", len(sheepSet))
    sheepSet = doHerdStuff(screen, sheepSet, paramDict, wolf)
    # print("after:", len(sheepSet))
    # if len(sheepSet) < paramDict["minHerdSize"]:
    #     print("it's too small", len(sheepSet))
    pygame.event.get()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]: 
        pygame.quit()

    return sheepSet

if __name__ == "__main__":
    main()