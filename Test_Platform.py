import pygame
import XGPIO
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
                XGPIO.setGPIO(components)   #todo see if this should be moved left one


def level_callback(args):
    global components
    components[10], components[11] = XGPIO.getlevel()
    XGPIO.setGPIO(components)




def gameLoop():
    gameExit = False
    global components
    clock = pygame.time.Clock()
    state = True
    btns = makebuttons()
    while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                XGPIO.GPIO.cleanup()
                quit()

        gameDisplay = pygame.display.set_mode((1002, 672))
        gameDisplay.fill(white)
        gameDisplay.blit(bg, (0, 0))
        Graphics.displaytemp(gameDisplay, XPhidgets.temp9)

        #need to create a multitimer to gettemp
        Graphics.displayphase(gameDisplay, "Test Environment")
        Graphics.displayheatersignal(gameDisplay, components, 50)
        checkbuttons(btns, gameDisplay)
        Graphics.changeGraphics(gameDisplay, components)
        pygame.display.update()

        clock.tick(30)

    def endgameLoop(self):
            pygame.quit()
            quit()

XGPIO.setup()
loadgametest()
channel = XPhidgets.gettemp3()
L1, L2 = XGPIO.getlevel()
components.append(L1)
components.append(L2)
XGPIO.setlevel_callback(level_callback)
gameLoop()
XPhidgets.closetemp(channel)




