from ssh_cisco import *
from cisco_operaciones import *
import ipcalc

interfaces = [['0/4', '0/5'], [], ['0/2', '0/8']]
m = '255.255.255.0'

#addr = ipcalc.IP('192.168.40.1', mask=m)
#network_with_cidr = str(addr.guess_network())
#bare_network = network_with_cidr.split('/')[0]

#print(addr, network_with_cidr, bare_network)
#add = ipaddress.ip_address("192.168.40.1")


#crear_vlan(40, 'vlan-prueba', '192.168.40.0', '255.255.255.0', interfaces)
#ver_vlanst()

eliminar_vlant(40)
