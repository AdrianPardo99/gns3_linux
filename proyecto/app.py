from flask import Flask
from flask_mail import Mail, Message
from flask import request, render_template, url_for, redirect, flash, session, jsonify
from scripts.scanner import *
from scripts.correos import *

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

@app.route('/',methods = ['POST','GET'])
def inicio():
    return render_template('index.html')    

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


#@app.route('/network')
#def show_network():
    

@app.route('/login',methods = ['POST','GET'])
def login():
    return render_template('login.html')

@app.route('/regPublic',methods = ['POST','GET'])
def registro_Publico():
    return render_template('registro.html')



@app.route('/adm0',methods = ['POST','GET'])
def adm0():
    return render_template('Adm0.html')

@app.route('/adm1',methods = ['POST','GET'])
def adm1():
    return render_template('Adm1.html')

@app.route('/adm11',methods = ['POST','GET'])
def adm11():
    return render_template('Adm11.html')

@app.route('/adm12',methods = ['POST','GET'])
def adm12():
    return render_template('Adm12.html')

@app.route('/adm121',methods = ['POST','GET'])
def adm121():
    return render_template('Adm121.html')

@app.route('/adm13',methods = ['POST','GET'])
def adm13():
    return render_template('Adm13.html')



@app.route('/adm2',methods = ['POST','GET'])
def adm2():
    return render_template('Adm2.html')

@app.route('/adm21',methods = ['POST','GET'])
def adm21():
    return render_template('Adm21.html')

@app.route('/adm22',methods = ['POST','GET'])
def adm22():
    return render_template('Adm22.html')

@app.route('/adm221',methods = ['POST','GET'])
def adm221():
    return render_template('Adm221.html')

@app.route('/adm23',methods = ['POST','GET'])
def adm23():
    return render_template('Adm23.html')


@app.route('/adm3',methods = ['POST','GET'])
def adm3():
    mapeo = True
    while mapeo:
        try:
            #res = mapearRed("eth0")
            #dibujarRed(res)
            mapeo = False
        except Exception as e:
            print("show_network(): error al mapear topologia, ", e)
    return render_template('Adm3.html')


@app.route('/adm4',methods = ['POST','GET'])
def adm4():
    return render_template('Adm4.html')

@app.route('/adm41',methods = ['POST','GET'])
def adm41():
	return render_template('Adm41.html')


@app.route('/adm5',methods = ['POST','GET'])
def adm5():
    return render_template('Adm5.html')


@app.route('/usr0',methods = ['POST','GET'])
def usr0():
    return render_template('Usr0.html')

@app.route('/usr1',methods = ['POST','GET'])
def usr1():
    return render_template('Usr1.html')

@app.route('/usr2',methods = ['POST','GET'])
def usr2():
    return render_template('Usr2.html')

@app.route('/usr21',methods = ['POST','GET'])
def usr21():
	return render_template('Usr21.html')

@app.route('/usr3',methods = ['POST','GET'])
def usr3():
    return render_template('Usr3.html')


@app.errorhandler(404)
def error404(error):
    return render_template("404.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
