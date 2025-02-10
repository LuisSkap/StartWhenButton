# StartWhenButton

Estas son las librerías y requerimientos para que corra el script.


Instalar librería pyserial para el manejo de comunicación serial vía el script de python
"sudo pip3 install pyserial"

Librerías nativas usadas en el script de python
"time"
"RPi.GPIO"
"sys"

Le damos permisos al puerto correspondiente serial para recibir los datos del controlador (pines 8 y 10 del GPIO)
"sudo chmod 666 /dev/ttyS0"

Activación del script:
mandamos llamar el script con los dos valores que vamos a controlar Mode(Efecto que se quiere mostrar, valores entre 1 y 15) y Speed(Velocidad del efecto, valores entre 1 y 16) separados por un espacio
python3 ./SerialMonitor.py 5 9

El script va a esperar recibir datos por el puerto serial (pin 10 del GPIO) y de acuerdo a estos va a tomar acción.
