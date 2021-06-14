from flask import Flask
from flask import render_template, redirect, request, jsonify
from flask_mail import Mail, Message

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

@app.route('/')
def index():
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


@app.route('/network')
def show_network():
    mapeo = True
    while mapeo:
        try:
            res = mapearRed("eth0")
            dibujarRed(res)
            mapeo = False
        except Exception as e:
            print("show_network(): error al mapear topologia, ", e)

    return render_template('network.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
