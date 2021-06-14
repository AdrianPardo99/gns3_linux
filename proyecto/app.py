from flask import Flask
from flask import render_template, redirect
from scripts.scanner import *

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = '12345'


@app.route('/')
def index():
    return render_template('index.html')

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
