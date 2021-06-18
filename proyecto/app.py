from flask import Flask
from flask_mail import Mail, Message
from flask import request, render_template, url_for, redirect, flash, session, jsonify
from scripts.scanner import *
from scripts.correos import *
from scripts.db import *
from os import system
import time
import scripts.down_protocols as down
import scripts.levanta_eigrp as eigrp
import scripts.levanta_ospf as ospf
import scripts.levanta_rip as rip
import scripts.redes_operaciones as redes_operaciones
from  scripts.dispositivos import * 
from  scripts.get_snmp import * 
from  scripts.set_snmp import * 

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = '12345'

#configuracion de email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'redes.proyecto920@gmail.com'
app.config['MAIL_PASSWORD'] = "X3egGemSD2qmZB2"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
mail2 = Mail(app)

conexiones_global = {}

@app.route('/send-email', methods=['GET'])
def send_email():
    if request.method == "GET":
        # json_data = flask.request.json
        # destinatario = json_data["destinatario"]
        # asunto = json_data["asunto"]
        # cuerpo = json_data["cuerpo"]
        destinatario = "fnicosg@gmail.com"
        asunto = "prueba envio de correos"
        cuerpo = "mensaje del correo"
        habilitar_internet()
        print("internet habilitado")
        correo = crear_correo("redes.proyecto920@gmail.com", destinatario, asunto, cuerpo)
        mail.send(correo)
        print("correo enviado")
        habilitar_topologia()
        print("topologia habilitada")
        return jsonify("sucess")


# ------------------------------ >   Menu publico  < ------------------------------

"""
    Ruta Inicial del proyecto, solo muetra nuestros nombres
"""
@app.route('/',methods = ['POST','GET'])
def inicio():
    session.clear()
    return render_template('index.html')    

"""
    Ruta que carga el login del proyecto
"""
@app.route('/login',methods = ['POST','GET'])
def login():
    session.clear()
    if request.method == 'POST':    
        usr=request.form['usuario']
        psw=request.form['clave']
        conexion = conecta_db("Proyecto.db")
        respuesta = valida_login(conexion,usr,psw,1)        
        if respuesta == "Administrador":
            session["usr"] = usr            
            session["idTipoUsr"] = 1
            session["nom"] = regresa_nombre(conexion,usr)
            session["email"] = regresa_email(conexion,usr)
            session["gateway"]= redes_operaciones.get_gateway()
            return respuesta            
        if respuesta == "Cliente":
            session["usr"] = usr
            session["idTipoUsr"] = 2
            session["nom"] = regresa_nombre(conexion,usr)
            session["email"] = regresa_email(conexion,usr)
            session["gateway"]= redes_operaciones.get_gateway()
            return respuesta
        if respuesta == "Invalido":
            return respuesta
        close_db(conexion)
    return render_template('login.html')

"""
    Ruta que sirve para dar de alta usuarios del tipo cliente
"""
@app.route('/regPublic',methods = ['POST','GET'])
def registro_Publico():
    session.clear()
    return render_template('registro.html')

# --------------------------------------------------------------------------------



# ------------------------------ >  Menu Administrador  < ------------------------------

