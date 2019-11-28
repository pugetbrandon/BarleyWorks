GPIOActive = False
import pygame
if GPIOActive == True:
    import XGPIO
import Graphics
import XPhidgets
import Recipe
import multitimer

import time

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
lineSize = 5

bg = pygame.image.load("barleyworksbackground2.jpg")

def loadgametest():
    pygame.init()
    pygame.display.set_caption('Barley Works')

class Operation:

    def __init__(self, func, equipMent, setpoint, initheatersignal, tempmode, phase):
        self.phase = phase
        self.equipMent = equipMent
        self.setpoint = setpoint
        if GPIOActive == True:
            self.components = XGPIO.setGPIO(self.equipMent)
        else:
            self.components = [False, False, False, False, False, False, False, False, False, False]
        self.func = func
        self.initheatersignal = initheatersignal
        self.tempmode = tempmode
        XPhidgets.setheatersignal(self.initheatersignal)
        self.gameLoop()

    def gameLoop(self):
        gameExit = False
        clock = pygame.time.Clock()
        state = True

        while state:
            #   for event in pygame.event.get():
            #   state = check()   if event.type ==pygame.QUIT:
            #         gameExit = True
            #multitimer.MultiTimer(1, self.func(self), self, -1, runonstart=True)
            #state = self.state
            state = self.func(self)
            gameDisplay = pygame.display.set_mode((1002, 672))
            gameDisplay.fill(white)
            gameDisplay.blit(bg, (0, 0))
            Graphics.displayphase(gameDisplay, self.phase)
            if self.tempmode is True:
                Graphics.displaytemp(gameDisplay, XPhidgets.temp9)
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
if GPIOActive == True:
    XGPIO.setup()
loadgametest()



# HEAT TO STRIKE TEMPERATURE 1
def endheat2strike(self):
    self.state = True
    #XPhidgets.gettimedtemp()
    #XPhidgets.gettemp3()
    temperature = XPhidgets.temp9

    #temperature = XPhidgets.gettemp()
    #self.temperature = temperature
    if temperature >= self.setpoint:
        #temptimer.stop()
        self.state = False
    else:
        return self.state


phase = "Heat to Strike"
equipMent = [2, 6]  # BP and Heater
stkTemp = Recipe[1]  # recipe is never called
heaterSignal = 100
tempmode = True
channel = XPhidgets.gettemp3()
heat2strike = Operation(endheat2strike, equipMent, stkTemp, heaterSignal, tempmode, phase)
XPhidgets.closetemp(channel)
heat2strike.endgameLoop()
print("Success")


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

