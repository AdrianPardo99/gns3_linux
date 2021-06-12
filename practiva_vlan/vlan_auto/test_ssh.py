from ssh_cisco import *
from cisco_operaciones import *
interfaces = [['0/4', '0/5'], [], ['0/2', '0/8']]

crear_vlan(40, 'vlan-prueba', '192.168.40.0', '255.255.255.0', interfaces)
