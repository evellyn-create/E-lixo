from flask import render_template, request, redirect, flash, url_for
from models import User
from utils import db, lm
from flask import Blueprint
import flask_login
from werkzeug.security import check_password_hash


bp_usuarios = Blueprint("usuario", __name__, template_folder='templates') 

@bp_usuarios.route('/get')
def get():
	if flask_login.current_user.administrador:
		usuario = User.query.all()
	# else:
	# 	abort(403)
	return render_template('usuario_get.html', usuario=usuario)

@bp_usuarios.route('/login')
def login():
	return render_template('login.html')
	

@bp_usuarios.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
	if request.method=='GET':
		return render_template('cadastro.html')

	if request.method=='POST':
		nome = request.form.get('nome')
		email = request.form.get('email')
		senha = request.form.get('senha')
		# csenha = request.form.get('csenha')
		administrador = request.form.get('administrador') =='on'
		usuario = User(nome, email, senha, administrador)
		db.session.add(usuario)
		db.session.commit()

		flash('Dados adicionados com sucesso', 'success')
		return redirect(url_for('index'))

@bp_usuarios.route('/delete/<int:id>')
def delete(id_user):
	u = User.query.get(id_user)
	db.session.delete(u)
	db.session.commit()
	flash('Dados excluídos com sucesso', 'success')
	return redirect(url_for('.get'))

@lm.user_loader
def load_user(id_user):
	usuario = User.query.filter_by(id_user=id_user).first()
	return usuario

@bp_usuarios.route('/logout')
def logout():
	flask_login.logout_user()
	flash('Você saiu do sistema.', 'success')
	return redirect(url_for('login'))

@bp_usuarios.route('/autenticar', methods=['POST'])
def autenticar():
	email = request.form.get('email')
	senha = request.form.get('senha')
	usuario = User.query.filter_by(email=email).first()
	if usuario and check_password_hash(usuario.senha, senha):
		flask_login.login_user(usuario)
		if usuario.administrador:
			return redirect(url_for('admin'))
		return redirect(url_for('home'))
	else:
		flash('Usuário ou senha inválidos', 'danger')
		return redirect(url_for('login'))
	
@bp_usuarios.errorhandler(403)
def acesso_negado(error):
    return render_template('acesso_negado.html'), 403
		