#!/usr/bin/env python3
from detecta import *
from ssh_connect import *
import os
import re
import netifaces as ni
cisco={
    "device_type":"cisco_xe",
    "ip":"",
    "username":"admin",
    "password":"admin",
    "secret":"1234"
}
# Listamos las interfaces de red aqui
interfaces=os.listdir("/sys/class/net/")
c=0
for i in range(len(interfaces)):
    print(f"{i+1}: {interfaces[i]}")
read=int(input("Ingresa el numero de interfaz: "))-1
# Obtiene datos del diccionario y accede directamente al apartado de IPv4
dic_data=ni.ifaddresses(interfaces[read])
if 2 not in dic_data:
    print("No hay un dirección IPv4 en la interfaz")
    exit(1)

dic_data=dic_data[2][0]
print(f"\n---------About---------\n{interfaces[read]}: {dic_data}")
addr=list(map(int,dic_data["addr"].split(".")))
net=list(map(int,dic_data["netmask"].split(".")))

c=determinate_prefix(net)
idnet=get_id_net(addr,net)
range_net=get_broadcast_ip(idnet,net)

# Se obtiene el identificador de la subred:
print(f"Identificador de red: {idnet}/{c}")
# Se obtiene direccion de broadcast
print(f"Broadcast ip: {range_net}")
# Se prepara para hacer is_host_up
ips=[idnet[0],idnet[1],idnet[2],idnet[3]+1]
responde=scan_range(ips,range_net)
print(f"Host con respuesta: {responde}")

# Se filtra por primera vez que solo los elementos que sean Cisco

ciscos=[]
for i in range(len(responde)):
    for k,v in responde[i].items():
        if "Cisco_Router_IOS" in v:
            ciscos.append(responde[i])
print(f"Solo routers cisco: {ciscos}")

# Despues de todo lo que hace el modulo hay que conectarse por ssh o telnet
#   a los dispositivos cisco
cmd=["sh ip int | i Internet address","sh ip int br | include up"]
c=0
red={}
for i in ciscos:
    # Los datos del router (Interfaces)
    for k,v in i.items():
        print(f"Enviando comandos a router con ip: {k}")
        cisco["ip"]=k
        output=conectar(cisco,cmd)
        dir=re.split("\n|  Internet address is | ",output[0])
        inte=re.split("\n|      YES NVRAM  up                    up      | ",output[1])
        direcciones=[]
        interf=[]
        for j in dir:
            if j!="":
                direcciones.append(j)
        for j in inte:
            if j!="":
                interf.append(j)
        red[f"Router {c}"]={}
        iter=red[f"Router {c}"]
        for j in range(len(direcciones)):
            iter[interf[(j*2)]]=direcciones[j]
        dir.clear()
        inte.clear()
        direcciones.clear()
    # Scan de subredes del router
    for k,v in red.items():
        for j,l in v.items():
            red=l.split("/")
            if red[0] in i.keys():
                print(f"Existe scan de red {red[0]}")
            else:
                net=create_masc_by_prefix(int(red[1]))
                id=get_id_net(list(map(int,red[0].split("."))),net)
                br=get_broadcast_ip(id,net)
                ip=[id[0],id[1],id[2],id[3]+1]
                resp_r=scan_range(ip,br)
                responde=responde+resp_r

    c+=1