"""
    Rescanear toda la red y configura protocolos
"""
@app.route('/adm0',methods = ['POST','GET'])
def adm0():
    
    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                opc=request.form['opc']
                gateway = session["gateway"] 
                print(gateway)
                #gateway = '10.0.1.254'
                if(opc=='1'):
                    # Volver a escanear
                    print("Volver a escanear")
                    mapeo = True
                    while mapeo:
                        try:
                            res = mapearRed("eth0")
                            dibujarRed(res)
                            
                            datos_dips = obtener_datos_inciales_dispositivos(res[0])
                            print(datos_dips)
                            

                            mapeo = False
                            conexion = conecta_db("Proyecto.db")
                            
                            global conexiones_global
                            con_local = {}
                            for dispositivo in datos_dips:
                                
                                datos_snmp = obtener_datos_dispositivo(dispositivo[1])

                                lista_datos = [int(dispositivo[0][1:]), dispositivo[0], datos_snmp[2], datos_snmp[4], dispositivo[1], datos_snmp[3]]
                                alta_disp(conexion,lista_datos) #idDisp,nombre,sistem,locali,ip,contac

                                #Conexiones de dispositivo
                                conexiones = obtener_conexiones_dispositivo(dispositivo[0], res[4])
                                session['conexiones-{}'.format(dispositivo[0])] = conexiones

                                con_local[dispositivo[0]] = conexiones
                                
                                

                                # try:
                                #     #paquetes
                                #     paqEnviados, paqPerdidos = obtener_paquetes_dispositivo(conexiones)
                                #     print(paqEnviados, paqPerdidos)
                                #     inserta_paquetes(conexion, int(dispositivo[0][1:]), paqEnviados, paqPerdidos)
                                # except Exception as e:
                                #     print(e)    

                            with open('data.json', 'w') as file:
                                json.dump(con_local, file, indent=4)

                            respuesta = consulta_usur(conexion,2)
                            numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
                        except Exception as e:
                            print("show_network(): error al mapear topologia, ", e)
                    pass
                elif(opc=='2'):
                    # RIP
                    #mandar llamar limpiar protcocolos
                    print("RIP")
                    down.init_configure(gateway)
                    rip.init_configure(gateway)
                    pass
                elif(opc=='3'):
                    # OSPF
                    print("OSPF")
                    down.init_configure(gateway)
                    ospf.init_configure(gateway)
                    pass
                elif(opc=='4'):
                    # EIGRP
                    print("EIGRP")
                    down.init_configure(gateway)
                    eogrp.init_configure(gateway)
                    pass
            conexion = conecta_db("Proyecto.db")
            numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
            return render_template('Adm0.html',nombrecito=session["nom"],numAlertas=numalertas[0])

    except Exception as e:
        print(e)
        return redirect(url_for("login"))   

"""
    Gestiona Administradores - Menu
"""
@app.route('/adm1',methods = ['POST','GET'])
def adm1():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            conexion = conecta_db("Proyecto.db")
            numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
            return render_template('Adm1.html',nombrecito=session["nom"],numAlertas=numalertas[0])

    except Exception as e:
        print(e)
        return redirect(url_for("login"))


"""
    Gestiona Administradores - Form Agregar
"""
@app.route('/adm11',methods = ['POST','GET'])
def adm11():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                usr=request.form['usr']
                psw=request.form['psw']
                nom=request.form['nom']
                ap1=request.form['ap1']
                ap2=request.form['ap2']
                gen=request.form['gen']
                ema=request.form['ema']
                conexion = conecta_db("Proyecto.db")
                respuesta = alta_usur(conexion,ema,usr,psw,nom,ap1,ap2,gen,1)
                print(inserta_bitacora(conexion,'Administrador Registrado',session["email"]))
                close_db(conexion)
                return respuesta

    except Exception as e:
        print(e)
        return redirect(url_for("login"))
    
    conexion = conecta_db("Proyecto.db")
    numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
    return render_template('Adm11.html',nombrecito=session["nom"],numAlertas=numalertas[0])

"""
    Gestiona Administradores - Tabla Busca
"""
@app.route('/adm12',methods = ['POST','GET'])
def adm12():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            conexion = conecta_db("Proyecto.db")
            respuesta = consulta_usur(conexion,1)           
            numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
            return render_template('Adm12.html',filas=respuesta,nombrecito=session["nom"],numAlertas=numalertas[0])

    except Exception as e:
        print(e)
        return redirect(url_for("login"))   

"""
    Gestiona Administradores - Form modifica
"""
@app.route('/adm121',methods = ['POST','GET'])
def adm121():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                usr=request.form['usr']
                conexion = conecta_db("Proyecto.db")
                respuesta = consulta_usur_esp(conexion,usr)             
                numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
                return render_template('Adm121.html',filas=respuesta,nombrecito=session["nom"],numAlertas=numalertas[0])

    except Exception as e:
        print(e)
        return redirect(url_for("login"))   

