


import scripts.get_snmp as g_snmp 
import scripts.levanta_snmp as lev_snmp
import scripts.set_snmp as s_snmp
import json, re


d0 = [{'hostname': 'R3', 'interfaces': [{'name': 'FastEthernet0/0', 'ip': '10.0.1.254', 'netmask': '255.255.255.0', 'idnet': '10.0.1.0/24'}, {'name': 'FastEthernet1/0', 'ip': '10.0.2.5', 'netmask': '255.255.255.252', 'idnet': '10.0.2.4/30'}, {'name': 'FastEthernet1/1', 'ip': '10.0.2.1', 'netmask': '255.255.255.252', 'idnet': '10.0.2.0/30'}, {'name': 'FastEthernet2/0', 'ip': '10.0.2.18', 'netmask': '255.255.255.252', 'idnet': '10.0.2.16/30'}, {'name': 'FastEthernet2/1', 'ip': '10.0.2.22', 'netmask': '255.255.255.252', 'idnet': '10.0.2.20/30'}]}, {'hostname': 'R5', 'interfaces': [{'name': 'FastEthernet0/0', 'ip': '10.0.5.254', 'netmask': '255.255.255.252', 'idnet': '10.0.5.252/30'}, {'name': 'FastEthernet1/0', 'ip': '10.0.2.6', 'netmask': '255.255.255.252', 'idnet': '10.0.2.4/30'}, {'name': 'FastEthernet1/1', 'ip': '10.0.2.13', 'netmask': '255.255.255.252', 'idnet': '10.0.2.12/30'}]}, {'hostname': 'R2', 'interfaces': [{'name': 'FastEthernet0/0', 'ip': '10.0.3.254', 'netmask': '255.255.255.252', 'idnet': '10.0.3.252/30'}, {'name': 'FastEthernet1/0', 'ip': '10.0.2.9', 'netmask': '255.255.255.252', 'idnet': '10.0.2.8/30'}, {'name': 'FastEthernet1/1', 'ip': '10.0.2.2', 'netmask': '255.255.255.252', 'idnet': '10.0.2.0/30'}]}, {'hostname': 'R1', 'interfaces': [{'name': 'FastEthernet0/0', 'ip': '10.0.4.254', 'netmask': '255.255.255.252', 'idnet': '10.0.4.252/30'}, {'name': 'FastEthernet1/0', 'ip': '10.0.2.10', 'netmask': '255.255.255.252', 'idnet': '10.0.2.8/30'}, {'name': 'FastEthernet2/0', 'ip': '10.0.2.17', 'netmask': '255.255.255.252', 'idnet': '10.0.2.16/30'}]}, {'hostname': 'R4', 'interfaces': [{'name': 'FastEthernet0/0', 'ip': '10.0.6.254', 'netmask': '255.255.255.252', 'idnet': '10.0.6.252/30'}, {'name': 'FastEthernet1/1', 'ip': '10.0.2.14', 'netmask': '255.255.255.252', 'idnet': '10.0.2.12/30'}, {'name': 'FastEthernet2/1', 'ip': '10.0.2.21', 'netmask': '255.255.255.252', 'idnet': '10.0.2.20/30'}]}]
d1 =['R3-R5:10.0.2.4', 'R3-R2:10.0.2.0', 'R3-R1:10.0.2.16', 'R3-R4:10.0.2.20', 'R2-R1:10.0.2.8']
d2 = {'R3': {'FastEthernet0/0': '10.0.1.254/24', 'FastEthernet1/0': '10.0.2.5/30', 'FastEthernet1/1': '10.0.2.1/30', 'FastEthernet2/0': '10.0.2.18/30', 'FastEthernet2/1': '10.0.2.22/30'}, 'R5': {'FastEthernet0/0': '10.0.5.254/30', 'FastEthernet1/0': '10.0.2.6/30', 'FastEthernet1/1': '10.0.2.13/30'}, 'R2': {'FastEthernet0/0': '10.0.3.254/30', 'FastEthernet1/0': '10.0.2.9/30', 'FastEthernet1/1': '10.0.2.2/30'}, 'R1': {'FastEthernet0/0': '10.0.4.254/30', 'FastEthernet1/0': '10.0.2.10/30', 'FastEthernet2/0': '10.0.2.17/30'}, 'R4': {'FastEthernet0/0': '10.0.6.254/30', 'FastEthernet1/1': '10.0.2.14/30', 'FastEthernet2/1': '10.0.2.21/30'}}

