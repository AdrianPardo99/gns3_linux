from flask_mail import Message
import os

def crear_correo(remitente, destinatario, asunto, texto):
    mensaje = Message(asunto, sender=remitente, recipients=[destinatario])
    mensaje.body = texto
    return mensaje

def habilitar_internet():
    sudoPassword = 'cisco1805'
    command = 'ifconfig eth0 down'
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'ifconfig eth1 up'
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

def habilitar_topologia():
    sudoPassword = 'cisco1805'
    command = 'ifconfig eth0 up'
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command = 'ifconfig eth1 down'
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
