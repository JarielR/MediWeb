from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_requiered, login_user, current_user
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import InputRequired, Length
from werkzeug.utils import secure_filename



# sv config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

# login config

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#Tablas de Registro Paciente
class Paciente(db.Model):
    id = db.Colum(db.Integer,primary_key = True)
    user_name = db.Column(db.String(100))
    user_ci = db.Column(db.String(10)) 
    user_sex = db.Column(db.Sting(20))
    user_blood =  db.Column(db.String(10)) 
    user_estatura =  db.Column(db.String(10)) 
    user_pat =  db.Column(db.String(500)) 

class Consultas(db.Model):
    consulta_id = db.Column (db.Integer, primary_key = True)
    consulta_user_id = db.Column (db.Integer, db.ForeingnKey('paciente.id'))
    fecha_consulta = db.Columm (db.String(100))
    razon_consulta = db.Columm (db.String(500))
    img_consulta = db.Columm(db.Text, default = 'default.jpg')
    img_name = db.Columm(db.Text)
    img_mimetype = db.Columm(db.Text)
    doctor_consulta = db.Columm (db.String(200))
    institucion_consulta = db.Columm (db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return Paciente.query.get(int(user_id))

class LoginForm(FlaskForm):
    ci = StringField('ci', validators=[InputRequiered(), Leng(min=4,max=25)])
    password = PasswordField('password', validators=[InputRequiered(), Length(min=8, max=80)])
    remember = BooleanField('remember me')




@app.route("/")
def index(): 
    return render_template('index.html')


@app.route('/registro', methods = ['GET', 'POST'])
def registro():
    if request.method =='POST':
        paciente = Paciente(
            user_name = request.form['name'],
            user_ci = request.form['ci'],
            user_sex = request.form['sex'],
            user_blood = request.form['blood'],
            user_estatura = request.form['estatura'],
            user_pat = request.form['pat']
        )
        db.session.add(paciente)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('registro.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Paciente.query.filter_by(user_ci=form.ci.date).first()
        if user:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))

        return '<h1>Invalid username or passord</h1>'

    return render_template('login.html', form=form)

@app.route('/inicio')
def inicio():
    return render_template ('inicio.html')

@app.route("/consulta", methods=['GET','POST'])
def consulta():
    if request.method == 'POST':
        pic = request.files['img']
        if not pic:
            return 'No image uploaded', 400
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype

        consulta = Consultas(
            consulta_user_id = current_user.id,
            fecha_consulta = request.form['fecha'],
            razon_consulta = request.form['razon'],
            img_consulta = pic.read(),
            img_name = filename,
            img_mimetype = mimetype,
            doctor_consulta = request.form['institucion']
        )
        db.session.add(consulta)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('consulta.html')

@app.route("/registrar_consulta")
def registrar_consulta():
    return render_template('registrar_consulta.html')
