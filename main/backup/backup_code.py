def Control_loop():
    b = gpio.Button(6, pull_up=True)
    Control_Box(node_ip, 1, 1)
    while True:
        sleep(0.1)
        if b.is_pressed:
            print("PRESIONADO")
            Control_Box(node_ip, 0, 0)
            sleep(3)
            init_tello()
            while True:
                if b.is_pressed:
                    Control_Box(node_ip, 1, 1)
                    sleep(3)
                    break
        else:
                print("NO")

def Control_Box(node_ip, foco_state, camara_state):
    R1 = str(foco_state)
    R2 = '1'
    R3 = str(camara_state)
    R4 = '1'
    response = requests.get(
        str('http://'+node_ip+'/relay?R1='+R1+'&R2='+R2+'&R3='+R3+'&R4='+R4+'/'))
    print("Se ejecuto la peticion al arduino")
    if (foco_state == 1 and camara_state == 1): return
    sleep(1)


def init_tello():
    start_time = str(datetime.now())
    file_name = sys.argv[1]
    f = open(file_name, "r")
    commands = f.readlines()
    drone = tello.Tello('',8889)
    if drone:
        print("Tello inicializado")
        sleep(1)
    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()
            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print 'delay %s' % sec
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