from netmiko import ConnectHandler
import time

switches = ['192.168.1.11', '10.10.1.12', '192.168.1.13']
router = '192.168.1.1'

def conectarse_ssh(ip, username, pwd):
    cisco_router = {
        'device_type': 'cisco_ios',
        'host':   ip,
        'username': username,
        'password': pwd
    }
    try:
        conn_session = ConnectHandler(**cisco_router, conn_timeout=5)
        conn_session.enable()
        return conn_session
    except Exception as e:
        print("error al conectarse viassh a ", ip)
    return None

def desconectarse_ssh(conn):
    try:
        conn.disconnect()
        print("Se ha desconectado ssh")
    except Exception as e:
        print("error al desconectar")

def ejecutar_comando(conn_session, comando):
    result = ""
    try:
        result = conn_session.send_command(comando)
        return result
    except Exception as e:
        result = "error al ejecutar el comando ssh: {}".format(comando)
    return None

def ejecutarComando_config(conn_session, comandos):
    try:
        result = conn_session.send_config_set(comandos)
        print(result)
        result = conn_session.save_config()
        print(result)
    except Exception as e:
        result = "error al ejecutar los comandos de configuracion ssh"
    return result

def ejecutar_comando_channel(conn_session, comando):
    result = ""
    try:
        conn_session.write_channel("\r{}\n".format(comando))
        time.sleep(0.1)
        result = conn_session.read_channel()
        return result
    except Exception as e:
        result = "error al ejecutar el comando ssh: {}".format(comando)
    return None


def crear_vlan(numero, nombre, id_subred, masc_subred, interfaces):
    print("creando vlan...")
    #conectarse al switch 1 y crear la vlan
    conn = conectarse_ssh(switches[0], 'admin', 'admin')
    if conn != None:
        print("conexion al switch server exitosa...")
        comandos = ['vlan database', 'vlan {} name {}'.format(numero, nombre), 'apply', 'exit' ]
        for comando in comandos:
            print("ejecutando {} ...".format(comando))
            res = ejecutar_comando(conn, comando)
            print(res)
        desconectarse_ssh(conn)
    else:
        print("error al crear vlan")

def eliminar_vlan(numero):
    print("eliminando vlan...")
    conn = conectarse_ssh(switches[0], 'admin', 'admin')
    if conn != None:
        print("conexion al switch server exitosa...")
        res = ejecutar_comando(conn, "sh vlan-s")
        print(res)
        # comandos = ['vlan database', 'vlan {} name {}'.format(numero, nombre), 'apply', 'exit' ]
        # for comando in comandos:
        #     res = ejecutar_comando(conn, comando)
        #     print(res)
        desconectarse_ssh(conn)
    else:
        print("error al eliminar vlan")
