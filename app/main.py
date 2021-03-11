import requests
from flask import Flask, redirect, render_template,url_for,request,flash
from flask.globals import session
import pymongo
from pymongo import MongoClient
import requests as api
import json
import os
from cryptography.fernet import Fernet
from requests import get



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



app = Flask(__name__)

app.secret_key = "elMiadoDelElmer"

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
    if 'username' in session:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        error = None
        correo = request.form.get('correo')
        password = request.form.get('pass')
        my_dict = {
            'correo':correo,
            'password':password
        }
        endpoint = 'http://localhost:5050/login'
        respuesta = api.post(endpoint,json = my_dict)
        dato = respuesta.json()
        if dato['respuesta'] == "Correo o contrasena invalidos":
            error = 'Contraseña o correo invalidos'
        
        if error is None:
            session.clear()
            session['username'] = dato['respuesta']
            usuario = session['username']
            flash(f"Bienvenido {usuario}","info")
            return redirect(url_for('home'))
            
        flash(error, "error")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Has cerrado sesion correctamente.","info")
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
    
    my_dict = {
        'username':userName,
        'email':email,
        'password':password,
        'nombre':name,
        'apellido':lastName,
        'genero':gender
    }

    """ endpoint = 'https://detlossecurityapi.herokuapp.com/register' """
    endpoint = 'http://localhost:5050/register'

    if verification != password:
        respuesta = "Las contraseñas no coinciden"
    else:
        respuesta = api.post(endpoint,json = my_dict)
        respuestaJson = respuesta.json()
    if respuestaJson['respuesta'] == 'SE INSERTARON LOS DATOS CORRECTAMENTE':
        flash(respuestaJson['respuesta'],'info')
        return redirect(url_for('home'))
       
    
    flash(respuestaJson['respuesta'], 'error')
    return render_template("register.html")

if __name__ == '__main__':
    app.run(port = 5000,debug=True)
