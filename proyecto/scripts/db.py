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

def regresa_email(conexion,usr):
	cursor_tb = conexion.cursor()
	sentencia = "select email from persona where usr=?"
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

def valida_disp(conexion,idDisp):
	cursor_tb = conexion.cursor()
	sentencia = "select * from dispositivos where idDisp=?"
	respuesta = cursor_tb.execute(sentencia,(idDisp,))
	existencia = respuesta.fetchone()
	if existencia!=None:
		existe = 1		
	else:
		existe = 0
	return existe

def alta_disp(conexion,list_data):
	cursor_tb = conexion.cursor()
	valida = valida_disp(conexion,list_data[0])
	if valida == 0:
		sentencia = "insert into dispositivos(idDisp,nombre,sistem,locali,encarg,contac,timeac,timemo) values(?,?,?,?,?,?,?,?)"
		cursor_tb.execute(sentencia,list_data)
		conexion.commit()
		return "Registro exitoso"
	else:
		return "Dispositivo previamente registrado"

def consulta_disp(conexion):
	cursor_tb = conexion.cursor()
	sentencia = "select * from dispositivos"
	return cursor_tb.execute(sentencia)

def consulta_disp_esp(conexion,idDisp):
	cursor_tb = conexion.cursor()
	valida = valida_disp(conexion,idDisp)
	if valida == 1:
		sentencia = "select * from dispositivos where idDisp=?"
		return cursor_tb.execute(sentencia,(idDisp,))
	else:
		return None

def modifica_disp(conexion,list_data):
	cursor_tb = conexion.cursor()
	sentencia = "update dispositivos set sistem=?, locali=?, encarg=?, contac=?  where idDisp=?"
	cursor_tb.execute(sentencia,list_data)
	conexion.commit()
	return "Dispositivo modificado"

def inserta_paquetes(conexion,idDisp,paqEnviados,paqPerdidos):
	cursor_tb = conexion.cursor()
	respuesta = cursor_tb.execute("select max(idHist) from historial_paquetes")				
	idReg = respuesta.fetchone()[0]
	if(idReg==None):
		idRegistro=1
	else:
		idRegistro = int(idReg)
		idRegistro = idRegistro+1	
	sentencia = "insert into historial_paquetes(idHist,idDisp,paqEnv,paqPer) values(?,?,?,?)"
	cursor_tb.execute(sentencia,(idRegistro,idDisp,paqEnviados,paqPerdidos))
	conexion.commit()
	return "Registro insertado"

def consulta_paquetes(conexion,idDisp):
	cursor_tb = conexion.cursor()
	sentencia = "select * from historial_paquetes where idDisp=? order by idDisp desc"
	return cursor_tb.execute(sentencia,(idDisp,))	

def consulta_paquete_esp(conexion,idDisp):
	cursor_tb = conexion.cursor()
	respuesta = cursor_tb.execute("select max(idHist) from historial_paquetes where idDisp=?",(idDisp,))	
	idReg = respuesta.fetchone()[0]	
	sentencia = "select paqEnv,paqPer from historial_paquetes where idHist=?"
	respuesta = cursor_tb.execute(sentencia,(idReg,))	
	return respuesta.fetchone()

def alertas_activas(conexion,idDisp,email):
	cursor_tb = conexion.cursor()
	sentencia = "select idEdoCo from control_alertas where idDisp=? and email=?"
	respuesta = cursor_tb.execute(sentencia,(idDisp,email))
	existencia = respuesta.fetchone()
	if existencia == None:		
		return (2,)
	else:
		return existencia

def valida_control(conexion,idDisp,email):
	cursor_tb = conexion.cursor()
	sentencia = "select * from control_alertas where idDisp=? and email=?"
	respuesta = cursor_tb.execute(sentencia,(idDisp,email))
	existencia = respuesta.fetchone()
	if existencia!=None:
		existe = 1		
	else:
		existe = 0
	return existe


def config_alertas(conexion,idDisp,email):
	cursor_tb = conexion.cursor()
	exis_dispo = valida_disp(conexion,idDisp)
	if(exis_dispo==1):
		exis_email = valida_email(conexion,email)
		if(exis_email==1):
			exis_reg = valida_control(conexion,idDisp,email)
			if(exis_reg==1):				
				sentencia = "select idEdoCo from control_alertas where idDisp=? and email=?"
				respuesta = cursor_tb.execute(sentencia,(idDisp,email))
				idstatus = respuesta.fetchone()[0]
				if(idstatus==1):
					sentencia = "update control_alertas set idEdoCo=2 where idDisp=? and email=?"
					respuesta = cursor_tb.execute(sentencia,(idDisp,email))
					conexion.commit()
					return "Alertas Desactivadas"
				elif(idstatus==2):
					sentencia = "update control_alertas set idEdoCo=1 where idDisp=? and email=?"
					respuesta = cursor_tb.execute(sentencia,(idDisp,email))
					conexion.commit()
					return "Alertas Activadas"
			else:				
				respuesta = cursor_tb.execute("select max(idContr) from control_alertas ")				
				idreg = respuesta.fetchone()[0]
				if(idreg==None):
				  	idRegistro=1
				else:
				 	idRegistro = int(idreg)
				 	idRegistro = idRegistro+1				
				sentencia = "insert into control_alertas(idContr,email,idDisp,idEdoCo) values(?,?,?,1)"
				cursor_tb.execute(sentencia,(idRegistro,email,idDisp))
				conexion.commit()
				return "Persona registrada para recibir notificaciones"
		else:
			return "No existe el email"
	else:
		return "No existe el dispositivo"

