import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_switch = 26  # select pin to connect button
GPIO.setup(GPIO_switch, GPIO.OUT, initial=GPIO.LOW)

try:
    for x in range(6):
        GPIO.output(GPIO_switch, GPIO.HIGH)
        time.sleep(0.09)
        GPIO.output(GPIO_switch, GPIO.LOW)
        time.sleep(0.09)



except KeyboardInterrupt:

    GPIO.cleanup()