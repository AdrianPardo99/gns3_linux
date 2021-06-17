import socket, ipaddress, os
import re

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_id_network(ip):
    id_net = ""
    try:
        os.system("ifconfig | grep 'netmask' >> temp.txt")
        with open('temp.txt', 'r') as res:
            id_nets = res.read().split("\n")
            for posible in id_nets:
                if ip in posible:
                    id_net = re.sub(' +', ' ', posible)
                    id_net = id_net[id_net.find("netmask")+8 : len(id_net)]
                    id_net = id_net.split(' ')[0]
    except Exception as e:
        print("get_id_network():error obteniendo id de red")
    os.system("rm temp.txt")
    id_net = ipaddress.ip_network('{}/{}'.format(ip, id_net), strict=False)
    return id_net


def get_gateway():
    os.system("route | grep 'default' >> temp.txt")    
    with open('temp.txt', 'r') as res:
        gateway = res.read().split('\n')[0]
        gateway = re.sub(' +', ' ', gateway)
        gateway = gateway.split(' ')[1]
    os.system('rm temp.txt')
    return gateway



