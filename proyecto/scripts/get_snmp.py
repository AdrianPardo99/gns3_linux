#!/usr/bin/env python3
from pysnmp.hlapi import *
import json

HOSTNAME_OID = "1.3.6.1.2.1.1.5.0"
DESCR_OID = "1.3.6.1.2.1.1.1.0"
CONTACT_OID = "1.3.6.1.2.1.1.4.0"
LOCATION_OID = "1.3.6.1.2.1.1.6.0"
INTERFACE_OID = "1.3.6.1.2.1.2.2.1"
INTNUMBER_OID = "1.3.6.1.2.1.2.1.0"
user='admin'
password='administrador_snmp'
community="REDES"
"""
    Verifica status de la interfaz de red
"""
def status(status):
    try:
        status = int(str(status))
        if status == 1:
            return "up"
        if status == 2:
            return "down"
        if status == 3:
            return "testing"
        return "unknown"
    except:
        return "unknown"

"""
    Realiza un split del string que recibe para que la presentacion este bonito
"""
def mac(raw_str):
    return ":".join("{:02x}".format(ord(c)) for c in raw_str)

"""
    Modifica la salida de la interfaz de red
"""
def translate_to_flask(interface_name):
    return interface_name.replace("/", "/")

"""
    Obtiene la informacion de un router a partir de su direccion ip
"""
def obtain_router_data(host):
    info = {
        "sysDescr": snmp_query(host, DESCR_OID),
        "sysContact": snmp_query(host, CONTACT_OID),
        "sysName": snmp_query(host, HOSTNAME_OID),
        "sysLocation": snmp_query(host, LOCATION_OID),
    }
    info["hostname"] = info["sysName"].split(".")[0]
    return info

"""
    Verifica los octetos de entrada y salida que tiene en una interfaz
    asi como los paquetes de entrada y salida
"""
def get_if_inout(ip, n):
    return {
        "ifInOctets": snmp_query(ip, f"{INTERFACE_OID}.10.{n}"),
        "ifOutOctets": snmp_query(ip, f"{INTERFACE_OID}.16.{n}"),
        "ifInUcastPkts": snmp_query(ip, f"{INTERFACE_OID}.11.{n}"),
        "ifInNUcastPkts": snmp_query(ip, f"1.3.6.1.2.1.2.2.1.12.{n}"),
        "ifOutUcastPkts": snmp_query(ip, f"1.3.6.1.2.1.2.2.1.17.{n}"),
        "ifOutNUcastPkts": snmp_query(ip, f"1.3.6.1.2.1.2.2.1.18.{n}"),
        "ifInErrors": snmp_query(ip, f"1.3.6.1.2.1.2.2.1.14.{n}"),
        
    }

"""
    Obtiene la informacion acerca de una interfaz de red
"""
def get_if_info(ip, n):
    return {
        "ifDescr": translate_to_flask(
            snmp_query(ip, f"{INTERFACE_OID}.2.{n}")
        ),
        "ifMtu": snmp_query(ip, f"{INTERFACE_OID}.4.{n}"),
        "ifSpeed": snmp_query(ip, f"{INTERFACE_OID}.5.{n}"),
        "ifPhysAddress": mac(
            snmp_query(ip, f"{INTERFACE_OID}.6.{n}")
        ),
        "ifAdminStatus": status(
            snmp_query(ip, f"{INTERFACE_OID}.7.{n}")
        ),
        "ifOperStatus": status(
            snmp_query(ip, f"{INTERFACE_OID}.8.{n}")
        ),
        "mibIndex": n,
    }

"""
    Obtiene el numero de interfaces que hay en un dispositivo
"""
def get_interfaces(ip):
    interfaces = []
    number = int(snmp_query(ip, INTNUMBER_OID)) + 1
    for i in range(number):
        interface = get_if_info(ip, i + 1)
        if interface["ifDescr"] != "Null0" and interface["ifDescr"] != "":
            interfaces.append(interface)
    return interfaces
