GPIOActive = True
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
        return self.state
    else:
        return self.state


phase = "Heat to Strike"
equipMent = [2, 6]  # BP and Heater
stkTemp = Recipe[1]  # recipe is never called
heaterSignal = 100
tempmode = True
channel = XPhidgets.gettemp3()  #starts temperature event handler, returns the channel so it can be closed later
heat2strike = Operation(endheat2strike, equipMent, stkTemp, heaterSignal, tempmode, phase)
XPhidgets.closetemp(channel)
tempmode = False
#heat2strike.endgameLoop()

# Transfer to Mash Tun
def endfillmash(self):
    self.state = True
    if GPIO.event_detected(XGPIO.levelpins[0]) or GPIO.event_detected(XGPIO.levelpins[1]):
        self.state = False
        return self.state
    else:
        return self.state

phase = "Fill Mashtun"
equipMent = [3, 4]
XGPIO.GPIO.add_event_detect(XGPIO.levelpins[0], RISING)
XGPIO.GPIO.add_event_detect(XGPIO.levelpins[1], FALLING)
heaterSignal = 0
tempmode = False
fillmash = Operation(endfillmash, equipMent, 0, heaterSignal, tempmode, phase)

#Mix

def endmashmix(self):
    self.state = Graphics.buttoncontrol(self.gameDisplay, "Complete Mixing")
    return self.state

phase = "Mix Mashtun"
equipMent = []
heaterSignal = 0
tempmode = False
mixmash = Operation(endmashmix, equipMent, 0, heaterSignal, tempmode, phase)


# Filter

def endfiltermash(self):
    self.state = True
    if time.time() >= (self.setpoint[0] + self.setpoint[1]):
        self.state = False
        return self.state
    return self.state

phase = "Filter Mashtun"
equipMent = [0]
filterTime = Recipe[9]
heaterSignal = 0
tempmode = False
starttime = time.time()
timerinfo = [filterTime, starttime]
filtermash = Operation(endfiltermash, equipMent, timerinfo, heaterSignal, tempmode, phase)

# Mash
def endmash(self):
    mashtime = self.setpoint[0]
    starttime = self.setpoint[1]
    mashtemp = self.setpoint[2]
    self.heaterSignal = Graphics.heaterctrlbuttons(self.heaterSignal)
    
    if time.time() >= (mashtime + starttime):
        self.state = False
        return self.state
    else:
        self.state = True
        return self.state



mashtemp = Recipe[2]
phase = "Mash at", str(mashtemp), "F"
equipMent = [0, 1, 2, 3, 6]
heaterSignal = 30
tempmode = True
starttime = time.time()
mashtime = Recipe[3]
mashinfo = [mashtime, starttime, mashtemp]
mash = Operation(endmash, equipMent, mashinfo, heaterSignal, tempmode, phase)



