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

class Residuo(db.Model):
    __tablename__ = "residuo"

    id_residuo = db.Column(db.Integer, primary_key=True)
    tipo_de_residuo = db.Column(db.String(100))
    dispositivo = db.Column(db.String(100))
    descricao = db.Column(db.String(100))

    def __init__(self, tipo_de_residuo, dispositivo, descricao):
        self.tipo_de_residuo = tipo_de_residuo
        self.dispositivo = dispositivo
        self.descricao = descricao

class Ponto_de_coleta(db.Model):
    __tablename__ = "ponto_de_coleta"

    id_ponto = db.Column(db.Integer, primary_key=True)
    endereco = db.Column(db.String(100))

    def __init__(self, endereco):
        self.endereco = endereco
