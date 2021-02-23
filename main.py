from flask import Flask, redirect, render_template,url_for,request,flash
import requests as api
import json
import os

# --
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

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

@app.route('/login')
def login():
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
