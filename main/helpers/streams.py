import os
import ffmpeg
'''
Código para ejecutar streams mediante comandos de sistema.
Se hace uso de ffmpeg.

    Send_Central_Stream -> Le dice a ffmpeg que tome todos los chunks de la central y los envia al servidor
    Send_Tello_Stream -> Le dice a ffmpeg que tome todos los chunks del drone (tello) y los envia al servidor

Las funciones requieren de la dirección ip del servidor y el token de acceso
'''
def Send_Central_Stream(server_ip, token):
    #os.system("ffmpeg -i rtmp://192.168.8.160:1935/flash/11:admin:admin -c copy -r 1 -f flv \"rtmp://" + server_ip + ":1935/live/$camara1?token=" + token + "&movil=camion1\"")
    ffmpeg.input("rtmp://192.168.8.160:1935/flash/11:admin:admin").output("rtmp://" + server_ip + ":1935/live/$camara1?token=" + token + "&movil=camion1", format='flv',vcodec='libx264')
    .global_args("-timeout", "-1").run() # -timeout -1 (infinito)
    

def Send_Tello_Stream(server_ip, token):
    #os.system("ffmpeg -i udp:192.168.10.1:11111 -c copy -f flv \"rtmp://" + server_ip + ":1935/live/d1b4?token=" + token +"&movil=camion1\"")
    ffmpeg.input('udp:192.168.10.1:11111?overrun_nonfatal=1&fifo_size=50000000').output("rtmp://" + server_ip + ":1935/live/d1b4?token=" + token +"&movil=camion1", format='flv',vcodec='libx264')
    .global_args("-timeout", "-1")
    .run()

