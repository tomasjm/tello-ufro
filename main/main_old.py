import sys
from datetime import datetime
from time import sleep
import gpiozero as gpio
import threading
import os

# import de funciones locales
from login import Login 
from box import Control_Box
from streams import Send_Tello_Stream, Send_Central_Stream

# import de clases locales
import tello


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


# Lógica sobre el botón de la estación (button_status: bool) y el uso de la función Control_Box(ip_address, bool, bool)

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


def init_tello():
    global tello_is_streaming
    start_time = str(datetime.now())
    file_name = sys.argv[1]
    f = open(file_name, "r")
    commands = f.readlines()
    drone = tello.Tello('',8889)
    if drone:
        print("Tello inicializado")
        sleep(1)
        tello_is_streaming = True
    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()
            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print 'delay %s' % sec
                sleep(sec)
                pass
            else:
                drone.send_command(command)

def main():
    token = Login(login_data['server_url'],login_data['email'], login_data['clave'])
    if token == '':
        print("No se pudo obtener el token")
        return
    bl_thread = threading.Thread(target=Control_loop, name='Button Loop')
    bl_thread.setDaemon()
    bl_thread.start()
    while True:
        global button_status
        print("Comprobando estado de la central...")
        if button_status:
            print("Inicializando thread cmd Tello...")
            tello_thread = threading.Thread(target=init_tello, name='Tello cmd thread')
            tello_thread.setDaemon()
            tello_thread.start()
            break
        sleep(1)
    while True:
        global tello_is_streaming
        print("Comprobando estado del streaming de Tello...")
        if tello_is_streaming:
            print("Inicializando thread stream Tello...")
            tello_stream_thread = threading.Thread(target=Send_Tello_Stream, name='Tello stream thread')
            tello_stream_thread.setDaemon()
            tello_stream_thread.start()
            break
        sleep(1)

if __name__ == "__main__":
    main()
