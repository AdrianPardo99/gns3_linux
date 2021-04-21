#!/usr/bin/env python3
from netmiko import ConnectHandler

def conectar(cisco,cmd):
    net_connect = ConnectHandler(**cisco)
    net_connect.enable()
    output=[]
    for i in range(len(cmd)):
        output.append(net_connect.send_command(cmd[i]))
    return output
