#!/usr/bin/env python3
from pyvis.network import Network
from module_scan import *
from dibujo import *

"""
    @author:        Adrian González Pardo
    @date_update:   23/04/2021
    @github:        AdrianPardo99
"""

# Listamos las interfaces de red aqui
interfaces=os.listdir("/sys/class/net/")
c=0
for i in range(len(interfaces)):
    print(f"{i+1}: {interfaces[i]}")
read=int(input("Ingresa el numero de interfaz: "))-1
# Modulo que permite escanear todos los datos
res = scan_by_interface(interfaces[read],"admin","admin","1234")

general = res[0]
interconexiones = res[1]
routers = res[2]
devices = res[3]

net = construirDibujoTopologia(routers, interconexiones, devices, general)
net.save_graph("temp.html")
cambiarEnlaces("temp.html", "net.html")
eliminarTemporal("temp.html")
