import pygame
import XGPIO
import Graphics
import XPhidgets
import Recipe

import time

# new color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
lineSize = 5

bg = pygame.image.load("barleyworksbackground2.jpg")

# Items needed for setup
# need to energize hoppers and set initial valve position
# XGPIO.setup()
# loadgametest()

def loadgametest():
    pygame.init()
    pygame.display.set_caption('Barley Works')

class Operation:

    def __init__(self, func, equipMent, setpoint, initheatersignal):
        #self.phase = phase
        self.equipMent = equipMent
        self.setpoint = setpoint
        self.components = XGPIO.setGPIO(self.equipMent)
        self.func = func
        self.initheatersignal = initheatersignal
        XPhidgets.setheatersignal(self.initheatersignal)
        self.gameLoop(self)

    def endheat2strike(self, setpoint):
        state = True
        self.setpoint = setpoint
        temperature = XPhidgets.whattemp()
        if temperature >= self.setpoint:
            state = False
        return state


    def endfillmashtun(self):
        state = True
        level = XGPIO.getlevel()
        if level[0] is True or level[1] is False:
            state = False
        return state

    def gameLoop(self):
        gameExit = False
        clock = pygame.time.Clock()
        state = True

        while state:
            #   for event in pygame.event.get():
            #   state = check()   if event.type ==pygame.QUIT:
            #         gameExit = True

            state = self.func(self.setpoint)
            gameDisplay = pygame.display.set_mode((1002, 672))
            gameDisplay.fill(white)
            gameDisplay.blit(bg, (0, 0))
            Graphics.changeGraphics(gameDisplay, self.components)
            pygame.display.update()
            # time.sleep(10)
            clock.tick(30)

    def endgameLoop(self):
            pygame.quit()
            quit()

# need to energize hoppers and set initial valve position
#SETUP
Recipe = Recipe.gettestrecipe()
# Recipe = Recipe.getrecipe()
XGPIO.setup()
loadgametest()



# HEAT TO STRIKE TEMPERATURE 1
def endheat2strike(self, setpoint):
        temperature = XPhidgets.gettemp()
        if temperature >= self.setpoint:
            state = False
        return state

#phase = "heat2strike"
equipMent = [2, 6]  # BP and Heater
stkTemp = Recipe[1]  # recipe is never called
heaterSignal = 100
heat2strike = Operation(endheat2strike, equipMent, stkTemp, heaterSignal)

heat2strike.endgameLoop()
print("Success")
# TODO  need to creat a pause here to allow a button to be pushed to start transfer.
# TODO learn how to create a button

'''
# Transfer to Mash Tun
phase = "fillmashtun"
equipMent = [3, 4]
components = setState(equipMent)
XGPIO.setGPIOhi(components)
gameLoop(phase, components, 0)

# Filter
phase = "filter"
equipMent = [0]
components = setState(equipMent)
XGPIO.setGPIOhi(components)
gameLoop(phase, components, 0)
# TODO create
'''

