from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.TemperatureSensor import *

# from Phidget22.EnumerationType import *
from Phidget22.ThermocoupleType import *
from Phidget22.Devices.VoltageOutput import *
import time


import time
temp9 = 0

def onAttachHandler(self):
    print("Phidget Attached!")
    ch = self
    ch.setTemperatureChangeTrigger(0.01)
    ch.setThermocoupleType(ThermocoupleType.THERMOCOUPLE_TYPE_K)
    ch.setDataInterval(1000)

def onTemperatureChangeHandler(self, temperature):
    print("Temperature changed ", temperature)
    self.val = temperature * 9 / 5 + 32
    self.val = float(self.val)
    print(self.val)
    global temp9
    temp9 = self.val

    return temperature

def gettemp():
    global temp9
    ch2 = TemperatureSensor()
    ch2.setDeviceSerialNumber(118651)
    ch2.setChannel(0)
    ch2.setOnAttachHandler(onAttachHandler)
    ch2.setOnTemperatureChangeHandler(onTemperatureChangeHandler)
    ch2.openWaitForAttachment(5000)
    temp9 = ch2.getTemperature() * 9 / 5 + 32
    temp8 = temp9
    #time.sleep(10)

    ch2.close()

    print("i got the temperature, its ", temp9)
    return temp8
voltageOutput0 = VoltageOutput()
def setheatersignal(heatersignal):
    global voltageOutput0
    voltageOutput0.openWaitForAttachment(5000)
    voltout = heatersignal / 100 * 5.0
    if voltout >= 0 and voltout <= 5.0:
        voltageOutput0.setVoltage(voltout)
    print("first")
    time.sleep(10)
    #voltageOutput0.close()
def endheatersignal():
    voltageOutput0 = VoltageOutput()
    voltageOutput0.close()

# setheatersignal(50)
# print("second")
# time.sleep(10)
# endheatersignal()
# print("donego")
# time.sleep(10)
