#!/usr/bin/env python3
from module_scan import *

# Listamos las interfaces de red aqui
interfaces=os.listdir("/sys/class/net/")
c=0
for i in range(len(interfaces)):
    print(f"{i+1}: {interfaces[i]}")
read=int(input("Ingresa el numero de interfaz: "))-1
# Modulo que permite escanear todos los datos
scan_by_interface(interfaces[read],"admin","admin","1234")
