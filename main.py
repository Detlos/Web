from flask import Flask, redirect, render_template,url_for,request,flash
from flask.globals import session
import pymongo
from pymongo import MongoClient
import requests as api
import json
import os

# --
client = pymongo.MongoClient("mongodb+srv://eadlpl11:5PinS5Jvi5WdHOOA@cluster0.dnnfi.mongodb.net/test?retryWrites=true&w=majority")


db = client.test
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html",)

@app.route('/perfil')
def perfil():
    return render_template("perfil.html")

@app.route('/camaras')
def camara():
    return render_template("camaras.html")

@app.route('/fotografias')
def fotos():
    return render_template("fotos.html")

@app.route('/video')
def video():
    return render_template("video.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login', methods = ['GET','POST'])
def login():
    users = db.camaras.find({'email':request.form.get('correo')})
    password = db.camaras.find({'correo':request.form.get('pass')})
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('pass')
        error = None

        if users is None or password is None:
            error = 'Contraseña o correo invalidos'
        
        if error is None:
            return redirect(url_for('home')) 

        flash(error)

    return render_template("login.html")



@app.route('/verification_register', methods=['POST','GET'])
def verRegister():
    email = request.form.get('correo')
    password = request.form.get('pass')
    name = request.form.get('name')
    lastName = request.form.get('lastName')
    gender = request.form.get('gender')
    return f'{gender}'

if __name__ == '__main__':
    app.run(port = 5000,debug=True)
