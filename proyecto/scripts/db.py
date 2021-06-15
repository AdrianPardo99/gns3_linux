import sqlite3

def conecta_db(name):
	return sqlite3.connect(name)

def close_db(conexion):
	conexion.close()

def crea_tbs(conexion):
	cursor_tb = conexion.cursor()
	cursor_tb.execute(
			"""
				create table if not exists credenciales(
					usr text not null primary key,
					psw text not null
				)				
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists tipoUsr(
					idTipoUsr integer not null primary key,
					descrip text not null
				)
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists persona(
					email text not null primary key,
					usr text not null,					
					nom text not null,
					apep text not null,
					apem text not null,
					sexo text not null,
					idTipoUsr integer not null,
					foreign key(usr) references credenciales(usr),
					foreign key(idTipoUsr) references tipoUsr(idTipoUsr)
				)
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists dispositivos(
					idDisp integer not null primary key,
					nombre text not null,
					sistem text not null,
					locali text not null,					
					encarg text not null,
					contac text not null,
					timeac text not null,
					timemo text not null
				)
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists edo_alerta(
					idEdoAler integer not null primary key,
					descrip text not null
				)
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists alertas(
					idAlert integer not null primary key,
					idDisp integer not null,
					email text not null,
					idEdoAler integer not null,
					descrip text not null,
					fecha timestamp default current_timestamp,
					foreign key(idDisp) references dispositivos(idDisp),
					foreign key(email) references persona(email),
					foreign key(idEdoAler) references edo_alerta(idEdoAler)
				)
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists historial_paquetes(
					idHist integer not null primary key,
					idDisp integer not null,
					paqEnv text not null,
					paqPer text not null,					
					fecha timestamp default current_timestamp,
					foreign key(idDisp) references dispositivos(idDisp)
				)
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists cat_actividades(
					idActiv integer not null primary key,
					descrip text not null
				)
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists rep_sistema(
					idRepor integer not null primary key,
					idActiv integer not null,
					email text not null,
					fecha timestamp default current_timestamp,
					foreign key(email) references persona(email),
					foreign key(idActiv) references cat_actividades(idActiv)
				)
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists edo_control(
					idEdoCo integer not null primary key,
					descrip text not null
				)
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists control_alertas(
					idContr integer not null primary key,
					email text not null,
					idDisp integer not null,
					idEdoCo integer not null,
					foreign key(email) references persona(email),
					foreign key(idDisp) references dispositivos(idDisp),
					foreign key(idEdoCo) references edo_control(idEdoCo)
				)
			"""
		)
	# Ingresamos los tipos de usuario que tendra el sistema
	llena_cats(conexion,"tipoUsr","idTipoUsr","1",[1,'Administrador'],'idTipoUsr,descrip')
	llena_cats(conexion,"tipoUsr","idTipoUsr","2",[2,'Cliente'],'idTipoUsr,descrip')

	# Ingresamos los estados que tengran las alertas dentro del sistema
	llena_cats(conexion,"edo_alerta","idEdoAler","1",[1,'No visto'],'idEdoAler,descrip')
	llena_cats(conexion,"edo_alerta","idEdoAler","2",[2,'Visto'],'idEdoAler,descrip')
	
	# Ingresamos las acciones que se van a registrar dentro del sistema
	llena_cats(conexion,"cat_actividades","idActiv","1",[1,'Escanea Topologia'],'idActiv,descrip')
	llena_cats(conexion,"cat_actividades","idActiv","2",[2,'Muestra Topologia'],'idActiv,descrip')
	
	# Ingresamos los estados en los que se encontraran las alertas en el sistema
	llena_cats(conexion,"edo_control","idEdoCo","1",[1,'Activada'],'idEdoCo,descrip')
	llena_cats(conexion,"edo_control","idEdoCo","2",[2,'Desactivada'],'idEdoCo,descrip')
		


def llena_cats(conexion,tabla,campo,valor,list_data,columnas):
	cursor_tb = conexion.cursor()
	respuesta = cursor_tb.execute("select * from {} where {}={}".format(tabla,campo,valor))
	existencia = respuesta.fetchone()
	if existencia == None:
		sentencia = "insert into {}({}) values(?,?)".format(tabla,columnas)
		cursor_tb.execute(sentencia,list_data)
		conexion.commit()
		# print("Registro exitoso")

def regresa_nombre(conexion,usr):
	cursor_tb = conexion.cursor()
	sentencia = "select nom from persona where usr=?"
	respuesta = cursor_tb.execute(sentencia,(usr,))
	for fila in respuesta:
		return fila[0]

		
def valida_login(conexion,usr,psw,opc):
	cursor_tb = conexion.cursor()
	if(opc==1):
		sentencia = "select * from credenciales where usr=? and psw=?"
		respuesta = cursor_tb.execute(sentencia,(usr,psw))
	if(opc==2):
		sentencia = "select * from credenciales where usr=?"
		respuesta = cursor_tb.execute(sentencia,(usr,))
	existencia = respuesta.fetchone()
	if existencia != None:				
		sentencia = "select idTipoUsr from persona where usr=?"
		respuesta = cursor_tb.execute(sentencia,(usr,))
		if(respuesta.fetchone()[0]==1):
			return "Administrador"
		else:
			return "Cliente"
	else:
		return "Invalido"

