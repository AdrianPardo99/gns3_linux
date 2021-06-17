#!/usr/bin/env python3
from netmiko import ConnectHandler
from scripts.detecta import *
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
    output=con.send_command_timing("sh ip ospf",delay_factor=0.5)
    if output!="":
        num_ospf=output.split("ospf ")[1].split("\" ")[0]
        cmd=["","conf t","no int loop0",f"no router ospf {num_ospf}","end"]
        for i in cmd:
            con.send_command_timing(i,delay_factor=0.5)
    cmd=["conf t","no router rip","no router eigrp 20","end"]
    for i in cmd:
        con.send_command_timing(i,delay_factor=0.5)
    print("\tDown all dynamic routing protocols")
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
    output=con.send_command_timing("sh ip ospf",delay_factor=0.5)
    output=output.split("\n")[0]
    if output!="":
        num_ospf=output.split("ospf ")[1].split("\" ")[0]
        cmd=["","conf t","no int loop0",f"no router ospf {num_ospf}","end"]
        for i in cmd:
            con.send_command_timing(i,delay_factor=0.5)
    cmd=["conf t","no router rip","no router eigrp 20","end"]
    for i in cmd:
        con.send_command_timing(i,delay_factor=0.5)
    print("\tDown all dynamic routing protocols")
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