d3 = [{'10.0.1.1': 'Unix-OS 0'}, {'10.0.1.2': 'Unix-OS 0'}, {'10.0.1.254': 'Cisco_Router_IOS 0'}, {'10.0.2.5': 'Cisco_Router_IOS 0'}, {'10.0.2.6': 'Cisco_Router_IOS 1'}, {'10.0.2.1': 'Cisco_Router_IOS 0'}, {'10.0.2.2': 'Cisco_Router_IOS 1'}, {'10.0.2.17': 'Cisco_Router_IOS 1'}, {'10.0.2.18': 'Cisco_Router_IOS 0'}, {'10.0.2.22': 'Cisco_Router_IOS 0'}, {'10.0.2.21': 'Cisco_Router_IOS 1'}, {'10.0.5.254': 'Cisco_Router_IOS 1'}, {'10.0.5.253': 'Unix-OS 2'}, {'10.0.2.14': 'Cisco_Router_IOS 1'}, {'10.0.3.254': 'Cisco_Router_IOS 1'}, {'10.0.3.253': 'Unix-OS 2'}, {'10.0.2.9': 'Cisco_Router_IOS 1'}, {'10.0.2.10': 'Cisco_Router_IOS 1'}, {'10.0.4.254': 'Cisco_Router_IOS 1'}, {'10.0.4.253': 'Unix-OS 2'}, {'10.0.2.10': 'Cisco_Router_IOS 1'}, {'10.0.2.9': 'Cisco_Router_IOS 1'}, {'10.0.6.254': 'Cisco_Router_IOS 1'}, {'10.0.2.14': 'Cisco_Router_IOS 1'}]

d4 = [{'ip_1': '10.0.2.6', 'interface_1': 'FastEthernet1/0', 'host_1': 'R5', 'ip_2': '10.0.2.5', 'interface_2': 'FastEthernet1/0', 'host_2': 'R3'}, {'ip_1': '10.0.2.2', 'interface_1': 'FastEthernet1/1', 'host_1': 'R2', 'ip_2': '10.0.2.1', 'interface_2': 'FastEthernet1/1', 'host_2': 'R3'}, {'ip_1': '10.0.2.17', 'interface_1': 'FastEthernet2/0', 'host_1': 'R1', 'ip_2': '10.0.2.18', 'interface_2': 'FastEthernet2/0', 'host_2': 'R3'}, {'ip_1': '10.0.2.21', 'interface_1': 'FastEthernet2/1', 'host_1': 'R4', 'ip_2': '10.0.2.22', 'interface_2': 'FastEthernet2/1', 'host_2': 'R3'}, {'ip_1': '10.0.2.10', 'interface_1': 'FastEthernet1/0', 'host_1': 'R1', 'ip_2': '10.0.2.9', 'interface_2': 'FastEthernet1/0', 'host_2': 'R2'}]

d5 = '10.0.1.254'


def actualizar_datos_dispositivo(conexiones, nombre, localizacion, contacto, os): #nombre, locali, contac, sistem
    host = ""
    for c in conexiones:
        print(c)
        host = c
        break
    print("cambiando informacion de nombre...")
    s_snmp.set_information(0,host, nombre)
    print("cambiando informacion de os...")
    #s_snmp.set_information(1,host, os)
    print("cambiando informacion de contacto...")
    s_snmp.set_information(2,host, contacto)
    print("cambiando informacion de localizacion...")
    s_snmp.set_information(3,host, localizacion)
    print("informacion cambiada...")

def obtener_datos_inciales_dispositivos(datos):
	res = []
	for dispositivo in datos:
		hostname = dispositivo["hostname"]
		ip_int = dispositivo["interfaces"][0]["ip"]
		res.append([hostname, ip_int])
	return res

def obtener_conexiones_dispositivo(nombre_disp, conexiones_dic):
    conexiones = {}

    for con in conexiones_dic:
        if con['host_1'] == nombre_disp:
            conexiones[con['ip_1']] = con['ip_2']
        elif con['host_2'] == nombre_disp:
            conexiones[con['ip_2']] = con['ip_1']
    return conexiones

