#!/usr/bin/python3

import serial
import time
import RPi.GPIO as gpio
import sys
import subprocess

# systemvar = sys.argv

# # LOG
# sendlog = "date '+%Y-%m-%d %T [INFO] - Receive: '" + systemvar[1] + "' '" + systemvar[2] + "' (serialMonitor.py)'" +">> /var/log/player.log"
# p = subprocess.check_output(sendlog,shell=True)

gpio.setwarnings(False)

gpio.setmode(gpio.BCM)

global mainport

mainport = True

# Sal_Chip = 17
# Sal_Mode = 18
# Sal_VelU = 27
# Sal_velD = 22

gpio.setup(17, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(27, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(23, gpio.IN)
gpio.setup(24, gpio.IN)


gpio.output(22, True)
gpio.output(27, True)
gpio.output(18, True)
gpio.output(17, True)

#____________________________Variables para la obtencion de datos K-1000
hex_list = []
chip_list = [0, 0]
chip_val = 0
chip_valA = 0
mode_list = [0, 0]
mode_val = 0
mode_valA = 0
velo_list = [0, 0]
velo_val = 0
velo_valA = 0

contador = 0


#____________________________Variables para el control de salida K-1000

global Tpc_chip
global Tpc_mode
global Tpc_velo

arduino = serial.Serial('/dev/ttyS0', baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout = 0.1)

Tcp_chip =  0
# Tcp_mode = int(systemvar[1])
# Tcp_velo = int(systemvar[2])

Tcp_mode = 1
Tcp_velo = 15

if(Tcp_mode >= 17):
    print("Modo no permitido por el controlador")
    Tcp_mode = 16
    
if(Tcp_mode <= 0):
    print("Modo no permitido por el controlador")
    Tcp_mode = 1
    
if(Tcp_velo >= 17):
    print("Velocidad superior a la permitida")
    Tcp_velo = 16
    
if(Tcp_velo <= 0):
    print("Velocidad inferior a la permitida")
    Tcp_velo = 1

print(f"Rcv mode: {Tcp_mode}")
print(f"Rcv velo: {Tcp_velo}")
print("waiting...")


def Serialcatch():
    
    t = arduino.readline()
    hex_val = t.hex()
    
    return hex_val


def ControlK(chip_val, mode_val, velo_val):
    
#     time.sleep(0.4)
    listTemp = [0, 0]
    listTemp1 = [0, 0]
    
    mode_Sal = False
    velo_Sal = False
    
    if(mode_val > 100):
        print("Error de lectura SD")
        mode_Sal = True
    elif(mode_val != Tcp_mode):
        cambMode = Tcp_mode - mode_val
        print(f"mode change: {cambMode}")
        
        if(cambMode > 0):
            for x in range(cambMode):
                print("cambMode")
                time.sleep(0.5)
                gpio.output(18, False)
                time.sleep(0.1)
                gpio.output(18, True)
                
                hex_valc = Serialcatch()
                listTemp[0] = hex_valc[6] + hex_valc[7]
                listTemp[1] = hex_valc[8] + hex_valc[9]
                tabla = tabladeCambio(listTemp[0], listTemp[1])
                print(f"mode_val: {Tcp_mode}")
                print(f"tabla: {tabla}")
                if(Tcp_mode == tabla):
                    mode_Sal = True
                    break
                else:
                    mode_Sal = False
                    
                print(f"mode_Sal: {mode_Sal}")
                    
                time.sleep(0.32)
                arduino.flushInput()
                
        else:
            for x in range(16 - abs(cambMode)):
#                 range(15 + cambMode):
#                 print(f"rango: {x}")
                time.sleep(0.5)
                gpio.output(18, False)
                time.sleep(0.1)
                gpio.output(18, True)

                hex_valc = Serialcatch()
                listTemp[0] = hex_valc[6] + hex_valc[7]
                listTemp[1] = hex_valc[8] + hex_valc[9]
                tabla = tabladeCambio(listTemp[0], listTemp[1])
#                 print(f"mode_val: {Tcp_mode}")
#                 print(f"tabla: {tabla}")
                if(Tcp_mode == tabla):
                    mode_Sal = True
                    break
                else:
                    mode_Sal = False
                    
                    
#                 print(f"mode_Sal: {mode_Sal}")

                time.sleep(0.32)
                arduino.flushInput()
                
    elif(mode_val == Tcp_mode):
            mode_Sal = True
    
    arduino.flushInput()
    
    if(velo_val > 100):
        print("Error de lectura SD")
        velo_val = Tcp_velo
    elif(velo_val > Tcp_velo):
        reduVelo = velo_val - Tcp_velo
        print(f"Vel change: -{reduVelo}")
        
        for x in range(reduVelo):
            time.sleep(0.5)
            gpio.output(22, False)
            time.sleep(0.1)
            gpio.output(22, True)
            
            hex_valc = Serialcatch()
#             print(hex_valc)
            listTemp1[0] = hex_valc[10] + hex_valc[11]
            listTemp1[1] = hex_valc[12] + hex_valc[13]
            tabla = tabladeCambio(listTemp1[0], listTemp1[1])
#             print(f"velo_val: {Tcp_velo}")
#             print(f"tabla: {tabla}")
            if(Tcp_velo == tabla):
                velo_Sal = True
            else:
                velo_Sal = False
                
#             print(f"velo_Sal: {velo_Sal}")
                
            time.sleep(0.32)
            arduino.flushInput()
            
    elif(velo_val < Tcp_velo):
        incrVelo = Tcp_velo - velo_val
        print(f"Vel change: {incrVelo}")
        
        for x in range(incrVelo):
            time.sleep(0.5)
            gpio.output(27, False)
            time.sleep(0.1)
            gpio.output(27, True)
            
            hex_valc = Serialcatch()
            listTemp[0] = hex_valc[10] + hex_valc[11]
            listTemp[1] = hex_valc[12] + hex_valc[13]
            tabla = tabladeCambio(listTemp[0], listTemp[1])
#             print(f"velo_val: {Tcp_velo}")
#             print(f"tabla: {tabla}")
            if(Tcp_velo == tabla):
                velo_Sal = True
            else:
                velo_Sal = False
                
#             print(f"velo_Sal: {velo_Sal}")
            
            time.sleep(0.32)
            arduino.flushInput()
            
    elif(velo_val == Tcp_velo):
        velo_Sal = True
    velo_val = Tcp_velo

#     print(f"mode_val: {Tcp_mode}")
#     print(f"velo_val: {Tcp_velo}")
#     
#     print(f"mode_verif: {mode_Sal}")
#     print(f"velo_verif: {velo_Sal}")
    
    if(mode_Sal == True and velo_Sal == True):
        return True
    else:
        return False


def tabladeCambio(cadena, cadenb):
    
    cheap = 0
    
    if ( cadena == '3f'):
        cheap = cheap + 0
    if (cadena == '06'):
        cheap = cheap + 10
    if (cadena == '5b'):
        cheap = cheap + 20
    if (cadena == '4f'):
        cheap = cheap + 30
    if (cadena == '66'):
        cheap = cheap + 40
    if (cadena == '6d'):
        cheap = cheap + 50
    if (cadena == '7d'):
        cheap = cheap + 60
    if (cadena == '07'):
        cheap = cheap + 70
    if (cadena == '7f'):
        cheap = cheap + 80
    if (cadena == '6f'):
        cheap = cheap + 90
        
    if ( cadenb == '3f'):
        cheap = cheap + 0
    if (cadenb == '06'):
        cheap = cheap + 1
    if (cadenb == '5b'):
        cheap = cheap + 2
    if (cadenb == '4f'):
        cheap = cheap + 3
    if (cadenb == '66'):
        cheap = cheap + 4
    if (cadenb == '6d'):
        cheap = cheap + 5
    if (cadenb == '7d'):
        cheap = cheap + 6
    if (cadenb == '07'):
        cheap = cheap + 7
    if (cadenb == '7f'):
        cheap = cheap + 8
    if (cadenb == '6f'):
        cheap = cheap + 9
    if (cadenb == '71'):
        cheap = cheap + 250
        
    return cheap


def extract():
    
    listTemp = [0, 0]

    pos1 = 2
    pos2 = 3
    pos3 = 4
    pos4 = 5
    listTemp[0] = hex_val[pos1] + hex_val[pos2]
    listTemp[1] = hex_val[pos3] + hex_val[pos4]
    chip_val = tabladeCambio(listTemp[0], listTemp[1])
    print(f"chip: {chip_val}")

    pos1 = 6
    pos2 = 7
    pos3 = 8
    pos4 = 9
    listTemp[0] = hex_val[pos1] + hex_val[pos2]
    listTemp[1] = hex_val[pos3] + hex_val[pos4]
    mode_val = tabladeCambio(listTemp[0], listTemp[1])
    print(f"mode: {mode_val}")

    pos1 = 10
    pos2 = 11
    pos3 = 12
    pos4 = 13
    listTemp[0] = hex_val[pos1] + hex_val[pos2]
    listTemp[1] = hex_val[pos3] + hex_val[pos4]
    velo_val = tabladeCambio(listTemp[0], listTemp[1])
    print(f"vel:  {velo_val}")
    
    return chip_val, mode_val, velo_val


def decodificar():

    
    if(len(hex_val) >= 18):
        
        finish1 = False
    
        chip_val, mode_val, velo_val = extract()
            

        finish1 = ControlK(chip_val, mode_val, velo_val) # finish1 = True
    else:
        print("Error de obtencion de datos")
        finish1 = False
        
    hex_list.clear()
    
    return finish1


while mainport == True:
    
    finish = False
    
    if(gpio.input(23) == True):
        
        print("Controlador encendido")
        
    else:
        
        print("Controlador apagado")
        time.sleep(2)
        mainport = False 
    
    time.sleep(0.5)
    gpio.output(18, False)
    time.sleep(0.08)
    gpio.output(18, True)
    
#     try:
        
#         s = arduino.readline()
#         hex_val = s.hex()

    hex_val = Serialcatch()
    
    if(hex_val[16] + hex_val[17] == '85'):
        print(f"Cadena recibida: {hex_val}")
        finish = decodificar()
        
#             print(f"Respuesta Deco: {finish}")
    
    if(finish == True):
        mainport = False
            
#     except IndexError:
        
#         print("No data")
#         mainport = False