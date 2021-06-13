from flask import Flask
from flask import request, render_template, url_for, redirect, flash, session
from ssh_cisco import *
from cisco_operaciones import *
from Vlan import *
from db import *
import ipaddress as ip

app = Flask(__name__)
app.config['SECRET_KEY'] = '128381230985812'    

ssh_username = ''
ssh_pwd = ''
switches = ['192.168.1.11', '10.10.1.12', '192.168.1.13']
router = '192.168.1.1'
ssh_conn = None

@app.route('/')
def index():
    global ssh_username
    if ssh_username != '':
        return render_template('index.html')
    return redirect(url_for("login"))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    global ssh_username, ssh_pwd
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['pwd']
        if username == "admin" and pwd == "admin":
            ssh_username = request.form['username']
            ssh_pwd = request.form['pwd']
            return render_template('index.html')
        flash('credenciales ssh incorrectas')
    return render_template('login.html')

@app.route("/new-vlan", methods = ['POST', 'GET'])
def nueva_vlan():
    global ssh_username, conexion
    if ssh_username != '':
        if request.method == 'POST':
            numero = request.form['numero']
            nombre = request.form['nombre']
            id_subred = request.form['id_subred']
            mascara_subred = request.form['mascara_subred']
            interfaces =[] 
            for i in range(1,4):
                key = 'sw{}'.format(i)
                interfaces.append(request.form.getlist(key))

            print(interfaces)            
            try:                
                conexion = create_db("Vlans.db")
                valida = valida_vlan(conexion,numero)
                if valida == 1:
                	flash('La vlan ya existe')
                else:
                	crear_vlan(numero, nombre, id_subred, mascara_subred, interfaces)
                	gateway = str(list(ip.ip_network("{}/{}".format(id_subred,mascara_subred)))[1])
                	crea_vlan(conexion,int(numero), nombre, id_subred, mascara_subred, gateway , interfaces)
                	flash('vlan creada')
                close_db(conexion)                                
            except Exception as e:
                flash('Error al crear la vlan: {}'.format(e))
        return render_template("newVlan.html")
    return redirect(url_for("login"))

@app.route("/delete-vlan", methods = ['POST', 'GET'])
def eliminar_vlan():
    global ssh_username
    if ssh_username != '':
        if request.method == 'POST':
            numero = request.form['numero']
            try:                
                conexion = create_db("Vlans.db")                
                valida = valida_vlan(conexion,int(numero))
                if valida == 0:
                	flash('La vlan que quiere eliminar NO existe')
                else:
                	eliminar_vlant(numero)
                	elimina_vlan(conexion,int(numero))
                	flash('vlan eliminada')
                close_db(conexion)
            except Exception as e:
                flash('Error al eliminar la vlan: {}'.format(e))
        return render_template("deleteVlan.html")
    return redirect(url_for("login"))


@app.route("/vlans", methods = ['GET'])
def ver_vlans():
    global ssh_username
    if ssh_username != '':    	
        try:            
            conexion = create_db("Vlans.db")
            datos = consulta_vlans(conexion)                        
            return render_template("vlans.html", value=datos)
            close_db(conexion)
        except Exception as e:
                flash('Error al consultar las vlans: {}'.format(e))
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


def actualiza_vlans():
	conexion = create_db("Vlans.db")
	create_tb(conexion)
	try:
		datos = ver_vlanst()
		for vlan in datos:
			num = int(vlan.numero)
			nom = vlan.nombre
			ids = vlan.id_subred
			msk = vlan.masc_subred
			gtw = vlan.default_gw
			sw1 = vlan.ifaces_str[0]
			sw2 = vlan.ifaces_str[1]
			sw3 = vlan.ifaces_str[2]
			sws = list()
			sws.append(sw1)
			sws.append(sw2)
			sws.append(sw3)
			crea_vlan(conexion,num,nom,ids,msk,gtw,sws)
		print('\t******* > Vlans Actualizadas < *******\n\n')
	except Exception as e:
		flash('Error al consultar vlans existentes: {}'.format(e))
		print('Error al consultar vlans existentes: {}'.format(e))
	close_db(conexion)


if __name__ == '__main__':		
	actualiza_vlans()
	app.run(host="0.0.0.0", debug=True)	
