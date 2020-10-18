import tello_test as tello
import sys
from datetime import datetime
import time
import requests
from time import sleep
import threading
import os
import ffmpeg

def Start_streaming_to_server():
    ffmpeg.input('udp:192.168.10.1:11111?overrun_nonfatal=1&fifo_size=50000000').output('rtmp://localhost/live/STREAM_NAME', format='flv',vcodec='libx264').run() # cambiar ip por el servidor

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
                drone.send_command(command)

    log = drone.get_log()
    out = open('log/' + start_time + '.txt', 'w')
    for stat in log:
        stat.print_stats()
        strr = stat.return_stats()
        out.write(strr)

tello_stream_thread = threading.Thread(target=Start_streaming_to_server)

def main():
    tello_stream_thread.start()
    print("streaming server started?")
    sleep(10)
    init_tello()
    os.system("sudo pkill -f ffmpeg") #kill ffmpeg process TODOS LOS FFMPEG CUIDADO CON LOS OTROS STREAMS

if __name__ == "__main__":
    main()

