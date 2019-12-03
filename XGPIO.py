import RPi.GPIO as GPIO


# Component, list position, GPIO, pin
# Mashpump, 0, 1, 28
# Mashvalve, 1, 5, 29
# Boiler Pump, 2, 26, 37
# Boiler Valve, 3, 24, 18
# Ferm Valve, 4, 8, 24,
# Cooler Valve, 5, 7, 26
# Heater, 6, 3, 5




pins = (1, 5, 26, 24, 8, 7, 22, 12, 2, 25)   #Not actually Pins, GPIO
levelpins = (19, 16)  # Mash level is position 0, boiler level is position 1
#TODO put a comment with position number and components


def setup():
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    global pins
    global levelpins
    for i in range(10):
        GPIO.setup(pins[i], GPIO.OUT)
    for i in range(2):
        GPIO.setup(levelpins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

def setuplevel():
    for i in range(2):
        GPIO.setup(levelpins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)



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
        if components[i] is True:
            GPIO.output(pins[i], GPIO.HIGH)
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

def levelmonitor():
    for i in range(1):
        GPIO.add_event_detect(levelpins[i], GPIO.RISING)

def leveldetector():
    global levelpins
    GPIO.add_event_detect(levelpins[0], GPIO.RISING)
    GPIO.add_event_detect(levelpins[1], GPIO.FALLING)


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