"""
    Realiza toda la consulta get de acuerdo con los datos que se usan del archivo
    levanta_snmp.py para el usuario y password
"""
def snmp_query(host, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(
            SnmpEngine(),
            UsmUserData(user, password,password,
                authProtocol=usmHMACSHAAuthProtocol,
                privProtocol=usmDESPrivProtocol),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
    )
    if errorIndication:
        raise Exception(str(errorIndication))

    if errorStatus:
        raise Exception(
            f"{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1] or '?'}"
        )

    for name, val in varBinds:
        return str(val)
"""
    Levanta la alerta de saber cuantos paquetes hay perdidos de la red
    Nota: para esta parte es necesario tener dos diccionarios
        Ambos con las interfaces directamente conectadas y con su IP
        Y por otro lado con el porcentaje a solicitar de paquetes perdidos
        Para un mejor performance mandar llamar esta funcion con un hilo que se ejecute
        cada cierto tiempo y asi no se ejecute en secuencia, y se ejecute en paralelo
        y asi se monitore en un intervalo de tiempo
    interface_source/interface_dest:
        Es el diccionario que retorna la funcion get_interfaces, pero hay que
        aniadir la direccion IP de la interfaz
        con la que deseamos trabajar
"""
def check_lost_percentage(interface_source, interface_dest, percentage):
    info_dest = get_if_inout(interface_dest["ip"], interface_dest["mibIndex"])
    info_source = get_if_inout(interface_source["ip"], interface_source["mibIndex"])
    #print(info_source, info_dest)
    paquetes_enviados = int(info_source["ifOutUcastPkts"]) + int(info_source["ifOutNUcastPkts"])
    paquetes_recibidos = int(info_dest["ifInUcastPkts"]) + int(info_dest["ifInNUcastPkts"])
    #print("Paquetes de origen> ",paquetes_enviados, paquetes_recibidos)
    print("ifOutUcastPkts de origen:", int(info_source["ifOutUcastPkts"]))
    print("ifInUcastPkts de destino", int(info_dest["ifInUcastPkts"]))
    lost_packages = int(info_source["ifOutUcastPkts"]) - int(info_dest["ifInUcastPkts"])
    lost_percentage = 0
    if int(info_source["ifOutUcastPkts"]) == 0:
        lost_percentage = abs(lost_packages * 100 / 1)
    else:
        lost_percentage = abs(lost_packages * 100 / int(info_source["ifOutUcastPkts"]))
    
    
    #print(lost_packages, lost_percentage, percentage, info_source["ifOutUcastPkts"])
    """
        Posicion 0 verdadero o falso si se hace una alerta
        Posicion 1 porcentaje de perdida
        Posicion 2 paquetes enviados
        Posicion 3 paquetes perdidos (en valor absoluto por aquello de retransmision)
    """
    return (lost_percentage >= percentage, lost_percentage, paquetes_enviados, abs(paquetes_enviados - paquetes_recibidos))


def relaciona_interfaces(ip,conexiones):
    name=""
    for i in conexiones:
        for k,v in i.items():
            if v==ip:
                name=k.split("_")[1]
                name=int(name)
                interfaz=i[f"interface_{name}"]
                if(name==1):
                    ip_2=i["ip_2"]
                    interfaz_2=i["interface_2"]
                else:
                    ip_2=i["ip_1"]
                    interfaz_2=i["interface_1"]
                break
    interface_1=get_interfaces(ip)
    interface_2=get_interfaces(ip_2)
    for i in range(len(interface_1)):
        if interface_1[i]["ifDescr"]==interfaz:
            interface_1[i]["ip"]=ip
            index_1=i
            break
    for i in range(len(interface_2)):
        if interface_2[i]["ifDescr"]==interfaz_2:
            interface_2[i]["ip"]=ip_2
            index_2=i
            break
    print(f"interfaz:{interfaz}\nip:{ip}\ninterfaz 2:{interfaz_2}\nip 2:{ip_2}")
    return [interface_1[index_1],interface_2[index_2]]

def para_levantar_alertas(conexiones):
    arr=[]
    for i in conexiones:
        arr.append(relaciona_interfaces(i["ip_1"],conexiones))
    return arr
#print(json.dumps(obtain_router_data("10.0.1.254"),indent=4))
#lost1,lost2=get_interfaces("10.0.1.254"),get_interfaces("10.0.2.253")
#print(json.dumps(lost1,indent=4))
#print(json.dumps(lost2,indent=4))
#lost1[3]["ip"]="10.0.1.254"
#lost2[1]["ip"]="10.0.2.253"
#print(check_lost_percentage(lost1[3],lost2[1],50))
#datos=[
#    {
#        "ip_1": "10.0.2.6",
#        "interface_1": "FastEthernet1/0",
#        "host_1": "R5",
#        "ip_2": "10.0.2.5",
#        "interface_2": "FastEthernet1/0",
#        "host_2": "R3"
#    },
#    {
#        "ip_1": "10.0.2.2",
#        "interface_1": "FastEthernet1/1",
#        "host_1": "R2",
#        "ip_2": "10.0.2.1",
#        "interface_2": "FastEthernet1/1",
#        "host_2": "R3"
#    },
#    {
#        "ip_1": "10.0.2.17",
#        "interface_1": "FastEthernet2/0",
#        "host_1": "R1",
#        "ip_2": "10.0.2.18",
#        "interface_2": "FastEthernet2/0",
#        "host_2": "R3"
#    },
#    {
#        "ip_1": "10.0.2.21",
#        "interface_1": "FastEthernet2/1",
#        "host_1": "R4",
#        "ip_2": "10.0.2.22",
#        "interface_2": "FastEthernet2/1",
#        "host_2": "R3"
#    },
#    {
#        "ip_1": "10.0.2.14",
#        "interface_1": "FastEthernet1/1",
#        "host_1": "R4",
#        "ip_2": "10.0.2.13",
#        "interface_2": "FastEthernet1/1",
#        "host_2": "R5"
#    },
#    {
#        "ip_1": "10.0.2.10",
#        "interface_1": "FastEthernet1/0",
#        "host_1": "R1",
#        "ip_2": "10.0.2.9",
#        "interface_2": "FastEthernet1/0",
#        "host_2": "R2"
#    }
#]
#print(json.dumps(para_levantar_alertas(datos),indent=4))
