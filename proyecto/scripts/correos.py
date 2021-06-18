from flask_mail import Message
import os, time

def crear_correo(remitente, destinatario, asunto, texto):
    mensaje = Message(asunto, sender=remitente, recipients=[destinatario])
    mensaje.body = texto
    return mensaje

def habilitar_internet():
    sudoPassword = 'cisco1805'
    command = 'sudo ifconfig eth0 down'
    p = os.system(command)
    
    command = 'sudo ifconfig eth1 up'
    os.system(command)
    
    #time.sleep(0.5)

def habilitar_topologia():
    sudoPassword = 'cisco1805'
    command = 'sudo ifconfig eth0 up'
    p = os.system(command)
    
    command = 'sudo ifconfig eth1 down'
    os.system(command)
    
    #time.sleep(0.5)