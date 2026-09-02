from utils import db

class User(db.Model):
    __tablename__= "user"
    id_user = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))


    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
    
    def __repr__(self):
        return "<Usuario {}>".format(self.nome)

class Residuo(db.Model):
    __tablename__ = "residuo"
    id_residuo = db.Column(db.Integer, primary_key = True)
    tipo_de_residuo = db.Column(db.String(100))
    categoria = db.Column(db.String(100))
    descricao = db.Column(db.String(100))


    def __init__(self, tipo_de_residuo, categoria, descricao):
        self.tipo_de_residuo = tipo_de_residuo
        self.categoria = categoria
        self.decricao = decricao

class Ponto_de_coleta(db.Model):
    __tablename__ = "ponto_de_coleta"
    id_ponto = db.Column(db.Integer, primary_key = True)
    endereco = db.Column(db.String(100))


    def __init__(self, endereco):
        self.endereco = endereco
