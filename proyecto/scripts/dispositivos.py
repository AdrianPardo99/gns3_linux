
# - ID Dispositivo 
# - Nombre 
# - Sistema operativo 
# - localización 
# - encargado 
# - contacto 
import get_snmp as g_snmp 
import levanta_snmp as lev_snmp
import json, re

def obtener_datos_dispositivo(ip_dispositivo):
    id_dispositivo = ""
    nombre_disp = ""
    nombre_os = ""
    encargado = ""
    contacto = ""
    lugar = ""

    #res = g_snmp.obtain_router_data(ip_dispositivo)
    res =  {'sysDescr': 'Cisco IOS Software, 7200 Software (C7200-A3JK9S-M), Version 12.4(25g), RELEASE SOFTWARE (fc1)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2012 by Cisco Systems, Inc.\r\nCompiled Wed 22-Aug-12 11:45 by prod_rel_team', 'sysContact': '', 'sysName': 'R3.la-pandilla-mantequilla', 'sysLocation': '', 'hostname': 'R3'}

    nombre_disp = res['sysName']
    #nombre_disp = res['hostname']
    id_dispositivo = res["hostname"][1:]
    nombre_os = re.sub(' +', ' ', res["sysDescr"])
    nombre_os = re.sub('\r+', ' ', nombre_os)
    nombre_os = re.sub('\n+', ' ', nombre_os)
    contacto = res["sysContact"]
    lugar = res["sysLocation"]
    #falta encargado 

    #print("id_disp:|{}| nombre_disp:|{}| nombre_os:|{}| encargado:|{}| contacto:|{}| lugar|{}|".format(id_dispositivo, nombre_disp, nombre_os, encargado, contacto, lugar))
    #print(g_snmp.obtain_router_data(ip_dispositivo))

    return (id_dispositivo, nombre_disp, nombre_os, encargado, contacto, lugar)
#
def obtener_paquetes_dispositivo(ip_interfaz_medido, ip_interfaz_conectada):
    #lev_snmp.init_configure("10.0.1.254")
    #init_configure()
    ip_int_1 = "10.0.2.1"
    ip_int_2 = "10.0.2.2"
    print(json.dumps(g_snmp.obtain_router_data("10.0.2.1"),indent=4))
    lost1, lost2 = g_snmp.get_interfaces(ip_int_1), g_snmp.get_interfaces(ip_int_2)
    print(json.dumps(lost1,indent=4))
    print(json.dumps(lost2,indent=4))
    lost1[3]["ip"]= ip_int_1
    lost2[1]["ip"]= ip_int_2
    print(g_snmp.check_lost_percentage(lost1[3],lost2[1],50))
    #retorna 4 cosas: 
    #(  T o F si el porcentaje de paquetes perdidos excede el que se pasa como ultimo param, 
    #   Porcentaje de paquetes perdidos 0 a 100:float
    #   Numero de paquetes enviados: string
    #   Numero de paquetes perdidos: int
    #)


print(obtener_datos_dispositivo("10.0.2.1"))

