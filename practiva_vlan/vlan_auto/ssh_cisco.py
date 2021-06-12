from netmiko import ConnectHandler
from cisco_operaciones import *
from Vlan import *
import time, re, ipcalc


switches = ['192.168.1.11', '192.168.1.12', '192.168.1.13']
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
        desconectarse_ssh(conn)
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


def ver_vlans():
    #print("Buscando todas las vlan...")
    conn = conectarse_ssh(switches[0], 'admin', 'admin')
    vlans = []
    if conn != None:
        res = ejecutar_comando(conn, "sh running-config | section Vlan")
        #desconectarse_ssh(conn)
        res = re.sub(' +', ' ', res)
        res = re.sub('\n ', '\n', res).split('\n')
        i = 0
        res.remove('')
        numero = -1
        gateway = -1
        masc = -1
        for fila in res:
            if i % 2 == 0:
                #print("vlan id |{}|".format(re.sub('interface Vlan','', fila)))
                numero = re.sub('interface Vlan','', fila)
            else:
                gateway = fila.split(' ')[2]
                masc = fila.split(' ')[3]
                #print("gw: |{}| masc |{}|".format(gateway, masc))
                id_subred = obtener_subred(gateway, masc)
                #print("id subred: |{}|".format(id_subred))
                vlans.append(Vlan(numero, None, id_subred, masc, gateway))
            i += 1
        
        #obtener nombre de la vlan
        for vlan in vlans:
            nombre = ejecutar_comando(conn, 'sh vlan-s id {} | s active'.format(vlan.numero))
            nombre = re.sub(' +', ' ', nombre)
            nombre = re.sub(',', '', nombre).split(' ')
            #print(nombre[1])
            vlan.nombre = nombre[1]
        #for vlan in vlans:
        #    print(vlan)
        desconectarse_ssh(conn)
        #obtener interfaces asociadas a cada vlani
        count_switch = 0
        for switch in switches:
            print('obteniendo interfaces de cada vlan...')
            print("switch {}: obteniendo interfaces por vlan...".format(switch))
            conn = conectarse_ssh(switch, 'admin', 'admin')
            #obtener interfaces asociadas a cada vlan en el switch
            for vlan in vlans:
                ifaces = ejecutar_comando(conn, 'sh vlan-s id {} | s active'.format(vlan.numero))
                ifaces = re.sub(' +', ' ', ifaces)
                ifaces = re.sub(',', '', ifaces).split(' ')
                ifaces2vlan = []
                for i in range(3, len(ifaces)):
                    if "Fa" in ifaces[i]:
                        ifaces2vlan.append(ifaces[i])
                #print("INTERFACES DE VLAN {}: {}".format(vlan.numero, ifaces2vlan))
                vlan.ifaces[count_switch] = ifaces2vlan
                #for ifa in ifaces2vlan:
                    #print("agregando la {} del switch{} a la vlan {}".format(ifa, count_switch+1, vlan.numero))
                    #vlan.ifaces[count_switch].append(ifa)
                #print(vlan.ifaces)
                #print(vlan)
            count_switch += 1
            desconectarse_ssh(conn)
        for vlan in vlans:
            print(vlan)
            vlan.arr2str()
            print(vlan.ifaces_str)
    return vlans


def obtener_subred(ip_address, masc):
    addr = ipcalc.IP(ip_address, mask = '{}'.format(masc))
    net_with_cidr = str(addr.guess_network())
    return net_with_cidr.split('/')[0]


#para eliminar realmente la subinterface se tiene que hacer un reboot al router
def eliminar_vlan(numero):
    print("eliminando vlan...")
    conn = conectarse_ssh(switches[0], 'admin', 'admin')
    if conn != None:
        print("conexion al switch server exitosa...")
        
        res = ejecutar_comando(conn, "sh running-config | section Vlan{}".format(numero))
        res = re.sub(' +', ' ', res)
        res = re.sub('\n ', '\n', res).split('\n')
        
        gateway = None
        masc = None
        while len(res) != 3:
            if len(res) == 1:
                print("no existe la vlan")
                desconectarse_ssh(conn)
                return

            res = ejecutar_comando(conn, "sh running-config | section Vlan{}".format(numero))
            res = re.sub(' +', ' ', res)
            res = re.sub('\n ', '\n', res).split('\n')

        gateway = res[2].split(' ')[2]
        masc = res[2].split(' ')[3]
        print("gateway de vlan |{}|{}|".format(gateway, masc))
        
        desconectarse_ssh(conn)
        #eliminar subinterface router
        conn = conectarse_ssh(router, 'admin', 'admin')
        if conn != None:
            print("Eliminando subinterfaz de vlan en el router...")
            comandos = ["no int fa 0/0.{}".format(numero)]
            ejecutarComando_config(conn, comandos)
            print("subinterface fa 0/0.{} eliminada".format(numero))
            desconectarse_ssh(conn)

        for switch in switches:
            print("switch {}: quitando interfaces relacionadas a la vlan...".format(switch))
            conn = conectarse_ssh(switch, 'admin', 'admin')
            #obtener interfaces asociadas a la vlan en el switch
            ifaces = ejecutar_comando(conn, 'sh vlan-s id {} | s active'.format(numero))
            ifaces = re.sub(' +', ' ', ifaces)
            ifaces = re.sub(',', '', ifaces).split(' ')

            #print("ifaces: |{}| {}".format(ifaces, len(ifaces)))
            ifaces2rm = [] 
            for i in range(3, len(ifaces)):
                if "Fa" in ifaces[i]:
                    ifaces2rm.append(ifaces[i])
            print(ifaces2rm)
            if len(ifaces2rm) > 0:
                if switch == switches[0]:
                    #pasar interfaces de vlan n a la vlan 1 (default)
                    comandos = ['int vlan {}'.format(numero), "no ip add {} {}".format(gateway, masc), 'exit', 'no int vlan {}'.format(numero)]
                    ejecutarComando_config(conn, comandos)
                #pasar interfaces de vlan # a la vlan 1 (default)
                for iface in ifaces2rm:
                        comandos = ['int {}'.format(iface), "switchport access vlan 1"]
                        ejecutarComando_config(conn, comandos)

                if switch == switches[0]:
                    #Eliminar vlan de database
                    comandos = ['vlan database', 'no vlan {}'.format(numero), 'apply', 'exit', 'wr']
                    for comando in comandos:
                        res = ejecutar_comando(conn, comando)
                        print(res)
            desconectarse_ssh(conn)
    else:
        print("error al eliminar vlan")
