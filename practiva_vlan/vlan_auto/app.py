from flask import Flask
from flask import request, render_template, url_for, redirect, flash, session
from ssh_cisco import *
from cisco_operaciones import *

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
    global ssh_username
    if ssh_username != '':
        if request.method == 'POST':
            numero = request.form['numero']
            nombre = request.form['nombre']
            id_subred = request.form['id_subred']
            mascara_subred = request.form['mascara_subred']
            interfaces = request.form['interfaces']
            try:

                #crear_vlan(numero, nombre, id_subred, mascara_subred, interfaces)
                #guardar en bd
                flash('vlan creada')
            except Exception as e:
                flash('Error al crear la vlan: ', e)
        return render_template("newVlan.html")
    return redirect(url_for("login"))

@app.route("/delete-vlan", methods = ['POST', 'GET'])
def eliminar_vlan():
    global ssh_username
    if ssh_username != '':
        if request.method == 'POST':
            numero = request.form['numero']
            try:
                #eliminar_vlan_topologia(numero, nombre, id_subred, mascara_subred, interfaces)
                #eliminar en bd
                flash('vlan eliminada')
            except Exception as e:
                flash('Error al eliminar la vlan: ', e)
        return render_template("deleteVlan.html")
    return redirect(url_for("login"))


@app.route("/vlans", methods = ['GET'])
def ver_vlans():
    #conectarse a la bd y obtener todas las vlans
    datos = ["vlan1", "vlan2", "vlan3"]
    global ssh_username
    if ssh_username != '':
        return render_template("vlans.html", value=datos)
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
