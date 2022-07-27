from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import InputRequired, Length
from werkzeug.utils import secure_filename



# sv config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/rmc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Cierrate Sesamos'
db=SQLAlchemy(app)

# login config

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#Tablas de Registro Paciente
class Paciente(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_name = db.Column(db.String(100))
    user_ci = db.Column(db.String(10)) 
    user_sex = db.Column(db.String(20))
    user_blood =  db.Column(db.String(10)) 
    user_estatura =  db.Column(db.String(10)) 
    user_pat =  db.Column(db.String(500)) 

class Consultas(db.Model):
    consulta_id = db.Column (db.Integer, primary_key = True)
    consulta_user_id = db.Column (db.Integer, db.ForeignKey('paciente.id'))
    fecha_consulta = db.Column (db.String(100))
    razon_consulta = db.Column (db.String(500))
    img_consulta = db.Column(db.Text, default = 'default.jpg')
    img_name = db.Column(db.Text)
    img_mimetype = db.Column(db.Text)
    doctor_consulta = db.Column (db.String(200))
    institucion_consulta = db.Column (db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return Paciente.query.get(int(user_id))

class LoginForm(FlaskForm):
    ci = StringField('ci', validators=[InputRequired(), Length(min=4,max=25)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    # remember = BooleanField('remember me')



@app.route("/")
def index(): 
    return render_template('index.html')


@app.route('/registro_paciente', methods = ['GET', 'POST'])
def registro():
    if request.method =='POST':
        print("entre en post")
        paciente = Paciente(
            user_name = request.form['name'],
            user_ci = request.form['ci'],
            user_sex = request.form['sex'],
            user_blood = request.form['blood'],
            user_estatura = request.form['estatura'],
            user_pat = request.form['pat']
        )
        print(paciente)
        db.session.add(paciente)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    print(form.validate_on_submit())

    if form.validate_on_submit():
        user = Paciente.query.filter_by(user_ci=form.ci.data).first()
        print(user)
        if user:
            print("entre en el if")
            login_user(user)
            return redirect(url_for('user'))

        return '<h1>Invalid username or passord</h1>'

    return render_template('login.html', form=form)

@app.route('/inicio')
def inicio():
    return render_template ('perfil.html')

@app.route("/registro_consulta", methods=['GET','POST'])
def consulta():
    if request.method == 'POST':
        print("entre en post")
        pic = request.files['img']
        print("esta es la pic")
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
            doctor_consulta = request.form['doctor'],
            institucion_consulta=request.form['institucion']
        )
        print(consulta)
        db.session.add(consulta)
        db.session.commit()
        return redirect(url_for('user'))
    return render_template('registro_consulta.html')

@app.route("/user", methods=['GET'])
@login_required
def user():
    consultas =Consultas.query.filter_by(consulta_user_id=current_user.id)
    return render_template('perfil.html', consultas=consultas)

@app.route('/ver_consulta/foto/<id>')
def get_img(id):
    img=Consultas.query.filter_by(consulta_id=id).first()
    if not img:
        return 'no image'

    return Response(img.img_consulta, mimetype=img.img_mimetype)

@app.route('/ver_consulta/<int:consulta_id>', methods=['POST','GET'])
def ver_consulta(consulta_id):
    paciente=Paciente.query.filter_by(id=current_user.id).first()
    consulta =Consultas.query.filter_by(consulta_id=consulta_id).first()
    if not consulta:
        return 'no hay consulta con ese registro'
    
    return render_template('ver_historial.html', consulta=consulta, paciente=paciente)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