"""
    Gestiona Administradores - Metodo modifica
"""
@app.route('/adm122',methods = ['POST','GET'])
def adm122():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                usr=request.form['usr']
                psw=request.form['psw']
                nom=request.form['nom']
                ap1=request.form['ap1']
                ap2=request.form['ap2']
                gen=request.form['gen']
                ema=request.form['ema']
                conexion = conecta_db("Proyecto.db")
                respuesta = cambio_usur(conexion,usr,psw,nom,ap1,ap2,gen)
                print(inserta_bitacora(conexion,'Administrador Modificado',session["email"]))
                close_db(conexion)
                return respuesta

    except Exception as e:
        print(e)
        return redirect(url_for("login"))   


"""
    Gestiona Administradores - Tabla pre eliminar
"""
@app.route('/adm13',methods = ['POST','GET'])
def adm13():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            conexion = conecta_db("Proyecto.db")
            respuesta = consulta_usur(conexion,1)           
            numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
            return render_template('Adm13.html',filas=respuesta,nombrecito=session["nom"],numAlertas=numalertas[0])

    except Exception as e:
        return redirect(url_for("login"))   

"""
    Gestiona Administradores - Metodo eliminar
"""
@app.route('/adm131',methods = ['POST','GET'])
def adm131():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                usr=request.form['usr']
                conexion = conecta_db("Proyecto.db")
                respuesta = elimina_usur(conexion,usr)
                print(inserta_bitacora(conexion,'Persona Eliminada',session["email"]))
                close_db(conexion)
                return respuesta

    except Exception as e:
        return redirect(url_for("login"))


"""
    Gestiona Clientes - Menu
"""
@app.route('/adm2',methods = ['POST','GET'])
def adm2():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            pass

    except Exception as e:
        print(e)
        return redirect(url_for("login"))

    conexion = conecta_db("Proyecto.db")
    numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
    return render_template('Adm2.html',nombrecito=session["nom"],numAlertas=numalertas[0])

"""
    Gestiona Clientes - Agrega Usuario
"""
@app.route('/adm21',methods = ['POST','GET'])
def adm21():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                usr=request.form['usr']
                psw=request.form['psw']
                nom=request.form['nom']
                ap1=request.form['ap1']
                ap2=request.form['ap2']
                gen=request.form['gen']
                ema=request.form['ema']
                conexion = conecta_db("Proyecto.db")
                respuesta = alta_usur(conexion,ema,usr,psw,nom,ap1,ap2,gen,2)
                print(inserta_bitacora(conexion,'Cliente Registrado',session["email"]))
                close_db(conexion)
                return respuesta

    except Exception as e:
        print(e)
        return redirect(url_for("login"))

    conexion = conecta_db("Proyecto.db")
    numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
    return render_template('Adm21.html',nombrecito=session["nom"],numAlertas=numalertas[0])

"""
    Gestiona Clientes - Busca clientes
"""
@app.route('/adm22',methods = ['POST','GET'])
def adm22():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            conexion = conecta_db("Proyecto.db")
            respuesta = consulta_usur(conexion,2)
            numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
            return render_template('Adm22.html',filas=respuesta,nombrecito=session["nom"],numAlertas=numalertas[0])

    except Exception as e:
        print(e)
        return redirect(url_for("login"))

"""
    Gestiona Clientes - Form modifica Clientes
"""
@app.route('/adm221',methods = ['POST','GET'])
def adm221():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                usr=request.form['usr']
                conexion = conecta_db("Proyecto.db")
                respuesta = consulta_usur_esp(conexion,usr)
                numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
                return render_template('Adm221.html',filas=respuesta,nombrecito=session["nom"],numAlertas=numalertas[00])

    except Exception as e:
        print(e)
        return redirect(url_for("login"))   

"""
    Gestiona Clientes - Metodo modifica
"""
@app.route('/adm222',methods = ['POST','GET'])
def adm222():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                usr=request.form['usr']
                psw=request.form['psw']
                nom=request.form['nom']
                ap1=request.form['ap1']
                ap2=request.form['ap2']
                gen=request.form['gen']
                ema=request.form['ema']
                conexion = conecta_db("Proyecto.db")
                respuesta = cambio_usur(conexion,usr,psw,nom,ap1,ap2,gen)
                print(inserta_bitacora(conexion,'Cliente Modificado',session["email"]))
                close_db(conexion)
                return respuesta

    except Exception as e:
        print(e)
        return redirect(url_for("login"))   

