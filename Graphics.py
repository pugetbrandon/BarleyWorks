import pygame
import math
import pygbutton
import XPhidgets
import XGPIO

import time
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
lineSize = 5

degree = 0
degreeb = 0
x = []
y = []
mashpumpctr = (290, 346)
boilerpumpctr = (708, 440)
impeller_len = 13
angles = (0, 72, 144, 216, 288)
tlines = []

FPSCLOCK = pygame.time.Clock()

lineMaster = []
lineMaster.append([blue, [0, 0], [0, 0], 0])
lineMaster.append([blue, [266, 270], [266, 346], lineSize])
lineMaster.append([blue, [0, 0], [0, 0], 0])
lineMaster.append([blue, [266, 346], [288, 346], lineSize])
lineMaster.append([blue, [287, 330], [321, 330], lineSize])
lineMaster.append([blue, [350, 330], [368, 330], lineSize])
lineMaster.append([blue, [388, 349], [388, 424], lineSize])
lineMaster.append([blue, [388, 424], [189, 424], lineSize])
lineMaster.append([blue, [189, 424], [189, 67], lineSize])
lineMaster.append([blue, [189, 67], [278, 67], lineSize])
lineMaster.append([blue, [408, 330], [497, 330], lineSize])
lineMaster.append([blue, [587, 330], [587, 280], lineSize])
lineMaster.append([blue, [497, 330], [587, 330], lineSize])
lineMaster.append([blue, [732, 280], [732, 440], lineSize])
lineMaster.append([blue, [732, 440], [710, 440], lineSize])
lineMaster.append([blue, [710, 424], [672, 424], lineSize])
lineMaster.append([blue, [594, 424], [580, 424], lineSize])
lineMaster.append([blue, [541, 424], [517, 424], lineSize])
lineMaster.append([blue, [497, 330], [497, 405], lineSize])
lineMaster.append([blue, [441, 424], [479, 424], lineSize])
lineMaster.append([blue, [388, 424], [415, 424], lineSize])
lineMaster.append([blue, [561, 444], [561, 581], lineSize])
lineMaster.append([blue, [658, 440], [658, 489], lineSize])  #cooler
lineMaster.append([blue, [608, 440], [608, 489], lineSize])  #cooler

def changeGraphics(gameDisplay, component):
    global degree
    global degreeb
    tLines = []
    if component[0] is True and component[1] is False:
        tLines = [1, 3, 4, 5, 6, 7, 8, 9]

    if component[0] is True and component[1] is True: #and component[3] is False:
        tLines = [1, 3, 4, 5, 10, 11, 12]

    if component[2] is True and component[3] is False and component[4] is False:
        tLines = [11, 12, 13, 14, 15, 16, 17, 18]

    if component[2] is True and component[3] is True and component[4] is False and component[0] is False:
        tLines = [7, 8, 9, 13, 14, 15, 16, 17, 19, 20]

    if component[2] is True and component[3] is False and component[4] is True:
        tLines = [13, 14, 15, 16, 21, 22, 23]

    if component[0] is False and component[2] is False:
        tLines = []

    if component[2] is True and component[0] is True:
        tLines = [1, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20]


    for iLines in tLines:
        pygame.draw.line(gameDisplay, *lineMaster[iLines])

    if component[1] is True:   # draw mash valve
        pygame.draw.circle(gameDisplay, blue, [388, 330], 8)

    if component[3] is True:   #draw boiler valve
        pygame.draw.circle(gameDisplay, blue, [498, 424], 8)

    if component[4] is True:  # draw boiler valve
        pygame.draw.circle(gameDisplay, blue, [561, 424], 8)

    if component[5] is True:  # draw boiler valve
        pygame.draw.circle(gameDisplay, blue, [632, 423], 8)

    if component[6] is True and component[11] is True:  # draw boiler valve
        pygame.draw.circle(gameDisplay, blue, [642, 252], 8)

    if component[6] is True and component[11] is False:
        DefaultFont = None
        GameFont = pygame.font.Font(DefaultFont, 60)
        InterlockText = "Interlock"
        GameTempGraphic = GameFont.render(InterlockText, True, black)
        gameDisplay.blit(GameTempGraphic, (562, 145))

    if component[7] is True:  # draw bitter hopper
        pygame.draw.rect(gameDisplay, blue, [555, 76, 23, 19])

    if component[8] is True:  # draw flavor hopper
        pygame.draw.rect(gameDisplay, blue, [580, 76, 25, 19])

    if component[9] is True:  # draw aroma hopper
        pygame.draw.rect(gameDisplay, blue, [608, 76, 25, 19])

    if component[0] is True:
        for i in range(5):
            x = mashpumpctr[0] + math.cos(math.radians(degree + angles[i])) * impeller_len
            y = mashpumpctr[1] + math.sin(math.radians(degree + angles[i])) * impeller_len
            pygame.draw.line(gameDisplay, blue, mashpumpctr, [x, y], 1)
        degree += 5

    if component[2] is True:
        for i in range(5):
            xb = boilerpumpctr[0] + math.cos(math.radians(degreeb + angles[i])) * impeller_len
            yb = boilerpumpctr[1] + math.sin(math.radians(degreeb + angles[i])) * impeller_len
            pygame.draw.line(gameDisplay, blue, boilerpumpctr, [xb, yb], 1)

        degreeb -= 5

    if component[10] is False:  # draw mash level
        pygame.draw.circle(gameDisplay, blue, [287, 87], 8)


    if component[11] is True:  # draw boiler level
        pygame.draw.circle(gameDisplay, blue, [731, 237], 8)

