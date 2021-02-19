from flask import Flask, redirect, render_template,url_for,request,flash
import requests as api
import json
import os

def clear(): os.system('clear')
clear()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return ('aqui va el login')

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

if __name__ == '__main__':
    app.run(debug=True)

