import RPI.GPIO as GPIO

levelpins = (3, 35)
GPIO.setmode(GPIO.BCM)

for i in range(1):
    GPIO.setup(levelpins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print(i)

GPIO.add_event_detect(levelpins[0], GPIO.RISING)
GPIO.add_event_detect(levelpins[1], GPIO.FALLING)
state2 = True
while state2:
    if GPIO.event_detected(levelpins[0]) or GPIO.event_detected(levelpins[1]):
        state2 = False