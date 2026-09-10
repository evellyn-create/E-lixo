from flask import render_template, request, redirect, flash, url_for
from models import User
from utils import db
from flask import Blueprint

bp_usuarios = Blueprint("usuarios", __name__, template_folder='templates') 

@bp_usuarios.route('/recovery')
def recovery():
	usuarios = User.query.all()
	return render_template('usuarios_recovery.html', usuarios = usuarios)

@bp_usuarios.route('/create', methods=['GET', 'POST'])
def create():
	if request.method=='GET':
		return render_template('usuario_create.html')

	if request.method=='POST':
		nome = request.form.get('nome')
		email = request.form.get('email')
		senha = request.form.get('senha')
		csenha = request.form.get('csenha')
		usuario = User(nome, email, senha)
		db.session.add(usuario)
		db.session.commit()

		return redirect(url_for('index'))

		