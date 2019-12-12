GPIOActive = True
Test = True
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
            self.components = XGPIO.buildcomponents(self.equipMent)
            L1, L2 = XGPIO.getlevel()
            self.components.append(L1)
            self.components.append(L2)
            XGPIO.setGPIO(self.components)
        else:
            self.components = [False, False, False, False, False, False, False, False, False, False, False, False]
        self.func = func

        XGPIO.setlevel_callback(self.level_callback)
        self.heaterSignal = heaterSignal
        self.tempmode = tempmode
        XPhidgets.setheatersignal(self.heaterSignal)
        self.state = True
        self.gameLoop()






    def level_callback(self, VAL):
        self.components[10], self.components[11] = XGPIO.getlevel()
        XGPIO.setGPIO(self.components)
        if self.phase == "Mash":
            self.levelcontrol()

    def levelcontrol(self):
        if self.components[11] is False and self.state is True:
            self.components[2] = False
            XGPIO.setGPIO(self.components)

        if self.components[11] is True and self.state is True:
            time.sleep(10)
            self.components[2] = True
            XGPIO.setGPIO(self.components)



    def gameLoop(self):
        gameExit = False
        clock = pygame.time.Clock()


        while self.state:
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    XGPIO.GPIO.cleanup()
                    quit()


            self.gameDisplay = pygame.display.set_mode((1002, 672))
            self.gameDisplay.fill(white)
            self.gameDisplay.blit(bg, (0, 0))
            self.state = self.func(self)
            Graphics.displayphase(self.gameDisplay, self.phase)
            if self.tempmode is True:
                Graphics.displaytemp(self.gameDisplay, XPhidgets.temp9)
                Graphics.displayheatersignal(self.gameDisplay, self.components, self.heaterSignal)
            Graphics.changeGraphics(self.gameDisplay, self.components)
            pygame.display.update()
            # time.sleep(10)
            clock.tick(30)

    def endgameLoop(self):
            pygame.quit()
            quit()




#SETUP
if Test:
    Recipe = Recipe.gettestrecipe()
else:
    Recipe = Recipe.getrecipe()

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
    if self.components[10] is True or self.components[11] is False:
        self.state = False
        return self.state
    else:
        return self.state

phase = "Fill Mashtun"
equipMent = [2, 3]

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
channel = XPhidgets.gettemp3()  #starts temperature event handler, returns the channel so it can be closed later
mash = Operation(endmash, equipMent, mashinfo, heaterSignal, tempmode, phase)
XPhidgets.closetemp(channel)

#Ready to Transfer

def endready2transfer(self):
    self.state = True
    self.state = Graphics.buttoncontrol(self.setpoint, self.gameDisplay)
    return self.state


phase = "Ready to Transfer to Boiler"
equipMent = []
heaterSignal = 0
tempmode = False
ctrbtns = Graphics.makecontrolbutton("Ready to Transfer")
ready2transfer = Operation(endready2transfer, equipMent, ctrbtns, heaterSignal, tempmode, phase)

#Transfer to Boiler

def endtransfer2boiler(self):
    self.state = True
    self.state = Graphics.buttoncontrol(self.setpoint, self.gameDisplay)
    return self.state

phase = "Transfer to Boiler"
equipMent = [0, 1, 6]
heaterSignal = 66
tempmode = True
ctrbtns = Graphics.makecontrolbutton("Transfer Complete")
channel = XPhidgets.gettemp3()  #starts temperature event handler, returns the channel so it can be closed later
transfer2boiler = Operation(endtransfer2boiler, equipMent, ctrbtns, heaterSignal, tempmode, phase)
XPhidgets.closetemp(channel)

#Heat to Boil
def endheat2boil(self):
    self.state = True
    print(len(self.setpoint))
    print(self.setpoint)
    if len(self.setpoint) == 0:
        self.startboil = time.time()
        self.setpoint.append(XPhidgets.gettemp())
        self.reset = False
        self.startboil = time.time()
    if self.reset:
        self.startboil = time.time()
        self.reset = False
    if time.time() >= self.startboil + 1:
        btemp = XPhidgets.temp9
        self.setpoint.append(btemp)
        if len(self.setpoint) >= 60:
            del self.setpoint[0]
            sum = 0
            for i in range(len(self.setpoint)):
                sum += self.setpoint[i]
            average = sum / len(self.setpoint)
            differ = btemp - average
            if btemp > 75 and differ < 0.1:
                self.state = False
        self.reset = True

    return self.state

phase = "Heat to Boil"
equipMent = [2, 6]
heaterSignal = 66
tempmode = True
boiltemp = []
channel = XPhidgets.gettemp3()  #starts temperature event handler, returns the channel so it can be closed later
heat2boil = Operation(endheat2boil, equipMent, boiltemp, heaterSignal, tempmode, phase)
XPhidgets.closetemp(channel)

#Boil


def endboil(self):
    self.state = True

    if time.time() >= self.setpoint[2] and self.components[7] is True:   #Bitter hops check
        self.components[7] = False
        XGPIO.setGPIO(self.components)

    if time.time() >= self.setpoint[3] and self.components[8] is True:   #Flavor hops check
        self.components[8] = False
        XGPIO.setGPIO(self.components)

    if time.time() >= self.setpoint[4] and self.components[9] is True:   #Aroma hops check
        self.components[9] = False
        XGPIO.setGPIO(self.components)

    if time.time() >= self.setpoint[5] and self.components[2] is False:   #Turns on Boiler Pump for Sanitization
        self.components[2] = True
        XGPIO.setGPIO(self.components)

    if time.time() >= self.setpoint[1]:
        self.state = False
        return self.state
    return self.state

phase = "Boil"
equipMent = [6]
starttime = time.time()
BoilTime = Recipe[4] + starttime
BitterTimer = BoilTime - Recipe[5]
FlavorTimer = BoilTime - Recipe[6]
AromaTimer = BoilTime - Recipe[7]
#SanTimer = BoilTime - 300
SanTimer = BoilTime - 5
heaterSignal = 66
tempmode = False

timerinfo = [starttime, BoilTime, BitterTimer, FlavorTimer, AromaTimer, SanTimer]
boil = Operation(endboil, equipMent, timerinfo, heaterSignal, tempmode, phase)

def endcool2ferm(self):
    if XPhidgets.temp9 <= self.setpoint:
        self.components[5] = False
        XGPIO.setGPIO(self.components)

phase = "Cool to Fermentation Temperature"
equipMent = [2, 5]
heaterSignal = 0
tempmode = True
fermtemp = Recipe[8]

boil = Operation(endcool2ferm, equipMent, fermtemp, heaterSignal, tempmode, phase)


