import sqlite3

def create_db(name):
	return sqlite3.connect(name)

def close_db(conexion):
	conexion.close()

def create_tb(conexion):
	cursor_tb = conexion.cursor()
	cursor_tb.execute(
			"""
				create table if not exists vlans(					
					numero integer primary key,
					nombre text not null,
					id_subred text not null,
					ms_subred text not null,
					d_gateway text not null,
					SW1_inter text not null,
					SW2_inter text not null,
					SW3_inter text not null
				)
			"""
		)

def valida_vlan(conexion,numero_vlan):
	cursor_tb = conexion.cursor()
	sentencia = "select * from vlans where numero=?"
	respuesta = cursor_tb.execute(sentencia,(numero_vlan,))
	existencia = respuesta.fetchone()
	if existencia!=None:
		existe = 1
		# print("La Vlan ya existe")
	else:
		existe = 0
		# print("La Vlan NO existe")
	return existe

def crea_vlan(conexion,num,nom,id_sub,ms_sub,d_gate,list_interfaces=None):
	cursor_tb = conexion.cursor()
	valida = valida_vlan(conexion,num)
	if valida == 1:
	 	print("Error al crear Vlan {} -  VLAN EXISTENTE".format(num))	 	
	else:
		list_data = list()		 
		SW1 = ' '.join(list_interfaces[0])
		SW2 = ' '.join(list_interfaces[1])
		SW3 = ' '.join(list_interfaces[2])		
		sentencia = "insert into vlans(numero,nombre,id_subred,ms_subred,d_gateway,SW1_inter,SW2_inter,SW3_inter) values(?,?,?,?,?,?,?,?)"
		list_data.append(num)
		list_data.append(nom)
		list_data.append(id_sub)
		list_data.append(ms_sub)
		list_data.append(d_gate)
		list_data.append(SW1)
		list_data.append(SW2)
		list_data.append(SW3)
		# print(list_data)
		cursor_tb.execute(sentencia,list_data)
		conexion.commit()
		print("Vlan {} Registrada".format(list_data[0]))

def consulta_vlans(conexion):
	cursor_tb = conexion.cursor()
	sentencia = "select * from vlans"
	return cursor_tb.execute(sentencia)

def consulta_vlan_especial(conexion,num):	
	cursor_tb = conexion.cursor()
	valida = valida_vlan(conexion,num)
	if valida == 1:
		sentencia = "select * from vlans where numero=?"
		resultado = cursor_tb.execute(sentencia,(num,))	
	else:
		print("Error al consultar Vlan {} -  VLAN NO EXISTENTE".format(num))
		resultado = None
	return resultado

def elimina_vlan(conexion,num):
	cursor_tb = conexion.cursor()
	valida = valida_vlan(conexion,num)
	if valida == 1:
		sentencia = "delete from vlans where numero=?"
		cursor_tb.execute(sentencia,(num,))
		conexion.commit()
		print("Vlan {} eliminada exitosamente".format(num))
	else:
		print("Error al eliminar Vlan {} -  VLAN NO EXISTENTE".format(num))		




# --------------- Testing area ---------------
# # Crear BD
conexion = create_db("Vlans.db")
create_tb(conexion)

# # Crea Vlan
# print("\t > Respuestas al crear VLANS < \n")
# interfaces = [['0/4', '0/5'], [], ['0/2', '0/8']]
# crea_vlan(conexion,1, 'vlan-1', '192.168.10.0', '255.255.255.0', '192.168.1.1' , interfaces)
# interfaces = [['0/4', '0/5'], ['0/2'], ['0/2', '0/8']]
# crea_vlan(conexion,2, 'vlan-2', '192.168.20.0', '255.255.255.0', '192.168.1.1' , interfaces)
# interfaces = [['0/4', '0/5'], ['0/2','0/7'], ['0/2', '0/8']]
# crea_vlan(conexion,3, 'vlan-3', '192.168.30.0', '255.255.255.0', '192.168.1.1' , interfaces)
# print("\n")

# # Consulta Vlans
# print("\t > Respuestas al consultar VLANS < \n")
# datos = consulta_vlans(conexion)
# for dato in datos:
# 	print(dato)
# print("\n")

# # Consulta especial Vlan
# print("\t > Respuestas al consultar una VLAN < \n")
# dato = consulta_vlan_especial(conexion,1)
# for fila in dato:
# 	print(fila)
# print("\n")

# # Elimina vlan
# print("\t > Respuestas al eliminar una VLAN < \n")
# elimina_vlan(conexion,1)
# print("\n")

# # Consulta Vlans
# print("\t > Respuestas al consultar VLANS < \n")
# datos = consulta_vlans(conexion)
# for dato in datos:
# 	print(dato)
# print("\n")

# close_db(conexion)

#import ipaddress as ip
#net = ip.ip_network("{}/{}".format("192.168.1.0","255.255.255.0"))
#print(list(net)[1])

