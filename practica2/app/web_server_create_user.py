#!/usr/bin/env python3
"""
    Author: Adrian González Pardo
    Email: gozapaadr@gmail.com
    A.k.a: d3vcr4ck / DevCrack
    Fecha de modificación: 01/04/2021
    GitHub: AdrianPardo99
    Licencia Creative Commons CC BY-SA
"""
from flask import Flask, redirect, request
from conecta import *
from databaseController import *
from markupsafe import escape
import json

usur="admin"
password="admin01"
con=create_database("routers.db")
create_table_with_params(con,"rest","ip TEXT, usuario TEXT, pass TEXT")
close_database(con)
app = Flask(__name__)

@app.route("/router",methods=["POST","PUT","DELETE","GET"])
@app.route("/router/all")
def router():
    con=create_database("routers.db")
    cmd=[]
    if request.method=="POST":
        ip=request.form["ip"]
        user=request.form["user"]
        pwd=request.form["pwd"]
        print("Alta")
        if len(select_query_all_with_where(con,"rest","ip=? and usuario=?",(ip,user,)))>0:
            close_database(con)
            return {"Error":"Usuario en existencia"}
        insert_into_table(con,"rest","?,?,?",(ip,user,pwd))
        cmd=["conf t",f'username {user} privilege 15 password {pwd}',"end","exit"]
        conexion(ip,usur,password,cmd)
        close_database(con)
        return {"Operacion":f'Alta de usuario {user}'}
    elif request.method=="PUT":
        ip=request.form["ip"]
        user=request.form["user"]
        pwd=request.form["pwd"]
        info=select_query_all_with_where(con,"rest","ip=? and usuario=?",(ip,user,))
        if len(info)==0:
            return {"Error":"Usuario no existe para modificar"}
        update_data(con,"rest","pass=?","ip=? and usuario=?",(pwd,ip,user))
        cmd=["conf t",f'username {user} privilege 15 password {pwd}',"end","exit"]
        conexion(ip,usur,password,cmd)
        close_database(con)
        return {"Operacion":f'Modificacion de usuario {user}'}
    elif request.method=="DELETE":
        ip=request.form["ip"]
        user=request.form["user"]
        pwd=request.form["pwd"]
        info=select_query_all_with_where(con,"rest","ip=? and usuario=? "+
         "and pass=?",(ip,user,pwd))
        if len(info)==0:
            return {"Error":"Usuario no existe para eliminar",
                "Informacion":"O en su defecto el password del usuario es incorrecto"}
        delete_from(con,"rest","ip=? and usuario=?",(ip,user,))
        cmd=["conf t",f'no username {user} privilege 15 password {pwd}',"end","exit"]
        conexion(ip,usur,password,cmd)
        print("Eliminación")
        close_database(con)
        return {"Operacion":f'Eliminacion de usuario {user}'}
    elif request.method=="GET":
        if "all" in str(request.url_rule):
            print("Encontrado")
            l=select_query_all(con,"rest")
            if len(l)==0:
                return {"Informacion":"No hay datos que mostrar"}
            jj=[]
            for i in l:
                st="{"+f'"ip":"{i[0]}", "usuario":"{i[1]}", "pass":"{i[2]}"'+"}"
                jj.append(json.loads(st))
            close_database(con)
            return {"About":jj}
        close_database(con)
        return {"No info":f'{request.url_rule}'}

if __name__=="__main__":
    app.run("0.0.0.0",50000,debug=True)
