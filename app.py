
#Bibliotecas
from flask import Flask, render_template, request
from tinydb import TinyDB, Query
from serial.tools import list_ports
from pydobot import Dobot
from datetime import datetime

#Instanciando o Flask
app = Flask(__name__)

#Instanciando o banco de dados
log_db = TinyDB('db.json')

#Instanciando o robô e conectando com a porta serial
connectedComPorts = list_ports.comports()
robot = Dobot(port=connectedComPorts[0].device)

#Rota da página principal
@app.route('/', methods=['GET', 'POST'])
def mainPage():

    connectedComPorts = list_ports.comports()

    #Só renderiza a página de mover o robô se ele estiver conectado
    if len(connectedComPorts) > 0:
        return render_template("robozin.html")
    
    #Se o robô não estiver conectado, renderiza a página de logs
    return render_template("logs.html", log_db=log_db)

#Rota para verificar se o robô está conectado
@app.route('/conexao')
def conexao():
    connectedComPorts = list_ports.comports()

    if len(connectedComPorts) > 0:
        return '<p>O robô está conectado! ^-^ </p>'
    
    return '<p>O robô não está conectado :(</p>'

#Rota para a página de logs
@app.route('/logs')
def logPage():
    return render_template("logs.html", log_db=log_db)

#Rota para mover o robô
@app.route('/mover', methods=['POST'])
def mover():

    x = float(request.form.get("x"))
    y = float(request.form.get("y"))
    z = float(request.form.get("z"))

    robot.move_to(x=x, y=y, z=z, r=50, wait=True)

    log_db.insert({'tempo': str(datetime.now()), 'X': x, 'Y': y, 'Z': z})
    
    return f"<p> O robô veio pra cá ó: X: {x} Y: {y} Z: {z}"


if __name__ == "__main__":

    app.run(port=8000, host='0.0.0.0')