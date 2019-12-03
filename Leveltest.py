import RPi.GPIO as GPIO

levelpins = (19, 16)
GPIO.setmode(GPIO.BCM)

for i in range(2):
    GPIO.setup(levelpins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print(i)

GPIO.add_event_detect(levelpins[0], GPIO.RISING)
GPIO.add_event_detect(levelpins[1], GPIO.FALLING)
state2 = True
while state2:
    if GPIO.event_detected(levelpins[0]) or GPIO.event_detected(levelpins[1]):
        print('detected')
        state2 = False