import RPi.GPIO as GPIO
import XPhidgets


pins = (1, 5, 26, 24, 8, 7, 22, 12, 2, 25)   #Not actually Pins, GPIO
levelpins = (19, 16)  # Mash level is position 0, boiler level is position 1
boilerlevel = True
#TODO put a comment with position number and components


def interlock_callback(channel):
    global pins
    level = getlevel()
    print("interlock")
    print(level[1])
    if level[1] == 0:
        print("false")
        XPhidgets.setheatersignal(0)
        GPIO.output(pins[6], GPIO.LOW)
        print("low")
        print(pins[6])


def setup():
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    global pins
    global levelpins
    for i in range(10):
        GPIO.setup(pins[i], GPIO.OUT)
    for i in range(2):
        GPIO.setup(levelpins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(levelpins[1], GPIO.FALLING, interlock_callback, bouncetime=200)
    GPIO.add_event_callback(levelpins[1], interlock_callback)





def setGPIO(changeComp):
    global pins
    components = []
    for i in range(7):
        components.append(False)
    for i in range(7, 10):
        components.append(True)

    for i in changeComp:
        components[i] = True

    for i in range(10):
        if components[i] is True and i != 6:   # implements heater interlock with the boiler level
            GPIO.output(pins[i], GPIO.HIGH)
        elif components[i] is True and i == 6:
            level = getlevel()
            if level[1]:
                GPIO.output(pins[i], GPIO.HIGH)
            else:
                components[i] = False
                XPhidgets.setheatersignal(0)
                GPIO.output(pins[i], GPIO.LOW)
        else:
            GPIO.output(pins[i], GPIO.LOW)
    return components

def setGPIO2(components):
    global pins
    for i in range(10):
        if components[i] is True:
            GPIO.output(pins[i], GPIO.HIGH)
        else:
            GPIO.output(pins[i], GPIO.LOW)

def getlevel():
    global levelpins
    level = []
    level.append(GPIO.input(levelpins[0]))
    level.append(GPIO.input(levelpins[1]))
    return level


def boilerlevel_callback():
    global boilerlevel
    boilerlevel = False


def leveldetector():
    global levelpins
    GPIO.add_event_detect(levelpins[0], GPIO.FALLING, bouncetime=200)
    GPIO.add_event_callback(levelpins[1], boilerlevel_callback)


if __name__ == "__main__":
    setup()
    level2 = getlevel()
    print(level2)

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
