import requests
'''
Función de Login al servidor streaming.
Tres parametros, url del servidor de autenticación y las credenciales (email, clave)
    url: string
    email: string
    clave: string
La función retorna un token: string para hacer peticiones al servidor
'''
def Login(url, email, clave):
    #obj = {'email': 'j.martinez09@ufromail.cl', 'clave': '123456'}
    obj = {'email': str(email), 'clave': str(clave)}
    #url_server_login = 'http://' + server_ip + ':3976/api/usuario/login'
    print("--------------------------------")
    print("Realizando petición de ingreso...")
    r = requests.post(url, json=obj)
    print(("Respuesta: " + r))
    response = r.json()
    token = response['token']
    if token:
        print("Token obtenido éxitosamente")
        return token
    return ''
    #Control_loop()