"""
    Gestiona Clientes - Form elimina Clientes
"""
@app.route('/adm23',methods = ['POST','GET'])
def adm23():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            conexion = conecta_db("Proyecto.db")
            respuesta = consulta_usur(conexion,2)
            numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
            return render_template('Adm23.html',filas=respuesta,nombrecito=session["nom"],numAlertas=numalertas[0])

    except Exception as e:
        print(e)
        return redirect(url_for("login"))   

#  ------------------------------ Topologia ----------------------------
@app.route('/adm3',methods = ['POST','GET'])
def adm3():
    try:
        conexion = conecta_db("Proyecto.db")
        respuesta = consulta_usur(conexion,2)
        numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
        print(inserta_bitacora(conexion,'Consulto Topologia',session["email"]))
        return render_template('network.html',nombrecito=session["nom"],numAlertas=numalertas[0])
    except Exception as e:
        print(e)
        return redirect(url_for("login")) 

"""
    Dispositivos - Muestra dispositivos
"""
@app.route('/adm4',methods = ['POST','GET'])
def adm4():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            conexion = conecta_db("Proyecto.db")
            respuesta = consulta_disp(conexion)

            numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
            print(inserta_bitacora(conexion,'Consulto Dispositivos',session["email"]))
            return render_template('Adm4.html',filas=respuesta,nombrecito=session["nom"],numAlertas=numalertas[0])

    except Exception as e:
        print(e)
        return redirect(url_for("login"))   



"""
    Dispositivos - Dispositivos especifico
"""
@app.route('/adm41',methods = ['POST','GET'])
def adm41():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                datos = list()
                paque = list()
                idDisp=request.form['idDisp']
                conexion = conecta_db("Proyecto.db")
                respuesta = consulta_disp_esp(conexion,idDisp)
                for elemento in respuesta:
                    datos.append(elemento[0]) #idDisp
                    datos.append(elemento[1]) #nombre
                    datos.append(elemento[2]) #sistem
                    datos.append(elemento[3]) #locali
                    datos.append(elemento[4]) #encarg
                    datos.append(elemento[5]) #contac
                    datos.append(elemento[6]) #timeac
                    datos.append(elemento[7]) #timemo
                respuesta = alertas_activas(conexion,elemento[0],session["email"])
                datos.append(respuesta[0]) #datos[8] = edo_alertas         
                try:
                    #paquetes
                    #conexiones_dispositivos = session['conexiones-{}'.format(datos[1])]
                    conexiones = None
                    with open('data.json') as json_file:
                        conexiones = json.load(json_file)
  
                    # Print the type of data variable
                    print(conexiones[datos[1]])
                    # paqEnviados, paqPerdidos = obtener_paquetes_dispositivo(conexiones)
                    # print(paqEnviados, paqPerdidos)
                    # inserta_paquetes(conexion, int(dispositivo[0][1:]), paqEnviados, paqPerdidos)
                    
                    
                except Exception as e:
                    print(e)
                historial = consulta_paquetes(conexion,idDisp)
                for elemento in historial:                  
                    paque.append(elemento)
                grafica = consulta_paquete_esp(conexion,idDisp)             
                numalertas = cantidad_alertas_NoVistas(conexion,session["email"])

                # Area de alertas
                pregunta_alertas = consult_edo_alertas(conexion,idDisp,session["email"]).fetchone()
                if (pregunta_alertas!=None):    
                    if(pregunta_alertas[0]==1):
                        print(regis_alerta(conexion,idDisp,session["email"],'Los paquetes del Router {} han sido actualizados para su visualizacion'.format(idDisp)))
                        destinatario = session['email']
                        asunto = "Alerta: Actualizacion de paquetes del Router {} ".format(idDisp)
                        cuerpo = "Se ha actualizado el porcentaje de paquetes perdidos del Router {}".format(idDisp)
                        habilitar_internet()
                        print("internet habilitado")
                        correo = crear_correo("redes.proyecto920@gmail.com", destinatario, asunto, cuerpo)
                        mail.send(correo)
                        print("correo enviado")
                        habilitar_topologia()
                        print("topologia habilitada")
                        # aqui ponemos el email
                                                
                print(inserta_bitacora(conexion,'Actualizo Paquetes de un Router',session["email"]))
                close_db(conexion)
                return render_template('Adm41.html',filas=datos,tablita=paque,grafiquita=grafica,nombrecito=session["nom"],email=session["email"],numAlertas=numalertas[0])

    except Exception as e:
        print(e)
        return redirect(url_for("login"))   