#Retorna:
# - ID Dispositivo 
# - Nombre 
# - Sistema operativo 
# - localización 
# - encargado 
# - contacto 
def obtener_datos_dispositivo(ip_dispositivo):
    id_dispositivo = ""
    nombre_disp = ""
    nombre_os = ""
    contacto = ""
    lugar = ""

    res = g_snmp.obtain_router_data(ip_dispositivo)
    #res =  {'sysDescr': 'Cisco IOS Software, 7200 Software (C7200-A3JK9S-M), Version 12.4(25g), RELEASE SOFTWARE (fc1)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2012 by Cisco Systems, Inc.\r\nCompiled Wed 22-Aug-12 11:45 by prod_rel_team', 'sysContact': '', 'sysName': 'R3.la-pandilla-mantequilla', 'sysLocation': '', 'hostname': 'R3'}

    nombre_disp = res['hostname']
    #nombre_disp = res['sysName']
    id_dispositivo = res["hostname"][1:]
    nombre_os = re.sub(' +', ' ', res["sysDescr"])
    nombre_os = re.sub('\r+', ' ', nombre_os)
    nombre_os = re.sub('\n+', ' ', nombre_os)
    contacto = res["sysContact"]
    lugar = res["sysLocation"]

    return [id_dispositivo, nombre_disp, nombre_os, contacto, lugar]


#ip de alguna interfaz del dispositivo a obtener paquetes
#obtenemos la ip de la interfaz con la cual se conecta el router que queremos sacar sus paquetes perdidos.
#obtenemos el numero de paquetes enviados en las conexiones del dispositivo
#calculamos promedio de perdida, numero total de paquetes enviados y recibidos
    #numero total de paquetes enviados: suma de paquetes de salida de todas las interfaces del dispositivo a medir
    #numero total de paquetes recibidos: suma de paquetes de entrada en cada interfaz
def obtener_paquetes_dispositivo(conexiones):
    #lev_snmp.init_configure("10.0.1.254")
    total_paquetes_enviados = 0
    total_paquetes_perdidos = 0
    i = 0
    for conexion in conexiones:
        ip_int_1 = conexion
        ip_int_2 = conexiones[conexion]
        print(ip_int_1," a ", ip_int_2)
        lost1, lost2 = g_snmp.get_interfaces(ip_int_1), g_snmp.get_interfaces(ip_int_2)
        lost1[3]["ip"]= ip_int_1
        lost2[1]["ip"]= ip_int_2
        snmp_res = g_snmp.check_lost_percentage(lost1[3],lost2[1], 50)
        print(int(snmp_res[2]))
        print(int(snmp_res[3]))
        if(int(snmp_res[2]) != 0 and int(snmp_res[3])):
            total_paquetes_enviados += int(snmp_res[2])
            total_paquetes_perdidos += int(snmp_res[3])
        i += 1
    
    print("Paquetes enviados:", total_paquetes_enviados)
    print("Paquetes recibidos:", total_paquetes_perdidos)
    if total_paquetes_enviados == 0:
        total_paquetes_enviados +=1
    print("%", ((total_paquetes_enviados-total_paquetes_perdidos)/total_paquetes_enviados)*100, "paquetes perdidos" )
    return total_paquetes_enviados, total_paquetes_perdidos
        
    # print(json.dumps(g_snmp.obtain_router_data("10.0.2.1"),indent=4))
    # lost1, lost2 = g_snmp.get_interfaces(ip_int_1), g_snmp.get_interfaces(ip_int_2)
    # print(json.dumps(lost1,indent=4))
    # print(json.dumps(lost2,indent=4))
    # lost1[3]["ip"]= ip_int_1
    # lost2[1]["ip"]= ip_int_2
    # print(g_snmp.check_lost_percentage(lost1[3],lost2[1],50))
    #retorna 4 cosas: 
    #(  T o F si el porcentaje de paquetes perdidos excede el que se pasa como ultimo param, 
    #   Porcentaje de paquetes perdidos 0 a 100:float
    #   Numero de paquetes enviados: string
    #   Numero de paquetes perdidos: int
    #)

#lev_snmp.init_configure("10.0.1.254")
# print(obtener_datos_dispositivo("10.0.2.1"))
# print("conexions del router 3 con los demas routers", obtener_conexiones_dispositivo('R3', d4))

# datos_dispositivo = obtener_datos_dispositivo("10.0.2.1")
# nom_disp = datos_dispositivo[1]
# conexiones = obtener_conexiones_dispositivo(nom_disp, d4)
# paquetes,dos = obtener_paquetes_dispositivo(conexiones)

#5253 3608