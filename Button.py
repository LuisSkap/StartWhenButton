import RPi.GPIO as GPIO
import time
import subprocess, os
import signal

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_switch = 21 # select pin to connect button
GPIO.setup(GPIO_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO_LED = 20  # select pin to connect led
GPIO.setup(GPIO_LED, GPIO.OUT, initial=GPIO.LOW)

def LED_s():
    
    for x in range(6):
        GPIO.output(GPIO_LED, GPIO.HIGH)
        time.sleep(0.09)
        GPIO.output(GPIO_LED, GPIO.LOW)
        time.sleep(0.09)

try:

    run = 0
    
    while True:
        
        if GPIO.input(GPIO_switch)==0 and run == 0:
        
            LED_s()
            print("Button")
            run=1
            rpistr = "python3 /home/pi/Documentos/ControlK.py"
#             rpistr = "python3 /home/pi/Documentos/LED.py"
            p=subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid)
            time.sleep(10)
            LED_s()
            rpistr1 = "python3 /home/pi/Documentos/ControlK1.py"
#             rpistr1 = "python3 /home/pi/Documentos/LED.py"
            p=subprocess.Popen(rpistr1, shell=True, preexec_fn=os.setsid)
            
            while GPIO.input(GPIO_switch)==0:
                time.sleep(0.01)
                
                
        else:
            
            time.sleep(0.01)
            run=0


except KeyboardInterrupt:

    GPIO.cleanup()