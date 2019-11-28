from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.TemperatureSensor import *

# from Phidget22.EnumerationType import *
from Phidget22.ThermocoupleType import *
from Phidget22.Devices.VoltageOutput import *
import multitimer
import time


import time
temp9 = 0

def onAttachHandler(self):

    ch2 = self
    ch2.setTemperatureChangeTrigger(1.0)
    ch2 .setThermocoupleType(ThermocoupleType.THERMOCOUPLE_TYPE_K)
    ch2.setDataInterval(4000)
    print("setTrigger")



def onTemperatureChangeHandler(self, temperature):

    print(temperature + 300)
    self.val = temperature * 9 / 5 + 32
    self.val = float(self.val)

    global temp9
    temp9 = self.val



def gettemp():
    global temp9
    ch2 = TemperatureSensor()
    ch2.setDeviceSerialNumber(118651)
    ch2.setChannel(0)
    ch2.setOnAttachHandler(onAttachHandler)

    #ch2.setOnTemperatureChangeHandler(onTemperatureChangeHandler)
    ch2.openWaitForAttachment(5000)
    temp9 = ch2.getTemperature() * 9 / 5 + 32
    temp8 = temp9
    #time.sleep(10)
    print(temp9)
    ch2.close()


    return temp8

def gettemp3():
    global temp9
    ch2 = TemperatureSensor()
    ch2.setDeviceSerialNumber(118651)
    ch2.setChannel(0)
    ch2.setOnAttachHandler(onAttachHandler)
    ch2.setOnTemperatureChangeHandler(onTemperatureChangeHandler)
    ch2.openWaitForAttachment(5000)
    return ch2
    #ch2.close()

def closetemp(self):
    ch2 = self
    ch2.close()
    print("closed")



def gettimedtemp():

    temptimer = multitimer.MultiTimer(1, gettemp, -1, runonstart=True)
    temptimer.start()


voltageOutput0 = VoltageOutput()  #keeps the voltage set after the function ends
def setheatersignal(heatersignal):
    global voltageOutput0
    voltageOutput0.openWaitForAttachment(5000)
    voltout = heatersignal / 100 * 5.0
    if voltout >= 0 and voltout <= 5.0:
        voltageOutput0.setVoltage(voltout)



def endheatersignal():
    voltageOutput0 = VoltageOutput()
    voltageOutput0.close()

# setheatersignal(50)
# print("second")
# time.sleep(10)
# endheatersignal()
# print("donego")
# time.sleep(10)
