from netmiko import ConnectHandler
from cisco_operaciones import *
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
        print("error al conectarse via ssh a ", ip)
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
        #crear vlans
        for comando in comandos:
            print("ejecutando {} ...".format(comando))
            res = ejecutar_comando(conn, comando)
            print(res)
        
        #asignar gateway a las vlans
        asignar_gateway(conn, numero, id_subred, masc_subred)

        #revisar se se tiene que cambiar alguna interfaz de sw1
        if len(interfaces[0]) > 0:
            print("cambiar al menos 1 fa de sw1")
            cambiar_interfaces(conn, interfaces[0], numero)
        desconectarse_ssh(conn)
    
    else:
        print("error al crear vlan")
    #conexion al sw2
    if len(interfaces[1]) > 0:
        conn = conectarse_ssh(switches[1], 'admin', 'admin')
        if conn != None:
            print("conexion al switch client exitosa...")
            cambiar_interfaces(conn, interfaces[1], numero)
            desconectarse_ssh(conn)

    #conexion al sw3
    if len(interfaces[2]) > 0:
        conn = conectarse_ssh(switches[2], 'admin', 'admin')
        if conn != None:
            print("conexion al switch client exitosa...")
            cambiar_interfaces(conn, interfaces[2], numero)
            desconectarse_ssh(conn)
    
    #configurar subinterfaz de la vlan
    conn = conectarse_ssh(router, 'admin', 'admin')
    if conn != None:
        print("COnfigurando subinterface...")
        configurar_subinterface(conn, numero, id_subred, masc_subred)

    print("vlan agregada exitosamente")

def cambiar_interfaces(conn, interfaces, vlan):
    print("cambio")
    for interfaz in interfaces:
        comandos = ['interface fa {}'.format(interfaz), 'switchport access vlan {}'.format(vlan)]
        ejecutarComando_config(conn, comandos)
        print("interfaz {} agregada a vlan {}".format(interfaz, vlan))

def asignar_gateway(conn, vlan, subred, mascara):
    net = ipaddress.ip_network("{}/{}".format(subred, mascara))
    comandos = ['interface vlan {}'.format(vlan), 'ip add {} {}'.format(list(net.hosts())[0], str(net.netmask))]
    #print(comandos)
    ejecutarComando_config(conn, comandos)

def configurar_subinterface(conn, vlan, subred, mascara):
    net = ipaddress.ip_network("{}/{}".format(subred, mascara))
    comandos = ['interface fa 0/0.{}'.format(vlan), 'encapsulation dot1Q {}'.format(vlan),'ip add {} {}'.format(list(net.hosts())[0], str(net.netmask)), 'no shut']
    #print(comandos)
    ejecutarComando_config(conn, comandos)


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