def displaytemp(gameDisplay, temp):
    DefaultFont = None
    GameFont = pygame.font.Font(DefaultFont, 40)
    temp1 = format(temp, '.1f')
    GameText = str(temp1) + "F"
    GameTempGraphic = GameFont.render(GameText, True, black)
    gameDisplay.blit(GameTempGraphic, (465, 250))


def displayphase(gameDisplay, phase):
    DefaultFont = None
    GameFont = pygame.font.Font(DefaultFont, 40)
    PhaseTextGraphic = GameFont.render(phase, True, black)
    gameDisplay.blit(PhaseTextGraphic, (710, 36))

def displayheatersignal(gameDisplay, components, heatersignal):
    if components[11] is True:
        DefaultFont = None
        GameFont = pygame.font.Font(DefaultFont, 40)
        GameText = str(heatersignal) + "%"
        GamehtrSignalGraphic = GameFont.render(GameText, True, black)
        gameDisplay.blit(GamehtrSignalGraphic, (755, 270))

def makecontrolbutton(btitle):
    btncontrol = pygbutton.PygButton((35, 180, 140, 40), btitle)
    return btncontrol

def buttoncontrol(btncontrol, gameDisplay):  #single button controller

    btncontrol.draw(gameDisplay)
    for event in pygame.event.get():  # event handling loop
        if 'click' in btncontrol.handleEvent(event):
            state = False
            return state
    state = True
    return state

def makehtrctrlbtns():
    upheater = pygbutton.PygButton((825, 255, 100, 40), "Heater UP")
    downheater = pygbutton.PygButton((825, 300, 100, 40), "Heater Down")
    boilpwr = pygbutton.PygButton((825, 210, 100, 40), "66%")
    fullpwr = pygbutton.PygButton((825, 165, 100, 40), "100%")
    nopwr = pygbutton.PygButton((825, 345, 100, 40), "Zero")
    ctrlbtns = [upheater, downheater, boilpwr, fullpwr, nopwr]
    return ctrlbtns

def heaterctrlbuttons(heatctrlbtns, gameDisplay, heaterSignal):
    upheater = heatctrlbtns[0]
    downheater = heatctrlbtns[1]
    boilpwr = heatctrlbtns[2]
    fullpwr = heatctrlbtns[3]
    nopwr = heatctrlbtns[4]
    #
    upheater.draw(gameDisplay)
    downheater.draw(gameDisplay)
    boilpwr.draw(gameDisplay)
    fullpwr.draw(gameDisplay)
    nopwr.draw(gameDisplay)
    #
    for event in pygame.event.get():  # event handling loop
        if 'click' in upheater.handleEvent(event):
            heaterSignal += 1
            XPhidgets.setheatersignal(heaterSignal)
            return heaterSignal

        if 'click' in downheater.handleEvent(event):
            heaterSignal -= 1
            XPhidgets.setheatersignal(heaterSignal)
            return heaterSignal

        if 'click' in boilpwr.handleEvent(event):
            heaterSignal = 66
            XPhidgets.setheatersignal(heaterSignal)
            return heaterSignal

        if 'click' in fullpwr.handleEvent(event):
            heaterSignal = 100
            XPhidgets.setheatersignal(heaterSignal)
            return heaterSignal

        if 'click' in nopwr.handleEvent(event):
            heaterSignal = 0
            XPhidgets.setheatersignal(heaterSignal)
            return heaterSignal

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                heaterSignal += 1
                XPhidgets.setheatersignal(heaterSignal)
                return heaterSignal

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                heaterSignal -= 1
                XPhidgets.setheatersignal(heaterSignal)
                return heaterSignal
    return heaterSignal

def makecoolbuttons(bxy, btitles):
    buttons = []
    for i in range(2):
        buttons.append(pygbutton.PygButton((bxy[i][0], bxy[i][1], 60, 30), btitles[i]))
    return buttons

def checkcoolbuttons(buttons, gameDisplay, components):
    state = True
    for i in range(3):
        buttons[i].draw(gameDisplay)
    for event in pygame.event.get():  # event handling loop
        if 'click' in buttons[0].handleEvent(event):
            if components[2] is True:
                components[2] = False
            else:
                components[2] = True
            XGPIO.setGPIO(components)
        if 'click' in buttons[1].handleEvent(event):
            if components[5] is True:
                components[5] = False
            else:
                components[5] = True
            XGPIO.setGPIO(components)
        if 'click' in buttons[2].handleEvent(event):
            state = False
            return state
    return state








if __name__ == "__main__":
    bg = pygame.image.load("barleyworksbackground2.jpg")
    pygame.init()
    pygame.display.set_caption('Barley Works')
    gameExit = False
    clock = pygame.time.Clock()
    state = True
    while state:
                #   for event in pygame.event.get():
                #   state = check()   if event.type ==pygame.QUIT:
                #         gameExit = True


        gameDisplay = pygame.display.set_mode((1002, 672))
        #tempdisplay = displaytemp(100)

        gameDisplay.fill(white)
        gameDisplay.blit(bg, (0, 0))
        displaytemp(gameDisplay, 100)
        displayphase(gameDisplay, "Heat to Strike")
        displayheatersignal(gameDisplay, 50)
        #gameDisplay.blit(tempdisplay, (485, 250))
        changeGraphics(gameDisplay, [True, True, True, True, True, True, True, True, True, True])
        pygame.display.update()

        clock.tick(30)



