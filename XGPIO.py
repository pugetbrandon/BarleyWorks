import RPi.GPIO as GPIO

# Component, list position, GPIO, pin
# Mashpump, 0, 1, 28
# Mashvalve, 1, 5, 29
# Boiler Pump, 2, 26, 37
# Boiler Valve, 3, 24, 18
# Ferm Valve, 4, 8, 24,
# Cooler Valve, 5, 7, 26
# Heater, 6, 3, 5




pins = (28, 29, 37, 18, 24, 26, 5, 32, 15, 22)
levelpins = (3, 35)  # Mash level is position 0, boiler level is position 1
#TODO put a comment with position number and components


def setup():
    GPIO.setmode(GPIO.BCM)
    global pins
    for i in range(10):
        GPIO.setup(pins(i), GPIO.OUT)
    for i in range(1):
        GPIO.setup(pins(i), GPIO.IN, pull_up_down=GPIO.PUD_UP)



def setGPIO(changeComp):

    components = []
    for i in range(7):
        print(i)
        components.append(False)
    for i in range(8, 10):
        components.append(True)

    for i in changeComp:
        components[i] = True

    for i in range(7):
        if components[i] is True:
            GPIO.output(pins(i), GPIO.HIGH)
        else:
            GPIO.output(pins(i), GPIO.LO)
    return components

def getlevel():
    global levelpins
    level = []
    level[0] = GPIO.input(levelpins(0))
    level[1] = GPIO.input(levelpins(1))
    return level