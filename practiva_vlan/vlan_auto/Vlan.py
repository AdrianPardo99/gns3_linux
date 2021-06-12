class Vlan:
    def __init__(self, numero = None, nombre = None, id_subred = None, masc_subred = None, default_gw = None):
        self.numero = numero
        self.nombre = nombre
        self.id_subred = id_subred
        self.masc_subred = masc_subred
        self.default_gw = default_gw
        self.ifaces = [[] ,[],[]]
        self.ifaces_str = []
    
    def arr2str(self):
        i = 0
        for switch in self.ifaces:
            self.ifaces_str.append("")
            for iface in switch:
                self.ifaces_str[i] += iface + ' '
            i += 1

    def __repr(self):
        return '''Vlan {
        numero: {}
        nombre: {}
        id subred: {}
        mascara: {}
        gateway: {}
        interfaces: {}
    }'''.format(self.numero, self.nombre, self.id_subred, self.masc_subred, self.default_gw, self.ifaces)

    def __str__(self):
        return "numero: {}\nnombre: {}\nid subred:{}\nmascara subred: {}\ngateway: {}\n interfaces:{}".format(self.numero, self.nombre, self.id_subred, self.masc_subred, self.default_gw, self.ifaces)


