#!/usr/bin/env python3
from pyvis.network import Network
from scripts.module_scan import *
from scripts.dibujo import *

"""
    @author:        Adrian González Pardo
    @date_update:   23/04/2021
    @github:        AdrianPardo99
"""

def mapearRed(interface):
    res = scan_by_interface(interface,"admin","admin","1234")
    return res

def dibujarRed(data):
    general = data[0]
    interconexiones = data[1]
    routers = data[2]
    devices = data[3]
    print("construyendo topologia...")
    net = construirDibujoTopologia(routers, interconexiones, devices, general)
    print("guardando topologia en html")
    net.save_graph("scripts/temp.html")
    print("corrigiendo enlaces css y js a forma local...")
    cambiarEnlaces("scripts/temp.html", "scripts/net.html")
    print("eliminando archivo temporal de topologia")
    eliminarTemporal("scripts/temp.html")
    print("fin de dibujo")