def valida_email(conexion,email):
	cursor_tb = conexion.cursor()
	sentencia = "select * from persona where email=?"
	respuesta = cursor_tb.execute(sentencia,(email,))
	existencia = respuesta.fetchone()
	if existencia!=None:
		existe = 1		
	else:
		existe = 0		
	return existe

def alta_usur(conexion,email,usr,psw,nom,apep,apem,sexo,tipo):
	msj = ""
	credenciales = valida_login(conexion,usr,psw,2)
	if(credenciales=="Invalido"):
		correo = valida_email(conexion,email)
		if(correo==0):
			cursor_tb = conexion.cursor()
			sentencia = "insert into credenciales values(?,?)"
			respuesta = cursor_tb.execute(sentencia,(usr,psw))
			sentencia = "insert into persona values(?,?,?,?,?,?,?)"
			respuesta = cursor_tb.execute(sentencia,(email,usr,nom,apep,apem,sexo,tipo))
			conexion.commit()
			if(tipo==1):
				msj = "Administrador registrado"
			elif(tipo==2):
				msj = "Cliente registrado"
		elif(correo==1):
			msj = "Existe una persona con ese correo"
	elif(credenciales=="Administrador"):
		msj = "Existe un administrador con ese usuario"
	elif(credenciales=="Cliente"):
		msj = "Existe un cliente con ese usuario"	

	return msj

def consulta_usur(conexion,tipo):
	cursor_tb = conexion.cursor()
	if(tipo==1):
		sentencia = "select * from persona where idTipoUsr=1"
	elif(tipo==2):
		sentencia = "select * from persona where idTipoUsr=2"
	return cursor_tb.execute(sentencia)

def consulta_usur_esp(conexion,usr):
	cursor_tb = conexion.cursor()
	sentencia = "select * from persona where usr=?"
	return cursor_tb.execute(sentencia,(usr,))

def cambio_usur(conexion,usr,psw,nom,apep,apem,sexo):
	msj = ""
	credenciales = valida_login(conexion,usr,psw,2)
	if(credenciales=="Administrador"):		
		cursor_tb = conexion.cursor()
		sentencia = "update persona set nom=? , apep=? , apem=? , sexo=? where usr=?"
		respuesta = cursor_tb.execute(sentencia,(nom,apep,apem,sexo,usr))
		sentencia = "update credenciales set psw=? where usr=?"
		respuesta = cursor_tb.execute(sentencia,(psw,usr))
		conexion.commit()
		msj = "Administrador {} modificado".format(usr)
	elif(credenciales=="Cliente"):
		cursor_tb = conexion.cursor()
		sentencia = "update persona set nom=? , apep=? , apem=? , sexo=? where usr=?"
		respuesta = cursor_tb.execute(sentencia,(nom,apep,apem,sexo,usr))
		sentencia = "update credenciales set psw=? where usr=?"
		respuesta = cursor_tb.execute(sentencia,(psw,usr))
		conexion.commit()
		msj = "Cliente {} modificado".format(usr)
	elif(credenciales=="Invalido"):
		msj = "El usuario no existe"

	return msj

def elimina_usur(conexion,usr):
	msj = ""
	cursor_tb = conexion.cursor()
	sentencia = "select * from persona where usr=?"
	respuesta = cursor_tb.execute(sentencia,(usr,))
	existencia = respuesta.fetchone()
	if existencia!=None:		
		sentencia = "delete from credenciales where usr=?"
		cursor_tb.execute(sentencia,(usr,))
		sentencia = "delete from persona where usr=?"
		cursor_tb.execute(sentencia,(usr,))
		conexion.commit()
		print("Persona {} eliminada".format(usr))
	else:
		msj = "La persona ya no existe en el sistema"

	return msj







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
# conexion = conecta_db("Proyecto.db")
# # crea_tbs(conexion)
# # print(alta_usur(conexion,'hola1@hola.com','usr1','123','USR01','02','02','M',1))
# # print(alta_usur(conexion,'hola2@hola.com','usr2','123','USR02','02','02','F',2))
# # print(alta_usur(conexion,'hola3@hola.com','usr3','123','USR03','03','03','M',2))
# # print(cambio_usur(conexion,'usr1','12','usr1','01','01','M'))
# # print(cambio_usur(conexion,'usr2','12','usr2','02','02','M'))
# respuesta = regresa_nombre(conexion,'usr1')
# print(respuesta)
# print(elimina_usur(conexion,'usr3','hola3@hola.com'))


# # Crea Vlan
# print("\t > Respuestas al crear VLANS < \n")
# interfaces = [['0/4', '0/5'], [], ['0/2', '0/8']]
# crea_vlan(conexion,1, 'vlan-1', '192.168.10.0', '255.255.255.0', '192.168.1.1' , interfaces)
# interfaces = [['0/4', '0/5'], ['0/2'], ['0/2', '0/8']]
# crea_vlan(conexion,2, 'vlan-2', '192.168.20.0', '255.255.255.0', '192.168.1.1' , interfaces)
# interfaces = [['0/4', '0/5'], ['0/2','0/7'], ['0/2', '0/8']]
# crea_vlan(conexion,3, 'vlan-3', '192.168.30.0', '255.255.255.0', '192.168.1.1' , interfaces)
# print("\n")

# Consulta Vlans
# print("\t > Respuestas al consultar all < \n")
# datos = consulta_all(conexion)
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

