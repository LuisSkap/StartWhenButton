#!/usr/bin/env python3
import os
import vlc
import time
from shutil import copyfile, ignore_patterns
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_switch = 21 # select pin to connect button
GPIO.setup(GPIO_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

run = 0


dest = '/home/pi/Desktop/video/'
oldfiles = os.listdir(dest)

vlc_instance = vlc.Instance("--no-xlib --quiet --fullscreen")

media_play = vlc_instance.media_player_new()

#media_play = vlc.MediaPlayer()

def play_video():

    #media_play.set_fullscreen(True)

    media = vlc.Media(dest + file)

    media_play.set_media(media)
    
    #media_play.set_mrl(media)
    
    media_play.set_fullscreen(True)

    # player.vlm_set_loop(dest + video, True)

    media_play.play()
    
    while media_play.get_state() != 6:
        time.sleep(0.1)

    print("Finish")
    
    
key = True

while key:

    for file in oldfiles:
        if file.endswith(('ANI', 'mp4', 'MU3', 'MOV')):
            print('Played video: ' + file)
            video = file
            play_video()
            
    if GPIO.input(GPIO_switch) == 0 and run == 0:
        media_play.stop()
        time.sleep(0.5)
        run = 1
        break
        
    elif GPIO.input(GPIO_switch) == 1 and run == 1:
        run = 0
                        
            