def regis_alerta(conexion,idDisp,email,descrip):
	cursor_tb = conexion.cursor()
	exis_dispo = valida_disp(conexion,idDisp)
	if(exis_dispo==1):
		exis_email = valida_email(conexion,email)
		if(exis_email==1):
			respuesta = cursor_tb.execute("select max(idAlert) from alertas ")				
			idreg = respuesta.fetchone()[0]
			if(idreg==None):
				  idRegistro=1
			else:
				 idRegistro = int(idreg)
				 idRegistro = idRegistro+1
			sentencia = "insert into alertas(idAlert,idDisp,email,idEdoAler,descrip) values(?,?,?,1,?)"
			cursor_tb.execute(sentencia,(idRegistro,idDisp,email,descrip))
			conexion.commit()
			return "Alerta Registrada"
		else:
			return "No existe el email"
	else:
		return "No existe el dispositivo"

def consul_alertas(conexion,email):
	cursor_tb = conexion.cursor()	
	cursor_tb = conexion.cursor()
	sentencia = "select * from alertas where email=? order by idAlert desc"
	respuesta = cursor_tb.execute(sentencia,(email,))
	return respuesta	

def cantidad_alertas(conexion,email):
	cursor_tb = conexion.cursor()	
	sentencia = "select count(*) from alertas where email=?"
	respuesta = cursor_tb.execute(sentencia,(email,))
	return respuesta.fetchone()

def cantidad_alertas_NoVistas(conexion,email):
	cursor_tb = conexion.cursor()	
	sentencia = "select count(*) from alertas where email=? and idEdoAler=1" #Contamos las alertas que esten en 1 "No vistas"
	respuesta = cursor_tb.execute(sentencia,(email,))
	return respuesta.fetchone()

def set_alertas_visto(conexion,email):
	cursor_tb = conexion.cursor()	
	sentencia = "update alertas set idEdoAler=2 where email=?" #Pasamos las alertas en 2 "Vistas"
	respuesta = cursor_tb.execute(sentencia,(email,))
	conexion.commit()
	return "Alertas dejadas en visto"


# --------------- Testing area ---------------
# # Crear BD
# conexion = conecta_db("Proyecto.db")
# cursor_tb = conexion.cursor()
# respuesta = consulta_paquete_esp(conexion,1)
# print(inserta_paquetes(conexion,1,'94874','1270'))
# resp=cursor_tb.execute("select * from alertas")
# for i in resp:
# 	print(i)
# datos = list()


# respuesta = consul_alertas(conexion,'elias@alumno.com')
# for i in respuesta:
# 	print(i)
# conexion = conecta_db("Proyecto.db")
# print(regis_alerta(conexion,4,'elias@alumno.com','ALERTA PRUEBA COMO NO'))
# crea_tbs(conexion)
# lista = [1,'R1','SO','Localidad','Encargado','Contacto','Tiempo Activo','Tiempo Ultima Modificacion']
# print(alta_disp(conexion,lista))
# lista = [2,'R2','SO','Localidad','Encargado','Contacto','Tiempo Activo','Tiempo Ultima Modificacion']
# print(alta_disp(conexion,lista))
# lista = [3,'R3','SO','Localidad','Encargado','Contacto','Tiempo Activo','Tiempo Ultima Modificacion']
# print(alta_disp(conexion,lista))
# lista = [4,'R4','SO4','Localidad4','Encargado4','Contacto4','Tiempo Activo4','Tiempo Ultima Modificacion4']
# print(alta_disp(conexion,lista))
# respuesta = consulta_disp_esp(conexion,1)
# if respuesta != None:
# 	for fila in respuesta:
# 		print(fila)
# print(alertas_activas(conexion,1,'elias@alumno.com'))

# print(config_alertas(conexion,1,'elias@alumno.com'))
# respuesta = alertas_activas(conexion,2,'elias@alumno.com')
# print(respuesta[0])
# respuesta = consulta_disp(conexion)
# for fila in respuesta:
# 	print(fila)


# # print(alta_usur(conexion,'hola1@hola.com','usr1','123','USR01','02','02','M',1))
# # print(alta_usur(conexion,'hola2@hola.com','usr2','123','USR02','02','02','F',2))
# # print(alta_usur(conexion,'hola3@hola.com','usr3','123','USR03','03','03','M',2))
# # print(cambio_usur(conexion,'usr1','12','usr1','01','01','M'))
# # print(cambio_usur(conexion,'usr2','12','usr2','02','02','M'))
# respuesta = consulta_disp(conexion)
# print(respuesta)
# print(elimina_usur(conexion,'usr3','hola3@hola.com'))