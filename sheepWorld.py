#########################################
# 
#  
#     |
# [}^8|]> oh hey its wild bill hickok! i thought you were dead! what are you doing here in sheepworld?
#     |   
#     
#########################################

#Libraries
import pygame
from pygame.locals import *
#Custom modules
import planetClass as pc
import sheepClass as sc
import playerClass as debug
################################################################################
###Global variables
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

#The following is useful for debugging, but may be useful for other stuff later
debugMode = True
arrowsToDirs = {pygame.K_DOWN:[0,1], 
                pygame.K_UP:[0,-1], 
                pygame.K_LEFT:[-1,0], 
                pygame.K_RIGHT:[1,0]}

################################################################################

def main():
    FPS = 20 #desired frame rate in frames per second.
    clock = pygame.time.Clock() #create a pygame clock object
    playtime = 0.0 #milliseconds elapsed since start of game.
    planet = pc.Planet()
    maxHerdSize = 10
    sheepSet = set()
    player = debug.Player()
    for i in range(maxHerdSize):
        sheepSet.add(sc.Sheep())
    while True:
        milliseconds = clock.tick(FPS)
        playtime += milliseconds
        deltaTime = milliseconds / 1000.0
        #^ clock.tick() returns number of milliseconds passed since last frame
        #FPS is otional. passing it causes a delay so that you dont go faster than FPS in your game
        screen.blit(background, (0, 0)) 
        step(sheepSet)
        #debug stuff
        player.move()
        player.draw(screen, size)

        # V don't you dare remove this!
        pygame.display.flip()

"""
doHerdStuff takes care of everything the herd must do at every time step. This 
includes breeding, planning moves, executing moves, and drawing.
"""
def doHerdStuff(screen, sheepSet, wolf=None):
    for s in sheepSet:
        s.planMove(sheepSet.difference({s}), wolf)
    for sheep in sheepSet:
        sheep.move()
        sheep.draw(screen, size)

def step(sheepSet):
    doHerdStuff(screen, sheepSet)
    pygame.event.get()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]: 
        pygame.quit()
    

if __name__ == "__main__":
    main()