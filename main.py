import requests
from flask import Flask, redirect, render_template,url_for,request,flash
from flask.globals import session
import pymongo
from pymongo import MongoClient
import requests as api
import json
from cryptography.fernet import Fernet
from requests import get


url1 = "https://img-detlos.herokuapp.com/"
'''url1 = "http://127.0.0.1:5050"'''
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


@app.route('/video')
def video():
    logged_in = sessionstatus()

    if logged_in != True:        
        return redirect(url_for('home'))

    username = session['username']
    

    endpoint = 'url1/get_hardware'
    my_dict = {'username':session['username']}
    
    answer = api.post(endpoint,json = my_dict)

    print(answer.text)

    camera_ip = answer.json()
    

    return render_template("video.html", logged_in = logged_in,camera_ip = camera_ip)


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
        

        endpoint = url1+'/login'
        respuesta = api.post(endpoint,json = my_dict)
        print(type(respuesta))
        dato = respuesta.json()
        if dato['respuesta'] == "Correo o contrasena invalidos":
            error = 'Contraseña o correo invalidos'
        
        if error is None:
            session.clear()
            session['username'] = dato['respuesta']
            usuario = session['username']
            flash(f"Bienvenido {usuario}","info")
            return redirect(url_for('perfil'))
            
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

    """ endpoint = 'httpss://detlossecurityapi.herokuapp.com/register' """
    endpoint = url1+'/register'

    if verification != password:
        respuesta = "Las contraseñas no coinciden"
    else:
        respuesta = api.post(endpoint,json = my_dict)
        respuestaJson = respuesta.json()
    if respuestaJson['msg'] == 'Se insertaron los datos correctamente':
        flash(respuestaJson['msg'],'info')
        return redirect(url_for('home'))
       
    
    flash(respuestaJson['msg'], 'error')
    return render_template("register.html")


@app.route('/fotografias')
def fotos():
    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))
    
    usuario = api.post(url1+'/obtenerImagenes2', json={"username":session['username']})
    
    imagenes = []
    fechas = []
    
    print(type(usuario))
    print(usuario)


    for x in usuario.values():
        info = list(x.values())
        imagenes.append(info[1])
        fecha = info[0]
        fechas.append(fecha[:10])
    fechas = set(fechas)
    


    
    return render_template("fotos.html", logged_in = logged_in, fotos = imagenes )


@app.route('/configuracion')
def configuracionInicial():
    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))
    return render_template("configuracion.html")

@app.route("/cambio_genero")
def cambio_genero():
    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))
    return render_template("cambio_de_genero.html")



@app.route("/cambio_genero_boton", methods = ["POST"])
def cambio_genero_boton():


    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))

    password = api.post(url1+"/obtener_pass", json={"username":session['username']})
    print(password.text)
    verification = request.form.get('verPass')

    if password.text != verification:
        return redirect(url_for('perfil'))
    else:
        api.post(url1+"/cambiar_genero", json={"username": session['username']})
        return redirect(url_for('perfil'))
    return redirect(url_for('perfil'))


@app.route("/cambio_pass")
def cambio_pass():

    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))
    return render_template("cambiar_pass.html")




@app.route("/cambio_pass_boton", methods = ["POST"])
def cambio_pass_boton():
    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))


    password = api.post(url1+"/obtener_pass", json={"username":session['username']})
    verification = request.form.get('verPass')


    nueva = request.form.get('nuevaPass')
    verifiacionNueva = request.form.get('verNuevaPass')

    if password.text != verification:
        return redirect(url_for('perfil'))
    if(nueva == verifiacionNueva):
        api.post(url1+"/cambiar_pass", json={"username": session['username'],'new':nueva})
        return redirect(url_for('perfil'))

    else:

        return redirect(url_for('perfil'))


@app.route("/cambio_nombre")
def cambio_nombre():
    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))


    return render_template("cambio_nombre.html")


@app.route("/cambio_nombre_boton", methods = ["POST"])
def cambio_nombre_boton():


    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))


    password = api.post(url1+"/obtener_pass", json={"username":session['username']})
    verification = request.form.get('verPass')


    nombre = request.form.get('nuevoNombre')
    apellido = request.form.get('nuevoApellido')



    if password.text != verification:
        return redirect(url_for('perfil'))
    else:
        api.post(url1+"/cambiar_nombres", json={"username": session['username'],'name':nombre,"last_name": apellido })
        return redirect(url_for('perfil'))

@app.route("/eliminar_cuenta")
def eliminar_cuenta():

    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))

    return render_template("eliminar_cuenta.html")

@app.route("/eliminar_cuenta_boton", methods=["POST"])
def eliminar_cuenta_boton():

    logged_in = sessionstatus()
    if logged_in != True:
        return redirect(url_for('home'))


    password = api.post(url1+"/obtener_pass", json={"username":session['username']})
    verification = request.form.get('verPass')


    if password.text != verification:
        return redirect(url_for('perfil'))
    else:
        api.post(url1+"/borrar_cuenta", json = {"username":session['username']})

        session.pop('username', None)
        flash("Has borrado la cuenta.")
        return redirect(url_for('home'))


@app.route("/add_camara")
def add_camara():
    return render_template()


if __name__ == '__main__':
    app.run(port = 5000,debug=True)
