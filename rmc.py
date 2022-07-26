from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    return render_template ('inicio.html')

@app.route("/consulta")
def consulta():
    return render_template('consulta.html')

@app.route("/registrar_consulta")
def registrar_consulta():
    return render_template('registrar_consulta.html')
 