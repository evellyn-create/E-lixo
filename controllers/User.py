from flask import render_template, request, redirect, flash, url_for
from models import User
from utils import db, lm
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user


bp_usuarios = Blueprint("usuarios", __name__, template_folder='templates') 

@bp_usuarios.route('/get')
#@login_required
def get():
	if current_user.administrador:
		usuarios = Usuario.query.all()
		return render_template('usuario_get.html', usuarios=usuarios)
	else:
		abort(403)

@bp_usuarios.route('/recovery')
def recovery():
	usuarios = User.query.all()
	return render_template('usuarios_recovery.html', usuarios = usuarios)

@bp_usuarios.route('/add', methods=['GET', 'POST'])
def add():
	if request.method=='GET':
		return render_template('usuario_add.html')

	if request.method=='POST':
		nome = request.form.get('nome')
		email = request.form.get('email')
		senha = request.form.get('senha')
		csenha = request.form.get('csenha')
		usuario = User(nome, email, senha)
		db.session.add(usuario)
		db.session.commit()

		flash('Dados adicionados com sucesso', 'success')
		return redirect(url_for('index'))

@bp_usuarios.route('/delete/<int:id>')
def delete(id):
	u = Usuario.query.get(id)
	db.session.delete(u)
	db.session.commit()
	flash('Dados excluídos com sucesso', 'success')
	return redirect(url_for('.get'))

@lm.user_loader
def load_user(id):
	usuario = Usuario.query.filter_by(id=id).first()
	return usuario

@bp_usuarios.route('/logout')
def logout():
	logout_user()
	flash('Você saiu do sistema.', 'success')
	return redirect(url_for('login'))

@bp_usuarios.route('/autenticar', methods=['POST'])
def autenticar():
	email = request.form.get('email')
	senha = request.form.get('senha')
	usuario = Usuario.query.filter_by(email=email).first()
	if usuario and check_password_hash(usuario.senha, senha):
		login_user(usuario)
		return redirect(url_for('admin'))
	else:
		flash('Usuário ou senha inválidos')
		return redirect(url_for('login'))
	
@bp_usuarios.errorhandler(403)
def acesso_negado(error):
    return render_template('acesso_negado.html'), 403
		