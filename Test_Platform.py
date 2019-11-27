import pygame
#import XGPIO
import Graphics
import XPhidgets
import Recipe
import pygbutton

import time

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (34, 177, 76)
lightgreen = (0, 255, 0)
lineSize = 5

bg = pygame.image.load("barleyworksbackground2.jpg")

def loadgametest():
    pygame.init()
    pygame.display.set_caption('Barley Works')

components = [False, False, False, False, False, False, False, False, False, False]
btitles = ("MP", "MV", "BP", "BV", "FV", "CV", "HTR", "BH", "FH", "AH")
buttons = []
bxy = []
bxy.append([200, 370])
bxy.append([360, 240])
bxy.append([750, 465])
bxy.append([405, 440])
bxy.append([532, 340])
bxy.append([605, 495])
bxy.append([615, 320])
bxy.append([395, 180])
bxy.append([395, 140])
bxy.append([395, 100])
bwidth = 60
bheight = 30

def makebuttons():
    for i in range(10):
        xy = []
        xy = bxy[i]
        x = xy[0]
        y = xy[1]
        buttons.append(pygbutton.PygButton((bxy[i][0], bxy[i][1], bwidth, bheight), btitles[i]))
    return buttons

def checkbuttons(buttons, gameDisplay):
    for i in range(10):
        buttons[i].draw(gameDisplay)
        for event in pygame.event.get():  # event handling loop
            for i in range(10):
                if 'click' in buttons[i].handleEvent(event):
                    if components[i] is True:
                        components[i] = False
                    else:
                        components[i] = True
                # XGPIO.setGPIO2(components)

def gameLoop():
    gameExit = False
    global components
    clock = pygame.time.Clock()
    state = True
    btns = makebuttons()
    while state:
        #   for event in pygame.event.get():
        #   state = check()   if event.type ==pygame.QUIT:
        #         gameExit = True

        gameDisplay = pygame.display.set_mode((1002, 672))
        gameDisplay.fill(white)
        gameDisplay.blit(bg, (0, 0))
        Graphics.displaytemp(gameDisplay, 100)  #need to create a multitimer to gettemp
        Graphics.displayphase(gameDisplay, "Test Environment")
        Graphics.displayheatersignal(gameDisplay, 50)
        checkbuttons(btns, gameDisplay)
        Graphics.changeGraphics(gameDisplay, components)
        pygame.display.update()
        # time.sleep(10)
        clock.tick(30)

    def endgameLoop(self):
            pygame.quit()
            quit()

#XGPIO.setup()
loadgametest()
gameLoop()



