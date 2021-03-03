from flask import Flask, redirect, render_template,url_for,request,flash
from flask.globals import session
import pymongo
from pymongo import MongoClient
import requests as api
import json
import os
from cryptography.fernet import Fernet

file = open('key.key','rb')
key = file.read()
f = Fernet(key)
def sessionstatus():
    if 'username' in session:
        logged_in = True
    else:
        logged_in = False
        return redirect(url_for('home'))
    return logged_in    


# --
app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb+srv://eadlpl11:5PinS5Jvi5WdHOOA@cluster0.dnnfi.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

@app.route('/')
def home():
    if 'username' in session:
        logged_in = True
    else:
        logged_in = False
    return render_template("index.html", logged_in = logged_in)

@app.route('/perfil')
def perfil():
    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))
    return render_template("perfil.html", logged_in = logged_in)

@app.route('/camaras')
def camara():
    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))
    return render_template("camaras.html", logged_in = logged_in)

@app.route('/fotografias')
def fotos():
    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))
    return render_template("fotos.html", logged_in = logged_in)

@app.route('/video')
def video():
    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))
    return render_template("video.html", logged_in = logged_in)

@app.route('/register')
def register():
    logged_in = sessionstatus()
    if logged_in == True:
        return redirect(url_for('home'))
    return render_template("register.html")

@app.route('/login', methods = ['GET','POST'])
def login():
    user = db.camaras.find_one({'email':request.form.get('correo')})

    
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        pe = f.decrypt( user['password'])
        pe = pe.decode()
        password = request.form.get('pass')
        error = None
        if user is None:
            error = 'Contraseña o correo invalidos'
        
        elif pe != password:
            error = 'Contraseña o correo invalidos'

        if error is None:
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('home'))
        flash(error)

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/verification_register', methods=['POST','GET'])
def verRegister():
    email = request.form.get('correo')
    password = request.form.get('pass')
    name = request.form.get('name')
    lastName = request.form.get('lastName')
    gender = request.form.get('gender')
    verification = request.form.get('verPass')
    userName = request.form.get('nick')

    error = None
    if verification != password:
        error = "Las contraseñas no coinciden"
    if error == None:
        db.camaras.insert_one({

        "username": userName,
        "email": email,
        "password": f.encrypt(password.encode()),
        "nombre": name,
        "apellido": lastName,
        "genero": gender,

        "hardware": {
            "ip": "xxx.xxx.xxx.xxx",
            "ssid": "XXXXXX",
            "password": "XXXXXXXXXXXXXXXXXXXX",
            "static": {
                "camara": 11
            }
        },

        "imagenes":{

            "nombre": "19231.jpg","hora":'17/05/25'
        },
            
        })


        return redirect(url_for('home'))
    
    flash(error)
    return render_template("register.html")

if __name__ == '__main__':
    app.run(port = 5000,debug=True)
