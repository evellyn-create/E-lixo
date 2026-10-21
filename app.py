from flask import Flask, render_template, request
import json
from flask import flash, redirect
from utils import db, lm
import os
from flask_migrate import Migrate
from models import User, Residuo, Ponto_de_coleta
from controllers.User import bp_usuarios
from controllers.Residuo import bp_residuo
from controllers.Ponto import bp_pontos


app = Flask(__name__)
app.secret_key = 'e-lixo'
app.register_blueprint(bp_usuarios, url_prefix='/usuarios')
app.register_blueprint(bp_residuo, url_prefix='/residuo')
app.register_blueprint(bp_pontos, url_prefix='/pontos')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_usuario = os.getenv('DB_USERNAME')
db_senha = os.getenv('DB_PASSWORD')
db_mydb = os.getenv('DB_DATABASE')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

conexao = f"mysql+pymysql://{db_usuario}:{db_senha}@{db_host}:{db_port}/{db_mydb}"
print(conexao)
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/pontos_add')
def pontos_add():
    return render_template('pontos_add.html', pontos=PONTOS_COLETA)


@app.route('/residuo_add')
def residuo_add():
    return render_template('residuo_add.html')


@app.route('/pontos_get')
def pontos_get():
    return render_template('pontos_get.html')


@app.route('/residuo_get')
def residuo_get():
    return render_template('residuo_get.html')


@app.route('/usuario_get')
def usuario_get():
    return render_template('usuario_get.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/faleconosco')
def faleconosco():
    return render_template('faleconosco.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.errorhandler(403)
def acesso_negado(error):
    return render_template('acesso_negado.html'), 403

@app.errorhandler(404)
def pagina_nao_encontrada(error):  
    return render_template('pagina_nao_encontrada.html'), 404

if __name__ == '__main__':
    app.run(debug=True)