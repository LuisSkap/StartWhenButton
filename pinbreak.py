import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_switch = 21 # select pin to connect button
GPIO.setup(GPIO_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

run = 0

while True:
    
    if GPIO.input(GPIO_switch) == 0 and run == 0:
        print("Hello")
        time.sleep(0.5)
        run = 1
        
    elif GPIO.input(GPIO_switch) == 1 and run == 1:
        run = 0
        
    