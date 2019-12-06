GPIOActive = True
import pygame
if GPIOActive == True:
    import XGPIO
    import RPi.GPIO as GPIO
import Graphics
import XPhidgets
import Recipe
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

    def __init__(self, func, equipMent, setpoint, heaterSignal, tempmode, phase):
        self.phase = phase
        self.equipMent = equipMent
        self.setpoint = setpoint
        #self.gameDisplay = gameDisplay
        if GPIOActive:
            self.components = XGPIO.setGPIO(self.equipMent)
        else:
            self.components = [False, False, False, False, False, False, False, False, False, False]
        self.func = func
        self.heaterSignal = heaterSignal
        self.tempmode = tempmode
        XPhidgets.setheatersignal(self.heaterSignal)
        self.gameLoop()

    def gameLoop(self):
        gameExit = False
        clock = pygame.time.Clock()
        state = True

        while state:
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    XGPIO.GPIO.cleanup()
                    quit()


            self.gameDisplay = pygame.display.set_mode((1002, 672))
            self.gameDisplay.fill(white)
            self.gameDisplay.blit(bg, (0, 0))
            state = self.func(self)
            Graphics.displayphase(self.gameDisplay, self.phase)
            if self.tempmode is True:
                Graphics.displaytemp(self.gameDisplay, XPhidgets.temp9)
                Graphics.displayheatersignal(self.gameDisplay, self.heaterSignal)
            Graphics.changeGraphics(self.gameDisplay, self.components)
            pygame.display.update()
            # time.sleep(10)
            clock.tick(30)

    def endgameLoop(self):
            pygame.quit()
            quit()


#SETUP
Recipe = Recipe.gettestrecipe()
# Recipe = Recipe.getrecipe()
if GPIOActive:
    XGPIO.setup()
loadgametest()



# HEAT TO STRIKE TEMPERATURE 1
def endheat2strike(self):
    self.state = True
    temperature = XPhidgets.temp9

    if temperature >= self.setpoint:
        #temptimer.stop()
        self.state = False
        return self.state
    else:
        return self.state


phase = "Heat to Strike"
equipMent = [2, 6]  # BP and Heater
stkTemp = Recipe[1]
heaterSignal = 100
tempmode = True
channel = XPhidgets.gettemp3()  #starts temperature event handler, returns the channel so it can be closed later
heat2strike = Operation(endheat2strike, equipMent, stkTemp, heaterSignal, tempmode, phase)
XPhidgets.closetemp(channel)
tempmode = False


# Transfer to Mash Tun
def endfillmash(self):
    self.state = True
    if XGPIO.GPIO.event_detected(XGPIO.levelpins[0]) or XGPIO.boilerlevel is False:
        self.state = False
        return self.state
    else:
        return self.state

phase = "Fill Mashtun"
equipMent = [2, 3]

XGPIO.leveldetector()  #todo figure out by this ends for rising and falling

heaterSignal = 0
tempmode = False
fillmash = Operation(endfillmash, equipMent, 0, heaterSignal, tempmode, phase)

#Mix

def endmashmix(self):

    self.state = True
    self.state = Graphics.buttoncontrol(self.setpoint, self.gameDisplay)
    return self.state



phase = "Mix Mashtun"
equipMent = []
heaterSignal = 0
tempmode = False
ctrbtns = Graphics.makecontrolbutton("Mix Complete")
mixmash = Operation(endmashmix, equipMent, ctrbtns, heaterSignal, tempmode, phase)


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
    heatctrlbtns = self.setpoint[3]
    self.heaterSignal = Graphics.heaterctrlbuttons(heatctrlbtns, self.gameDisplay, self.heaterSignal)
    
    if time.time() >= (mashtime + starttime):
        self.state = False
        return self.state
    else:
        self.state = True
        return self.state



mashtemp = Recipe[2]
phase = "Mash"
equipMent = [0, 1, 2, 3, 6]
heaterSignal = 30
tempmode = True
starttime = time.time()
mashtime = Recipe[3]
heatctrlbtns = Graphics.makehtrctrlbtns()
mashinfo = [mashtime, starttime, mashtemp, heatctrlbtns]
mash = Operation(endmash, equipMent, mashinfo, heaterSignal, tempmode, phase)



