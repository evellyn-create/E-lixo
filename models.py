from datetime import datetime 
from utils import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id_user = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(255))
    administrador = db.Column(db.Boolean, default=False)

    def __init__(self, nome, email, senha, administrador):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)
        self.administrador = administrador

    def get_id(self):
        return str(self.id_user)

    def __repr__(self):
        return "<Usuario {}>".format(self.nome)

class Horario(db.Model):
    __tablename__ = 'horario'
    id_horario = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, data_hora):
        self.data_hora = data_hora
class Residuo(db.Model):
    __tablename__ = "residuo"

    id_residuo = db.Column(db.Integer, primary_key=True)
    tipo_de_residuo = db.Column(db.String(100))
    dispositivo = db.Column(db.String(100))
    descricao = db.Column(db.String(100))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    id_horario = db.Column(db.Integer, db.ForeignKey('horario.id_horario'))
    horario = db.relationship('Horario')
    
    def __init__(self, tipo_de_residuo, dispositivo, descricao, id_user, id_horario=None):
        self.tipo_de_residuo = tipo_de_residuo
        self.dispositivo = dispositivo
        self.descricao = descricao
        self.id_user = id_user
        self.id_horario = id_horario

class Mensagem(db.Model):
    __tablename__ = "mensagem"

    id_mensagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.now, nullable=False)
    id_autor = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    autor = db.relationship('User')

    def __init__(self, titulo, texto, id_autor):
        self.titulo = titulo
        self.texto = texto
        self.id_autor = id_autor


class MensagemLida(db.Model):
    __tablename__ = "mensagem_lida"

    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), primary_key=True)
    id_mensagem = db.Column(db.Integer, db.ForeignKey('mensagem.id_mensagem'), primary_key=True)

    def __init__(self, id_user, id_mensagem):
        self.id_user = id_user
        self.id_mensagem = id_mensagem


