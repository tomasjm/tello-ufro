import requests

'''
Función que recibe tres parametros, la dirección ip de la estación, el estado del foco y el estado de la cámara.
Estados de foco y cámara:
    Encendido -> 0
    Apagado -> 1

Ejemplos de llamado a la función.
    Encendido -> Control_Box(ip_address: string, 0, 0)
    Apagado -> Control_Box(ip_address: string, 1, 1)

La función tiene retorno nulo : void
'''

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