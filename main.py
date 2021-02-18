from flask import Flask, redirect, render_template,url_for,request,flash
import requests as api
import json
import os

def clear(): os.system('clear')
clear()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html",logo='/home/eadlpl/Documents/web/DetlosSecurity/templates/images/logo.png')

if __name__ == '__main__':
    app.run(debug=True)