"""
    Dispositivos - Gestiona alertas
"""
@app.route('/adm411',methods = ['POST','GET'])
def adm411():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                idDisp=request.form['idDisp']
                email=request.form['email']
                conexion = conecta_db("Proyecto.db")
                respuesta = config_alertas(conexion,idDisp,email)
                if(respuesta=="Alertas Desactivadas"):
                    # Desactiva notificaciones
                    pass
                elif(respuesta=="Alertas Activadas"):
                    # activa notificaciones
                    pass
                elif(respuesta=="Persona registrada para recibir notificaciones"):
                    # activa notificaciones
                    pass
                # print(respuesta)
                return respuesta

    except Exception as e:
        print(e)
        return redirect(url_for("login"))

"""
    Dispositivos - Form Modifica Routers
"""
@app.route('/adm412',methods = ['POST','GET'])
def adm412():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':

                datos = list()
                idDisp=request.form['idDisp']
                nombre=request.form['nombre']
                sistem=request.form['sistem']
                locali=request.form['locali']
                encarg=request.form['encarg']
                contac=request.form['contac']
                timeac=""
                timemo=""
                datos.append(idDisp)
                datos.append(nombre)
                datos.append(sistem)
                datos.append(locali)
                datos.append(encarg)
                datos.append(contac)
                datos.append(timeac)
                datos.append(timemo)
                conexion = conecta_db("Proyecto.db")
                numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
                return render_template('Adm412.html',filas=datos,nombrecito=session["nom"],email=session["email"],numAlertas=numalertas[0])

    except Exception as e:
        print(e)
        return redirect(url_for("login"))

"""
    Dispositivos - Metodo Modifica Routers
"""
@app.route('/adm413',methods = ['POST','GET'])
def adm413():
    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                datos = list()              
                nombre=request.form['nombre'] #Este parametro no se modifica
                sistem=request.form['sistem']
                locali=request.form['locali']
                encarg=request.form['encarg']
                contac=request.form['contac']
                idDisp=request.form['idDisp']
                datos.append(sistem)
                datos.append(locali)
                datos.append(contac)
                datos.append(idDisp) #El id va al final
                 #conexion a snmp
                conexion = conecta_db("Proyecto.db")
                respuesta = modifica_disp(conexion,datos)
                print("conexion exitosa")
                
                try:
                    # global conexiones_global
                    # print(conexiones_global)
                    conexiones_dispositivos = None
                    with open('data.json') as json_file:
                        conexiones_dispositivos = json.load(json_file)
  
                    # Print the type of data variable
                    print(conexiones_dispositivos[nombre])

                    actualizar_datos_dispositivo(conexiones_dispositivos[nombre], nombre, locali, contac, sistem)
                    print("actualizar datos snmp")
                    # Area de alertas
                    pregunta_alertas = consult_edo_alertas(conexion,idDisp,session["email"]).fetchone()
                    if (pregunta_alertas!=None):    
                        if(pregunta_alertas[0]==1):
                            print(regis_alerta(conexion,idDisp,session["email"],'Informacion del router {} ha sido actualizada'.format(idDisp)))

                            # destinatario = session['email']
                            # asunto = "Alerta: Actualizacion Informacion del router {} ".format(idDisp)
                            # cuerpo = "Se ha se han actualizado algunos campos SNMP del router {}".format(idDisp)
                            # habilitar_internet()
                            # print("internet habilitado")
                            # correo = crear_correo("redes.proyecto920@gmail.com", destinatario, asunto, cuerpo)
                            # mail2.send(correo)
                            # print("correo enviado")
                            # habilitar_topologia()
                            # print("topologia habilitada")

                    print(inserta_bitacora(conexion,'Modificacion SNMP a un Router',session["email"]))
                    close_db(conexion)
                    return respuesta
                except Exception as e:
                    print("413:",e)
                    pass

                
                # Poner Funcion que modifique estos parametros en el router 'nombre'
                return respuesta
                

    except Exception as e:
        print(e)
        return redirect(url_for("login"))


