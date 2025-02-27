import pyudev
import os
from shutil import copyfile, ignore_patterns
import time
from subprocess import call

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

dest = '/home/pi/Desktop/video/'
oldfiles = os.listdir(dest)
        

for device in iter(monitor.poll, None):
    if device.action == 'add':
        print('{} connected', format(device))
        
        time.sleep(10)
        
        source = '/media/pi/USB_VIDEO/'
        newfiles = os.listdir(source)

        for file in oldfiles:
            if file.endswith(('ANI', 'mp4', 'MU3', 'MOV')):
                print('Delete: ' + file)
                os.remove(dest + file)


        for file in newfiles:
            if file.endswith(('ANI', 'mp4', 'MU3', 'MOV')):
                video = file
                print('Copy: ' + file)
                copyfile(source + file, dest + file)
                

        call("sudo reboot -h now", shell=True)

