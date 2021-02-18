from flask import Flask, redirect, render_template,url_for,request,flash
import json
import os

def clear(): os.system('clear')
clear()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")

if __name__ == '__main__':
    app.run(port = 5000,debug=True)