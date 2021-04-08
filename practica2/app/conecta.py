#!/usr/bin/env python3
"""
    Author: Adrian González Pardo
    Email: gozapaadr@gmail.com
    A.k.a: d3vcr4ck / DevCrack
    Fecha de modificación: 01/04/2021
    GitHub: AdrianPardo99
    Licencia Creative Commons CC BY-SA
"""

import telnetlib

def conexion(host,user,password,cmd_list):
    tn=telnetlib.Telnet(host)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii')+b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    for i in cmd_list:
        tn.write(i.encode("ascii")+b"\n")
    print(tn.read_all().decode("ascii"))
    tn.close()
#host="192.168.0.1"
#user="cisco"
#password="cisco"
#cmd=["sh ip route","sh ip int br","exit"]
#tn=conexion(host,user,password,cmd)
