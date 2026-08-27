from flask import Flask, render_template
import json
from flask import flash, redirect
from utils import db
import os
from flask_migrate import Migrate
from models import User


app = Flask(__name__)
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
migrate = Migrate(app, db)


PONTOS_COLETA = [
    {"nome": "Ecoponto Central - Escola", "endereco": "Av. Principal, 123", "tipo": "Todos os eletrônicos"},
    {"nome": "Cooperativa Recicla Tech", "endereco": "Rua da Reciclagem, 45", "tipo": "Pilhas e Baterias"},
    {"nome": "Secretaria de Meio Ambiente", "endereco": "Praça dos Três Poderes, s/n", "tipo": "Computadores e Celulares"}
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        if email=='evellyn@gmail.com' and senha=='123456':
            return render_template('index.html')
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        return render_template('login.html')
    return render_template('cadastro.html')


@app.route('/gestaodedescarte')
def gestaodedescarte():
    return render_template('gestaodedescarte.html', pontos=PONTOS_COLETA)


@app.route('/registroderesiduo')
def registroderesiduo():
    residuos = ["Celular", "Notebook", "Bateria", "Carregador", "Televisor Antigo"]
    return render_template('registroderesiduo.html', residuos=residuos)


@app.route('/guiadedescarte', methods=['GET', 'POST'])
def guiadedescarte():
    mensagem = None
    categoria = None
    
    if request.method == 'POST':
        categoria = request.form.get('categoria')
    
        if categoria == "bateria":
            mensagem = "ATENÇÃO: Baterias e pilhas possuem compostos químicos tóxicos. Devem ser embaladas em plástico seco e levadas apenas a pontos especializados."
        elif categoria == "computador":
            mensagem = "DICA: Lembre-se de formatar e apagar seus dados pessoais antes de descartar computadores e notebooks."
        elif categoria == "celular":
            mensagem = "IMPORTANTE: Remova o chip (SIM) e o cartão de memória antes de entregar o aparelho."
        else:
            mensagem = "Procure o ecoponto mais próximo para o descarte seguro deste material."

    return render_template('guiadedescarte.html', mensagem=mensagem, categoria=categoria)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/faleconosco')
def faleconosco():
    return render_template('faleconosco.html')

@app.route('/teste_insert') 
def teste_insert():
    user = User("Gabriel", "gabriel@ifrn.edu.br", "54321")
    db.session.add(user) #Insert into Usuario(nome, email, senha) values ('Alba Lopes', 'alba.lopes@ifrn.edu.br', '12345')
    db.session.commit()
    return 'Dados inseridos com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)