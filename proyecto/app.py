from flask import Flask, request, render_template, url_for, redirect, flash, session
from scripts.scanner import *

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = '12345'


@app.route('/',methods = ['POST','GET'])
def inicio():
    return render_template('index.html')    

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
            res = mapearRed("eth0")
            dibujarRed(res)
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
