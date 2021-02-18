from flask import Flask, redirect, render_template,url_for,request,flash
<<<<<<< HEAD
=======
import requests as api
>>>>>>> 2fc3f60862f257f74bd493230f70a3e439f0918b
import json
import os

def clear(): os.system('clear')
clear()

app = Flask(__name__)

@app.route('/')
def home():
<<<<<<< HEAD
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")

if __name__ == '__main__':
    app.run(port = 5000,debug=True)
=======
    return render_template("index.html",logo='/home/eadlpl/Documents/web/DetlosSecurity/templates/images/logo.png')

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 2fc3f60862f257f74bd493230f70a3e439f0918b
