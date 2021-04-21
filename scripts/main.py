#!/usr/bin/env python3
from detecta import *
from ssh_connect import *
import os
import re
import netifaces as ni
import json
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


# Se filtra por primera vez que solo los elementos que sean Cisco

ciscos=[]
for i in range(len(responde)):
    for k,v in responde[i].items():
        if "Cisco_Router_IOS" in v:
            ciscos.append(responde[i])
#print(f"Solo routers cisco: {ciscos}")

# Despues de todo lo que hace el modulo hay que conectarse por ssh o telnet
#   a los dispositivos cisco
cmd=["sh ip int | i Internet address","sh ip int br | include up","sh run | include hostname"]
c=0
red={}
net_router={}
for i in ciscos:
    flag=False
    # Los datos del router (Interfaces)
    for k,v in i.items():
        print(f"Enviando comandos a router con ip: {k}")
        cisco["ip"]=k
        output=conectar(cisco,cmd)
        dir=re.split("\n|  Internet address is | ",output[0])
        inte=re.split("\n|      YES NVRAM  up                    up      | ",output[1])
        host_cmd=output[2].split("hostname ")[1]
        direcciones=[]
        interf=[]
        for j in dir:
            if j!="":
                direcciones.append(j)
        for j in inte:
            if j!="":
                interf.append(j)
        if host_cmd in red.keys():
            flag=False
        else:
            flag=True
        if flag:
            iter={}
            for j in range(len(direcciones)):
                iter[interf[(j*2)]]=direcciones[j]
            red[host_cmd]=iter
        dir.clear()
        inte.clear()
        direcciones.clear()
    # Scan de subredes del router
    if flag:
        for k,v in red.items():
            if 0 not in v.values():
                for j,l in v.items():
                    red_e=l.split("/")
                    if red_e[0] in i.keys():
                        print(f"Exists the network scanning {red_e[0]}")
                    else:
                        net=create_masc_by_prefix(int(red_e[1]))
                        id=get_id_net(list(map(int,red_e[0].split("."))),net)
                        br=get_broadcast_ip(id,net)
                        ip=[id[0],id[1],id[2],id[3]+1]
                        print(f"Scan Network:\n\tID: {id}\n\tNetmask: {net}\n\tBroadcast: {br}")
                        resp_r=scan_range(ip,br)
                        responde=responde+resp_r
                        # aca filtrar Equipos cisco
                        for a in range(len(resp_r)):
                            for b,d in resp_r[a].items():
                                if "Cisco_Router_IOS" in d:
                                    ciscos.append(resp_r[a])
                net_router[k]=v
            red[k]={0:0}

print(f"Host con respuesta:\n{json.dumps(responde,sort_keys=True,indent=4)}")
print(f"Diccionario de routers:\n{json.dumps(net_router,sort_keys=True,indent=4)}")
