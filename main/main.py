# Imports de librerías
import sys
from datetime import datetime
import time
import requests
from time import sleep
import threading
import os

# Imports locales de funciones útiles (helpers)
import helpers.tello as tello
from helpers.streams import Send_Central_Stream, Send_Tello_Stream
from helpers.box import Control_Box
from helpers.login import Login


# variables globales
node_ip = '192.168.8.150'
server_ip = "190.114.255.51"
token = ''
button_status = False
tello_is_streaming = False

# objetos globales
login_data = {
    "server_url": 'http://' + server_ip + ':3976/api/usuario/login',
    "email": "j.martinez09@ufromail.cl",
    "clave": "123456"
}

# Función que trata en comprobar el estado de inicialización de la central (ON-OFF)
def Control_loop():
    global button_status
    b = gpio.Button(6, pull_up=True)
    Control_Box(node_ip, 1, 1)
    while True:
        print("Boton en estado: " + str(button_status))
        if b.is_pressed:
            button_status = not button_status
            if button_status:
                Control_Box(node_ip, 0, 0)
            else:
                Control_Box(node_ip, 1, 1)
        sleep(0.5)

# Función que inicializa el objeto Tello, imprime stats y envia los comandos a la clase inicializada del vehiculo
def init_tello():
    start_time = str(datetime.now())
    file_name = sys.argv[1]
    f = open(file_name, "r")
    commands = f.readlines()
    drone = tello.Tello('',8889)
    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()
            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print ('delay ' + str(sec))
                time.sleep(sec)
                pass
            else:
                if (command == 'streamoff'):
                    tello_is_streaming = False
                drone.send_command(command)

    log = drone.get_log()
    out = open('log/' + start_time + '.txt', 'w')
    for stat in log:
        stat.print_stats()
        strr = stat.return_stats()
        out.write(strr)

# Inicialización de threads utilizados
tello_stream_thread = threading.Thread(target=Send_Tello_Stream) # Stream del drone
central_stream_thread = threading.Thread(target=Send_Central_Stream) # Stream de la central
bl_thread = threading.Thread(target=Control_loop, name='Button Loop') # Estado del botón de la central
tello_thread = threading.Thread(target=init_tello, name='Tello cmd thread') # Función que está encargada del control del vehiculo

# Función general de inicialización
def main():
    token = Login(login_data['server_url'],login_data['email'], login_data['clave'])
    if token == '':
        print("No se pudo obtener el token")
        return
    bl_thread.setDaemon()
    bl_thread.start()
    while True:
        global button_status
        print("Comprobando estado de la central...")
        if button_status:
            print("Inicializando thread cmd Tello...")
            tello_thread.setDaemon()
            tello_thread.start()
            print("Inicializando stream de la central...")
            central_stream_thread.setDaemon()
            central_stream_thread.start()
            break
        sleep(1) 
    while True:
        global tello_is_streaming
        print("Comprobando estado del streaming de Tello...")
        if tello_is_streaming:
            print("Inicializando thread stream Tello...")
            tello_stream_thread.setDaemon()
            tello_stream_thread.start()
            break
        sleep(1)
    while True:
        global tello_is_streaming
        if not tello_is_streaming:
            sleep(5)
            print("Enviando sudo pkill ffmpeg para terminar los streams")
            os.system("sudo pkill -f ffmpeg") #kill ffmpeg process TODOS LOS FFMPEG CUIDADO CON LOS OTROS STREAMS
            print("sudo pkill enviado")
    print("Fin de la ejecución")
    

if __name__ == "__main__":
    main()

