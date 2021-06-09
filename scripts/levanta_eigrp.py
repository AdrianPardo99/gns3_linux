#!/usr/bin/env python3
from netmiko import ConnectHandler
from detecta import *
import netifaces as ni

user = 'admin'
password = 'admin'
secret = '1234'
domain_name="la-pandilla-mantequilla"

cisco = {
    "device_type":"cisco_ios",
    'ip': '',
    "username":user,
    "password":password,
    "secret":secret
}
known_routers = []

"""
    Llamar al modulo usando la ip y solo llamar a init_configure,
    modificar en cualquier caso el domain_name ya que si es recargar
    la topologia el cdp detecta el host con todo y domain_name
    
    Funciona para el caso en que el acceso por ssh no entra en modo exec directo
    hay que configurar los routers para que accedan en modo normal y despues
    a modo exec
"""
def init_configure(ip):
    cisco['ip'] =ip
    con=ConnectHandler(**cisco)
    con.enable()
    output=con.send_command_timing("sh run | i hostname",delay_factor=0.5)
    hostname=output.split()
    known_routers.append(hostname[1])
    print(hostname[1]+":")
    eigrp(con)
    neighbors(con)
    con.disconnect()

def configure_router(router,con):
    output = con.send_command(f'show cdp entry {router}')
    resp = output.split()
    con.send_command_timing(f"ssh -l {user} {resp[8]}",delay_factor=0.5)
    con.send_command_timing(password,delay_factor=0.5)
    con.send_command_timing("ena",delay_factor=0.5)
    con.send_command_timing(secret,delay_factor=0.5)
    output=con.send_command_timing("sh run | i hostname",delay_factor=0.5)
    hostname=output.split()
    if hostname[1] in known_routers:
    	con.send_command_timing('exit',delay_factor=0.5)
    	return None
    print(hostname[1]+":")
    known_routers.append(hostname[1])
    eigrp(con)
    neighbors(con)
    con.send_command_timing('exit',delay_factor=0.5)
    return None

def neighbors(con):
    output = con.send_command_timing('show cdp neighbors',delay_factor=0.5)
    routers = output.split()
    routers.pop()
    i = 35
    while i < len(routers):
    	if ("R" in routers[i+4]):
    		configure_router(routers[i],con)
    	i = i + 8

def findNetworkID(ip,con):
    output = con.send_command_timing(f'show running-config | i {ip}',delay_factor=0.5)
    mask = output.split()
    addr=list(map(int,mask[2].split(".")))
    netmask=list(map(int,mask[3].split(".")))
    wildcard=create_wildcard(netmask)
    idnet=get_id_net(addr,netmask)
    return [arr_to_ip(idnet),arr_to_ip(wildcard),arr_to_ip(netmask)]

def eigrp(con):
    output=con.send_command_timing('show ip interface brief | i up',delay_factor=0.5)
    ip=output.split()
    ip_id = []
    wildcards=[]
    netmasks=[]
    i = 1
    while i < len(ip):
        out=findNetworkID(ip[i],con)
        ip_id.append(out[0])
        wildcards.append(out[1])
        netmasks.append(out[2])
        i = i + 6
    for i in range(len(ip_id)):
        print(f"\tID: {ip_id[i]} Wildcard: {wildcards[i]} Netmask: {netmasks[i]}")
    cmd=["conf t",f"router eigrp 20"]
    for i in range(len(ip_id)):
        cmd.append(f"net {ip_id[i]} {wildcards[i]}")
        cmd.append(f"net {ip_id[i]} {netmasks[i]}")
    cmd.append("end")
    for i in cmd:
        out=con.send_command_timing(i,delay_factor=0.5)