"""
    Dispositivos - Historial notificaciones
"""
@app.route('/adm5',methods = ['POST','GET'])
def adm5():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            dato = list()
            conexion = conecta_db("Proyecto.db")
            respuesta = (cantidad_alertas_NoVistas(conexion,session["email"]))[0]
            numalertas = (cantidad_alertas(conexion,session["email"]))[0]
            if(numalertas!=0):
                alertas = consul_alertas(conexion,session["email"])
                for i in alertas:
                    dato.append(i)
            else:
                alertas = None          
            
            print(inserta_bitacora(conexion,'El Usuario Vio Sus Alertas',session["email"]))
            print(set_alertas_visto(conexion,session["email"]))
            return render_template('Adm5.html',nombrecito=session["nom"],Alertas=numalertas,numAlertas=respuesta,datitos=dato)


    except Exception as e:
        print(e)
        return redirect(url_for("login"))


"""
    Dispositivos - Historial bitacoras
"""
@app.route('/adm6',methods = ['POST','GET'])
def adm6():

    try:
        usr = session["idTipoUsr"]
        if(usr!=1):
            return redirect(url_for("login"))
        else:
            dato = list()
            conexion = conecta_db("Proyecto.db")
            respuesta = (cantidad_alertas_NoVistas(conexion,session["email"]))[0]
            numalertas = (cantidad_alertas(conexion,session["email"]))[0]
            if(numalertas!=0):
                alertas = consul_alertas(conexion,session["email"])
                for i in alertas:
                    dato.append(i)
            else:
                alertas = None

            bitacoras = consulta_bitacora(conexion)

            return render_template('Adm6.html',nombrecito=session["nom"],Alertas=numalertas,numAlertas=respuesta,datitos=dato,tablita=bitacoras)


    except Exception as e:
        print(e)
        return redirect(url_for("login"))    

# --------------------------------------------------------------------------------



# ------------------------------ >  Menu Cliente  < ------------------------------



@app.route('/usr0',methods = ['POST','GET'])
def usr0():

    try:
        usr = session["idTipoUsr"]
        if(usr!=2):
            return redirect(url_for("login"))
        else:
            pass


    except Exception as e:
        return redirect(url_for("login"))

    return render_template('Usr0.html')

@app.route('/usr1',methods = ['POST','GET'])
def usr1():

    try:
        usr = session["idTipoUsr"]
        if(usr!=2):
            return redirect(url_for("login"))
        else:
            pass 
        
        try:
            conexion = conecta_db("Proyecto.db")
            respuesta = consulta_usur(conexion,2)
            numalertas = cantidad_alertas_NoVistas(conexion,session["email"])
            return render_template('network2.html',nombrecito=session["nom"],numAlertas=numalertas[0])
        except Exception as e:
            print(e)
            return redirect(url_for("login")) 
    except Exception as e:
        return redirect(url_for("login"))

@app.route('/usr2',methods = ['POST','GET'])
def usr2():

    try:
        usr = session["idTipoUsr"]
        if(usr!=2):
            return redirect(url_for("login"))
        else:
            pass


    except Exception as e:
        return redirect(url_for("login"))

    return render_template('Usr2.html')

@app.route('/usr21',methods = ['POST','GET'])
def usr21():

    try:
        usr = session["idTipoUsr"]
        if(usr!=2):
            return redirect(url_for("login"))
        else:
            pass


    except Exception as e:
        return redirect(url_for("login"))

    return render_template('Usr21.html')

@app.route('/usr3',methods = ['POST','GET'])
def usr3():

    try:
        usr = session["idTipoUsr"]
        if(usr!=2):
            return redirect(url_for("login"))
        else:
            pass


    except Exception as e:
        return redirect(url_for("login"))

    return render_template('Usr3.html')


# --------------------------------------------------------------------------------


@app.errorhandler(404)
def error404(error):
    return render_template("404.html")

if __name__ == '__main__':
    conexion = conecta_db("Proyecto.db")
    crea_tbs(conexion)
    close_db(conexion)
    # llamamos al snpm
    # Guardamops los dispositovos en la BD
    app.run(host='0.0.0.0',debug=True)