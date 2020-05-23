import RPi.GPIO as GPIO


#modifyig ferm valve and boiler value due to failed motor on boiler valve
pins = (1, 5, 26, 8, 20, 7, 22, 16, 2, 25)   #Not actually Pins, GPIO
levelpins = (14, 23)  # Mash level is position 0, boiler level is position 1



Glevel = []
interlock = False

# def levelupdater_callback(channel):
#     global Glevel
#     Clevel = getlevel()
#     Glevel = [bool(Clevel[0]), bool(Clevel[1])]   #Glevel[0] is mash level   Glevel[1] is boiler level
#     print(Glevel, "levelupdatercallback")

# def interlock_callback(channel):
#     global pins
#     global interlock
#     level = getlevel()
#     print("interlock")
#     print(level[1])
#     if level[1] is False:
#         XPhidgets.setheatersignal(0)
#         GPIO.output(pins[6], GPIO.LOW)
#         interlock = True
#     if level[1] is True:
#         interlock = False



def setup():
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    global pins
    global levelpins
    for i in range(10):
        GPIO.setup(pins[i], GPIO.OUT)
    for i in range(2):
        GPIO.setup(levelpins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)


def setlevel_callback(callback):
    for i in range(2):
        GPIO.remove_event_detect(levelpins[i])
        GPIO.add_event_detect(levelpins[i], GPIO.BOTH, callback, bouncetime=200)

    print("XGPIO Callback set")
    #GPIO.add_event_callback(levelpins[1], interlock_callback)
    #GPIO.add_event_callback(levelpins[1], levelupdater_callback)
    #GPIO.add_event_detect(levelpins[0], GPIO.BOTH, callback, bouncetime=200)
    #GPIO.add_event_callback(levelpins[0], levelupdater_callback)


def buildcomponents(changeComp):
    global pins
    components = []
    for i in range(7):
        components.append(False)
    for i in range(7, 10):
        components.append(True)

    for i in changeComp:
        components[i] = True
    return components

def setGPIO(components):
     for i in range(10):
        if components[i] is True and i != 6:   # implements heater interlock with the boiler level
            GPIO.output(pins[i], GPIO.HIGH)
        elif components[i] is True and i == 6:
            ML, BL = getlevel()
            if BL:
                GPIO.output(pins[i], GPIO.HIGH)
            else:
                GPIO.output(pins[i], GPIO.LOW)
        else:
            GPIO.output(pins[i], GPIO.LOW)


# def setGPIO2(components):  #bypassses interlock
#     global pins
#     for i in range(10):
#         if components[i] is True:
#             GPIO.output(pins[i], GPIO.HIGH)
#         else:
#             GPIO.output(pins[i], GPIO.LOW)

def getlevel():
    global levelpins
    level = []
    level.append(GPIO.input(levelpins[0]))
    level.append(GPIO.input(levelpins[1]))
    return [bool(level[0]), bool(level[1])]



# def boilerlevel_callback():
#     global boilerlevel
#     boilerlevel = False

#
# def leveldetector():
#     global levelpins
#     GPIO.add_event_detect(levelpins[0], GPIO.FALLING, bouncetime=200)
#     GPIO.add_event_callback(levelpins[1], boilerlevel_callback)


if __name__ == "__main__":
    setup()


'''
setup()
changeComp = []
for i in range(10):
    changeComp.append(i)
    print(changeComp)
setGPIO(changeComp)
print("High")
time.sleep(10)

changeComp2 = []
setGPIO(changeComp2)
print('Low')
time.sleep(10)
GPIO.cleanup()

'''
